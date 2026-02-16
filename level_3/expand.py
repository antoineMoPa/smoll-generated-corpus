#!/usr/bin/env python3
"""
For each sentence in corpus.txt, generate Q&A pairs where every output line is
self-contained:

    <sentence> Q: <question> A: <answer><stop>

Results are appended to llm_expanded_corpus.txt.
Progress is tracked in expand_progress.json so the script is safely resumable.

Usage:
    python expand.py            # process up to 10 batches
    python expand.py -n 50      # process up to 50 batches
    python expand.py -n 0       # dry-run: list pending batches
    python expand.py --batch-size 15 --model qwen/qwen-2.5-72b-instruct
"""

import argparse
import json
import os
import sys
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_FILE = os.path.join(SCRIPT_DIR, "corpus.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "llm_expanded_corpus.txt")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "expand_progress.json")

FAL_QUEUE_URL = "https://queue.fal.run/openrouter/router"

SYSTEM_PROMPT = """\
You generate question-and-answer training data. For each sentence you receive,
output several Q&A pairs. Every output line must follow this exact format:

<sentence> Q: <question> A: <answer>

Rules:
- Copy the sentence verbatim at the start of each line.
- Ask varied questions: who, what, where, when, how, why, what kind, how many, etc.
- Keep answers short (1–6 words).
- Output one pair per line. No blank lines, no extra text, no numbering.\
"""

PROMPT_TEMPLATE = """\
Generate question-and-answer pairs for each sentence below.

Sentences:
{sentences}
"""


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


def load_sentences() -> list[str]:
    with open(CORPUS_FILE) as f:
        sentences = [line.strip().removesuffix("<stop>").strip() for line in f]
    return [s for s in sentences if s]


def load_progress() -> set[int]:
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE) as f:
        data = json.load(f)
    # Old format was list of [chunk, style] pairs — discard it and start fresh
    if not data or not isinstance(data[0], int):
        return set()
    return set(data)


def save_progress(done: set[int]) -> None:
    with open(PROGRESS_FILE, "w") as f:
        json.dump(sorted(done), f)


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
        "temperature": 0.7,
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


def format_output(raw: str) -> str:
    """Add <stop> to each non-empty line."""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            if not line.endswith("<stop>"):
                line += "<stop>"
            lines.append(line)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Expand corpus.txt with Q&A pairs")
    parser.add_argument("-n", type=int, default=10,
                        help="Max batches to generate (0=dry-run, default: 10)")
    parser.add_argument("--batch-size", type=int, default=10,
                        help="Sentences per batch (default: 10)")
    parser.add_argument("--model", type=str, default="qwen/qwen-2.5-72b-instruct",
                        help="Model to use")
    args = parser.parse_args()

    sentences = load_sentences()
    done = load_progress()

    # Split into batches
    batches = []
    for i in range(0, len(sentences), args.batch_size):
        batches.append(sentences[i : i + args.batch_size])

    pending = [i for i in range(len(batches)) if i not in done]

    print(f"Sentences: {len(sentences)}  Batches: {len(batches)}  "
          f"Done: {len(done)}  Remaining: {len(pending)}")

    if args.n == 0:
        print("\nDry-run — first 10 pending batches:")
        for idx in pending[:10]:
            preview = batches[idx][0][:60]
            print(f"  batch {idx:4d}: \"{preview}...\"")
        return

    api_key = load_key("FAL_KEY")
    if not api_key:
        print("ERROR: FAL_KEY not found in ~/.env", file=sys.stderr)
        sys.exit(1)

    to_do = pending[: args.n]
    print(f"Generating {len(to_do)} batches (model: {args.model})...\n")

    for i, batch_idx in enumerate(to_do, 1):
        batch = batches[batch_idx]
        sentences_text = "\n".join(f"- {s}" for s in batch)
        prompt = PROMPT_TEMPLATE.format(sentences=sentences_text)

        print(f"[{i}/{len(to_do)}] batch {batch_idx} ({len(batch)} sentences) ... ",
              end="", flush=True)
        try:
            raw = generate_one(api_key, prompt, args.model)
            formatted = format_output(raw)
            with open(OUTPUT_FILE, "a") as f:
                f.write(formatted + "\n")
            done.add(batch_idx)
            save_progress(done)
            lines = formatted.count("\n") + 1
            print(f" OK ({lines} lines)")
        except Exception as e:
            print(f" FAILED: {e}")

    remaining = len(pending) - len(to_do)
    if remaining > 0:
        print(f"\n{remaining} batches still remaining. Run again to continue.")
    else:
        print("\nAll batches generated!")


if __name__ == "__main__":
    main()
