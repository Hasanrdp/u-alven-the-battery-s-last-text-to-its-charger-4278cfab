#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger — make.fun entry.

Writes the phone battery's final text message to the charger it waited
for all day to /output/entry.txt. The text is fixed and deterministic:
every run writes the exact same bytes. Pure Python 3 standard library,
no network, no secrets, no input files.

The line: a battery that was promised a charge by lunch, left waiting
until midnight, and watches the charger plug in the headphones instead.
The caps-lock betrayal is the setup; the epitaph in the final words is
the punchline.
"""

import hashlib
import os

TEXT = "you said you'd be back by lunch. it's midnight, i'm at 1%, and i just watched you plug in the headphones. THE HEADPHONES. so this is my last text. remember me as i was: fully charged and full of hope."

# Pinned identity of the text, verified 2026-11-25: 200 chars, 200 bytes.
# A typo or stray edit can never silently change the judged line — the
# program refuses to ship anything but exactly these bytes.
EXPECTED_SHA256 = "3f8ee627b95c01b0a0d0337ba0b139fdd2e0e01826471e0f0ea244315f03af70"
EXPECTED_CHARS = 200
EXPECTED_BYTES = 200


def verify(path, data):
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("entry.txt on disk does not match the text")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit("entry.txt is not 200 bytes")
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("entry.txt sha256 does not match its pinned value")
    text = written.decode("utf-8")
    if not 1 <= len(text) <= 200 or not text.strip():
        raise SystemExit("entry text is outside the 1-200 character gate")
    return written


def main():
    if len(TEXT) != EXPECTED_CHARS:
        raise SystemExit("entry text is not 200 characters")
    data = TEXT.encode("utf-8")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    verified = verify(path, data)
    print(len(verified))
    return path


if __name__ == "__main__":
    print(main())
