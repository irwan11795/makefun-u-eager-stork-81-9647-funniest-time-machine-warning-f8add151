"""In Case of Paradox - Time Machine Warning Label.

Writes a single deadpan time-machine warning label (1-120 chars,
one line, no trailing newline) to the output directory.

Run:
    python3 main.py

Output directory fallback chain:
    MAKEFUN_OUTPUT_DIR -> /output -> output/ in repo -> temp dir
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY_PART1 = "WARNING: If a paradox occurs, stay calm. "
ENTRY_PART2 = "Your replacement has been briefed and prefers your job."

# Built additively from two literals so the full label is assembled here.
ENTRY = ENTRY_PART1 + ENTRY_PART2


def validate(text):
    """Gate: 1-120 chars, single line, not whitespace-only."""
    if not isinstance(text, str):
        return False
    if not text or not text.strip():
        return False
    if len(text) < 1 or len(text) > 120:
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def resolve_output_dir():
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> output/ -> temp."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir)
    if Path("/output").is_dir() or os.access("/", os.W_OK):
        try:
            Path("/output").mkdir(parents=True, exist_ok=True)
            return Path("/output")
        except OSError:
            pass
    repo_output = Path(__file__).resolve().parent / "output"
    try:
        repo_output.mkdir(parents=True, exist_ok=True)
        return repo_output
    except OSError:
        pass
    return Path(tempfile.mkdtemp(prefix="timemachine-output-"))


def main():
    if not validate(ENTRY):
        print(f"invalid entry: {ENTRY!r}", file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    # No trailing newline: write the exact bytes.
    out_path.write_bytes(ENTRY.encode("utf-8"))
    print(f"wrote {out_path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
