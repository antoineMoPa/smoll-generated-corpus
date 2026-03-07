#!/usr/bin/env python3
"""
Generate 3 variations of every source .corpus file in corpus/, achieving ~4x data.

Variant files are named:
    original.corpus  →  original_v2.corpus  original_v3.corpus  original_v4.corpus

Each variant has the same schema / format / example count as the source, but with
completely different values (locations, names, numbers, dates, phrasings, etc.).

Usage:
    python expand.py -n 0          # dry-run: list pending variants
    python expand.py -n 50 -p 8    # generate 50 variants, 8 in parallel

Reads FAL_KEY from ~/.env (KEY=VALUE format, one per line).
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
import urllib.request

FAL_QUEUE_URL = "https://queue.fal.run/openrouter/router"
CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")

VARIANTS = ("_v2", "_v3", "_v4")

SYSTEM_PROMPT = (
    "You are a structured dataset generator for training small language models. "
    "Output ONLY the requested examples — no prose, no markdown, no explanation. "
    "Follow the exact format of the source file. "
    "All JSON must be valid. Never repeat an example from the source."
)


def load_key(name: str) -> str | None:
    env_path = os.path.expanduser("~/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == name:
                    return v.strip()
    return None


def is_variant(filename: str) -> bool:
    """Return True if this file is itself an expansion variant."""
    stem = filename[: -len(".corpus")]
    return any(stem.endswith(v) for v in VARIANTS)


def count_examples(content: str) -> int:
    """Count examples in a corpus file by counting separator patterns."""
    # tool_use files: each example starts with "Question:"
    # json_qa files: each example starts with "Context:"
    q = len(re.findall(r"^Question:", content, re.MULTILINE))
    c = len(re.findall(r"^Context:", content, re.MULTILINE))
    return max(q, c)


def build_expand_prompt(source_content: str, variant: str) -> str:
    n = count_examples(source_content)
    label = variant.lstrip("_").upper()  # V2, V3, V4
    return (
        f"Below is a corpus file ({label}) of structured examples.\n"
        f"Generate exactly {n} NEW examples following the IDENTICAL format and schema.\n"
        "Rules:\n"
        "- Keep the header block (Available Tools / Call Schema / Response Schema) word-for-word identical if present.\n"
        "- Change ALL values: use different locations, names, numbers, dates, object types, and question phrasings.\n"
        "- Do NOT repeat any example from the source file below.\n"
        "- Maintain the same number of examples.\n"
        "- All JSON must be valid.\n\n"
        "--- SOURCE FILE ---\n"
        + source_content
    )


def find_pending(corpus_dir: str) -> list[tuple[str, str, str]]:
    """
    Return list of (source_path, variant_suffix, variant_path) for missing variants.
    Skips files that are themselves variants.
    """
    pending = []
    for root, _dirs, files in os.walk(corpus_dir):
        for fname in sorted(files):
            if not fname.endswith(".corpus"):
                continue
            if is_variant(fname):
                continue
            source_path = os.path.join(root, fname)
            stem = fname[: -len(".corpus")]
            for v in VARIANTS:
                variant_path = os.path.join(root, f"{stem}{v}.corpus")
                if not os.path.exists(variant_path):
                    pending.append((source_path, v, variant_path))
    return pending


def _fal_request(api_key: str, method: str, url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def generate_one(api_key: str, prompt: str, model: str) -> str:
    submit = _fal_request(api_key, "POST", FAL_QUEUE_URL, {
        "model": model,
        "system_prompt": SYSTEM_PROMPT,
        "prompt": prompt,
        "temperature": 0.95,
        "max_tokens": 8192,
    })
    request_id = submit["request_id"]
    status_url = f"{FAL_QUEUE_URL}/requests/{request_id}/status"
    result_url = f"{FAL_QUEUE_URL}/requests/{request_id}"

    poll_interval = 2
    last_state = None
    while True:
        status = _fal_request(api_key, "GET", status_url)
        state = status.get("status")
        if state != last_state:
            print(f"[{state}] ", end="", flush=True)
            last_state = state
        else:
            print(".", end="", flush=True)
        if state == "COMPLETED":
            break
        if state in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Request {state}: {status}")
        time.sleep(poll_interval)

    result = _fal_request(api_key, "GET", result_url)
    if result.get("error"):
        raise RuntimeError(result["error"])
    return result["output"].strip()


async def expand_task(
    sem: asyncio.Semaphore,
    api_key: str,
    source_path: str,
    variant: str,
    variant_path: str,
    model: str,
    i: int,
    total: int,
) -> None:
    rel = os.path.relpath(variant_path, CORPUS_DIR)
    async with sem:
        print(f"[{i}/{total}] {rel} ... ", end="", flush=True)
        try:
            with open(source_path) as f:
                source_content = f.read().strip()
            prompt = build_expand_prompt(source_content, variant)
            content = await asyncio.to_thread(generate_one, api_key, prompt, model)
            with open(variant_path, "w") as f:
                f.write(content + "\n")
            print(f"\n[{i}/{total}] {rel} OK ({len(content)} chars)")
        except Exception as e:
            print(f"\n[{i}/{total}] {rel} FAILED: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Expand corpus files with value-varied duplicates")
    parser.add_argument(
        "-n", type=int, default=10,
        help="Max variants to generate (0 = dry-run, default: 10)",
    )
    parser.add_argument(
        "-p", "--concurrency", type=int, default=5,
        help="Number of concurrent requests (default: 5)",
    )
    parser.add_argument(
        "--model", type=str, default="qwen/qwen3.5-plus-02-15",
        help="Model to use (default: qwen/qwen3.5-plus-02-15)",
    )
    args = parser.parse_args()

    pending = find_pending(CORPUS_DIR)

    if not pending:
        print("Nothing to expand — all variants already exist.")
        return

    print(f"Found {len(pending)} missing variants "
          f"({len(pending) // len(VARIANTS)} source files × {len(VARIANTS)} variants).")

    if args.n == 0:
        print("\nDry-run — variants that would be generated:")
        for source_path, variant, variant_path in pending:
            print(f"  {os.path.relpath(variant_path, CORPUS_DIR)}")
        return

    api_key = load_key("FAL_KEY")
    if not api_key:
        print("ERROR: FAL_KEY not found in ~/.env", file=sys.stderr)
        sys.exit(1)

    to_generate = pending[: args.n]
    print(f"Generating {len(to_generate)} of {len(pending)} missing variants "
          f"(model: {args.model}, concurrency: {args.concurrency})...\n")

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [
        expand_task(sem, api_key, source_path, variant, variant_path, args.model, i, len(to_generate))
        for i, (source_path, variant, variant_path) in enumerate(to_generate, 1)
    ]
    await asyncio.gather(*tasks)

    remaining = len(pending) - len(to_generate)
    if remaining > 0:
        print(f"\n{remaining} variants still remaining. Run again to continue.")
    else:
        print("\nAll variants generated!")


if __name__ == "__main__":
    asyncio.run(main())
