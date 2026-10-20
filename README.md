# Ornith 1.5 122B 100 HTML Files

100 self-contained HTML visual studies generated with Ornith 1.5 122B.

[Browse the gallery](https://miaai-lab.github.io/Ornith-1.5-122B-HTML-Files/)

Each gallery card includes a rendered screenshot, a link to the standalone HTML page, its design description, and an expandable generation prompt. Matching `.txt` files contain the complete accompanying notes.

The gallery layout follows [Fable 5.1 100 HTML Files](https://miaai-lab.github.io/Fable-5.1-100-HTML-Files/).

To rebuild the gallery after changing studies or text files:

```sh
python scripts/build_gallery.py
```

To regenerate screenshots (1440 × 900):

```sh
pip install playwright
playwright install chromium
python scripts/capture_screenshots.py
```

GitHub Pages serves the root of the `main` branch. No build step is required.
