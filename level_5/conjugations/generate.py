#!/usr/bin/env python3
"""
Walk all prompts.txt files under corpus/ and generate missing .corpus files
using fal.ai's OpenRouter endpoint.

Usage:
    python generate.py            # generate up to 10 missing files
    python generate.py -n 50      # generate up to 50 missing files
    python generate.py -n 0       # dry-run: list missing files only
    python generate.py -n 50 -p 8 # generate 50 files, 8 in parallel

Reads FAL_KEY from ~/.env (KEY=VALUE format, one per line).
"""

import argparse
import asyncio
import json
import os
import sys
import time
import urllib.request

FAL_QUEUE_URL = "https://queue.fal.run/openrouter/router"
CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "corpus", "conjugations")

SYSTEM_PROMPT = (
    "You are a linguistics dataset generator producing accurate verb conjugation tables "
    "for language model training. Output ONLY the conjugation tables — no prose, no markdown, "
    "no headers, no explanations. Follow the exact format specified in the prompt. "
    "All conjugations must be correct. Use accents and diacritics precisely."
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


def find_pending(corpus_dir: str) -> list[tuple[str, str, str]]:
    pending = []
    for root, _dirs, files in os.walk(corpus_dir):
        if "prompts.txt" not in files:
            continue
        prompts_path = os.path.join(root, "prompts.txt")
        with open(prompts_path) as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) != 2:
                    print(f"WARNING: bad format at {prompts_path}:{line_no}, skipping")
                    continue
                filename, prompt = parts
                if not filename.endswith(".corpus"):
                    print(f"WARNING: filename doesn't end with .corpus at {prompts_path}:{line_no}, skipping")
                    continue
                filepath = os.path.join(root, filename)
                if not os.path.exists(filepath):
                    pending.append((root, filename, prompt))
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
        "temperature": 0.2,
        "max_tokens": 4096,
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


async def generate_task(
    sem: asyncio.Semaphore,
    api_key: str,
    dirpath: str,
    filename: str,
    prompt: str,
    model: str,
    i: int,
    total: int,
) -> None:
    rel = os.path.relpath(os.path.join(dirpath, filename), CORPUS_DIR)
    async with sem:
        print(f"[{i}/{total}] {rel} ... ", end="", flush=True)
        try:
            content = await asyncio.to_thread(generate_one, api_key, prompt, model)
            out_path = os.path.join(dirpath, filename)
            with open(out_path, "w") as f:
                f.write(content + "\n")
            print(f"\n[{i}/{total}] {rel} OK ({len(content)} chars)")
        except Exception as e:
            print(f"\n[{i}/{total}] {rel} FAILED: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Generate missing conjugation .corpus files")
    parser.add_argument(
        "-n", type=int, default=10,
        help="Max number of files to generate (0 = dry-run, default: 10)",
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
        print("Nothing to generate — all .corpus files already exist.")
        return

    print(f"Found {len(pending)} missing .corpus files.")

    if args.n == 0:
        print("\nDry-run — files that would be generated:")
        for dirpath, filename, prompt in pending:
            rel = os.path.relpath(os.path.join(dirpath, filename), CORPUS_DIR)
            print(f"  {rel}")
        return

    api_key = load_key("FAL_KEY")
    if not api_key:
        print("ERROR: FAL_KEY not found in ~/.env", file=sys.stderr)
        sys.exit(1)

    to_generate = pending[: args.n]
    print(f"Generating {len(to_generate)} of {len(pending)} missing files "
          f"(model: {args.model}, concurrency: {args.concurrency})...\n")

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [
        generate_task(sem, api_key, dirpath, filename, prompt, args.model, i, len(to_generate))
        for i, (dirpath, filename, prompt) in enumerate(to_generate, 1)
    ]
    await asyncio.gather(*tasks)

    remaining = len(pending) - len(to_generate)
    if remaining > 0:
        print(f"\n{remaining} files still remaining. Run again to continue.")
    else:
        print("\nAll files generated!")


if __name__ == "__main__":
    asyncio.run(main())
