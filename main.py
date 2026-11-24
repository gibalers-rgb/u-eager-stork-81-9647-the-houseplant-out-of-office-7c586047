#!/usr/bin/env python3
"""Write the houseplant out-of-office entry to /output/entry.txt.

The entry is one out-of-office auto-reply, at most 120 characters,
written as if a houseplant sent it. Deterministic, standard library
only, no network access.
"""

import os
import sys

ENTRY = (
    "Out of office. I was moved next to the radiator in July. "
    "I complained to the sun. It hasn't replied either."
)

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the bounty gate before writing anything.

    The sealed scorer accepts UTF-8 text of 1 to 120 characters that is
    not only white space; anything else scores 0 and is never judged.
    Refuse to write an invalid entry instead of failing silently.
    """
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")


def main() -> int:
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    # No trailing newline: the gate counts every character in the file,
    # so the file must hold exactly the entry text, nothing more.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    print(f"wrote {len(ENTRY)} characters to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
