#!/usr/bin/env python3
"""Generate Japanese and Arabic pages from English and reviewed locale data.

Run `python3 -B _build/i18n.py`; use `--check` to verify without writing.
Every replacement is checked before any output is written. Locale copy lives
in ja.json and ar.json; update the matching source string when English changes.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")
COMMON_NAV = ["About", "Expertise", "Teaching", "Publications", "Milestones", "Links"]


def build(cfg):
    s = SRC
    lang = cfg["lang"]
    errors = []

    def rep(old, new, count=1):
        nonlocal s
        n = s.count(old)
        if (count and n != count) or (not count and n == 0):
            errors.append(f"[{lang}] expected {count or '>=1'} of: {old[:90]!r}, found {n}")
            return
        s = s.replace(old, new)

    for pair in cfg["pairs"]:
        rep(*pair)
    for en, tr in zip(COMMON_NAV, cfg["nav"]):
        rep(f'">{en}</a></li>', f'">{tr}</a></li>', 2)
    rep('<html lang="en">', f'<html lang="{lang}" dir="{cfg["dir"]}">')
    rep('<title>Amil Khanzada</title>', f'<title>{cfg["title"]}</title>')
    rep('<link rel="canonical" href="https://amilkhanzada.com/">', f'<link rel="canonical" href="https://amilkhanzada.com/{lang}/">')
    rep('<meta property="og:url" content="https://amilkhanzada.com/">', f'<meta property="og:url" content="https://amilkhanzada.com/{lang}/">')
    rep('"url": "https://amilkhanzada.com/",', f'"url": "https://amilkhanzada.com/{lang}/",')
    rep('href="https://fonts.googleapis.com/css2?', f'href="https://fonts.googleapis.com/css2?{cfg["fonts"]}')
    rep('</style>', cfg["font_css"] + '</style>')
    # local assets live one folder up
    s = re.sub(r'(src|href)="(img/|favicon\.svg|apple-touch-icon\.png)', r'\1="../\2', s)
    # language switcher for this page
    sw = re.search(r'<!--LANG-->.*?<!--/LANG-->', s, re.S)
    if not sw:
        errors.append(f"[{lang}] language switcher markers missing")
    else:
        cur = {'en': '', 'ja': '', 'ar': ''}
        cur[lang] = ' aria-current="true"'
        aria = re.search(r'<div class="lang-switch" aria-label="([^"]*)">', sw.group(0)).group(1)
        block = ('<!--LANG-->\n    <div class="lang-switch" aria-label="%s">\n'
                 '      <a href="../" hreflang="en"%s>EN</a>\n'
                 '      <a href="../ja/" hreflang="ja" lang="ja"%s>日本語</a>\n'
                 '      <a href="../ar/" hreflang="ar" lang="ar"%s>العربية</a>\n'
                 '    </div>\n    <!--/LANG-->') % (aria, cur['en'], cur['ja'], cur['ar'])
        s = s[:sw.start()] + block + s[sw.end():]
    if errors:
        raise ValueError("\n".join(errors))
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs without writing")
    args = parser.parse_args()
    outputs = {}
    for lang in ("ja", "ar"):
        cfg = json.loads((ROOT / "_build" / f"{lang}.json").read_text(encoding="utf-8"))
        if cfg["lang"] != lang:
            raise ValueError(f"Unexpected locale in {lang}.json")
        outputs[ROOT / lang / "index.html"] = build(cfg)
    stale = []
    for path, text in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        parser.exit(1, "Stale locale pages: " + ", ".join(stale) + "\n")
    if args.check:
        print("Japanese and Arabic pages match the reviewed locale sources.")


if __name__ == "__main__":
    main()
