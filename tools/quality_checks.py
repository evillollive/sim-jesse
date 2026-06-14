#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def expect(pattern: str, text: str, msg: str) -> None:
    if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is None:
        fail(msg)


def forbid(pattern: str, text: str, msg: str) -> None:
    if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
        fail(msg)


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")

    # Security baseline
    expect(
        r'<meta\s+name="referrer"\s+content="no-referrer"\s*/?>',
        html,
        "Missing referrer policy meta tag.",
    )
    expect(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="[^"]+">\s*',
        html,
        "Missing Content Security Policy meta tag.",
    )
    forbid(r"<iframe\b|<object\b|<embed\b", html, "Unexpected embedded active content found.")

    # Accessibility baseline
    expect(r"<html\s+lang=\"[a-zA-Z-]+\"", html, "Missing language declaration on html tag.")
    forbid(r'role="application"', html, "role=\"application\" should not be used for this document.")
    expect(r'id="sub"[^>]*aria-live="polite"', html, "Caption region should use aria-live=\"polite\".")
    expect(r'id="menubar"[^>]*role="menubar"', html, "Menu bar should expose role=\"menubar\".")
    expect(r'id="speak"[^>]*aria-pressed="false"', html, "Speak control should expose aria-pressed.")
    expect(r'id="music"[^>]*aria-pressed="false"', html, "Music control should expose aria-pressed.")
    expect(r'id="nature"[^>]*aria-pressed="false"', html, "Nature control should expose aria-pressed.")

    # Ensure buttons define explicit type
    for match in re.finditer(r"<button\b([^>]*)>", html, flags=re.IGNORECASE):
        attrs = match.group(1)
        if re.search(r'\btype\s*=\s*"button"', attrs, flags=re.IGNORECASE) is None:
            fail("Found button without explicit type=\"button\".")

    print("[PASS] quality_checks.py: security and accessibility baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
