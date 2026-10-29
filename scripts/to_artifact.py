#!/usr/bin/env python3
"""Turn a rendered flow map into a claude.ai Artifact page: no document wrapper, a short title,
and dark tokens that also follow the viewer's explicit theme choice."""
import argparse, re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--title", required=True, help="Two to four words, e.g. 'Activity Navigation Flow'")
    args = ap.parse_args()
    s = args.html.read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", s, re.S).group(1)
    body = re.search(r"<body>(.*)</body>", s, re.S).group(1)
    head = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", head)
    head = re.sub(r"<title>.*?</title>", f"<title>{args.title}</title>", head)
    m = re.search(r'@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme="light"\]\) \{(.*?)\}\s*\}', head, re.S)
    dark = m.group(1).strip()
    head = head.replace(m.group(0),
                        '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {' + dark + " color-scheme: dark; }\n}\n"
                        ':root[data-theme="dark"] {' + dark + " color-scheme: dark; }")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(head.strip() + "\n" + body.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
