# amilkhanzada.com

Personal website served by GitHub Pages from `master`.

## Editing

`index.html` is the English source and shared layout. Reviewed Japanese and
Arabic text lives in `_build/ja.json` and `_build/ar.json`. Preserve the exact
English source strings in each replacement; missing or ambiguous matches stop
the build before either locale page is written.

```sh
python3 -B _build/i18n.py
python3 -B _build/i18n.py --check
git diff --check
```

Check desktop and mobile layouts, both color schemes, keyboard navigation,
internal links and language switches before publishing. New papers must link
to their publisher or repository; label preprints separately from publications.

## Separate tools

`seminar/` and `teacher/` are independent tools. Personal-site edits must not
change their behavior or configuration.
