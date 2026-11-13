"""Write one joke line to entry.txt under MAKEFUN_OUTPUT_DIR."""

import hashlib
import os
import sys

JOKE = "I asked it to fix a typo. It rewrote the architecture. The typo survived, and now it lives in a class."

MAX_LEN = 280


def build_payload():
    """Return the joke as utf-8 bytes with exactly one trailing newline."""
    if not JOKE.strip():
        raise ValueError("joke is blank")
    if len(JOKE) > MAX_LEN:
        raise ValueError("joke is " + str(len(JOKE)) + " characters, over limit of " + str(MAX_LEN))
    return (JOKE + "\n").encode("utf-8")


def main():
    try:
        payload = build_payload()
    except ValueError as exc:
        sys.stderr.write("error: " + str(exc) + "\n")
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        sys.stderr.write("error: unable to write entry: " + str(exc) + "\n")
        return 1

    digest = hashlib.sha256(payload).hexdigest()
    print("wrote " + str(len(payload)) + " bytes to " + path + " sha256 " + digest[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
