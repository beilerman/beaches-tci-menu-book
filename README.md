# Beaches TCI Menu Book

Unofficial family guide to the posted menus, hours, bars and drinks at Beaches Turks & Caicos, compiled September 28, 2026.

Live: https://beaches-tci-menu-book.vercel.app (pushes to `main` deploy automatically)

- Single static page: `index.html` (no build step). Vercel serves it as-is.
- Menu data lives in the `VENUES`, `DRINKS` and `BARS` arrays near the top of the script in `index.html`.
- Sources are listed in the page footer; each menu links its resort PDF.
- Link to one place with its id as the hash, e.g. `#kimonos`, `#sky`, `#drinks`.
- `sw.js` keeps the last-loaded copy for offline use (resort Wi-Fi is spotty). Bump `CACHE` in `sw.js` if you add files to its `CORE` list.
- `og.png`, `apple-touch-icon.png` and `icon-512.png` are rendered from `favicon.svg` and the page fonts; `manifest.webmanifest` lets it be added to a phone's home screen.
- The site is deliberately `noindex` (`robots.txt` + meta tag); links still unfurl with a preview card.

Not affiliated with Beaches Resorts or Sandals.

Calorie estimates were prepared October 26, 2026 for the saved menu inventory:
480 modeled entries and 53 explicitly unavailable. All numeric entries are
**Grade D — Use with caution**, using assumed edible portions and USDA food
proxies. Grades describe evidence quality, not healthfulness. These are not
official Beaches nutrition, and the menu inventory has not been fully refreshed.
Each dish shows its serving basis, calorie scenario range, assumptions and sources.

- [Searchable calorie report](deliverables/nutrition/beaches-calorie-estimates.html)
- [Full method and limitations](data/nutrition/methodology.txt)
- [Calorie audit JSON](data/nutrition/estimates.json)
- Explicit assignments: `scripts/nutrition_models.py`; retained USDA data: `data/nutrition/profiles.json`.
- Rebuild: `python3 scripts/build_nutrition.py`; freshness check: `python3 scripts/build_nutrition.py --check`.
- Checks: `python3 -m unittest discover -s tests -v`; browser flow: `node scripts/check_nutrition.cjs` (requires Playwright and a local server at port 8765).
- Calorie display data is embedded in the HTML so online/offline page versions agree.

Photo galleries use 88 locally stored WebP images across 26 venues, with provenance
and 12 named dish-photo matches in `assets/photos/catalog.json` (also embedded as
`PHOTOS` in the page). The October 26 pass added 47 images: 24 official restaurant/
promotional images and 23 credited guest photos. Four new photos match specific
dishes; an existing Pinta spaghetti photo gained a dish match. The review record
is `data/photos/review-2026-10-26.json`.

Loaded photos cache for offline revisits; photos not yet loaded still require a
connection. Guest pictures reflect earlier visits, not guaranteed current
presentation. Photos may show extra sides and never calibrate calorie estimates.
Validate/re-embed: `python3 scripts/sync_photos.py`; check only with `--check`.
The helper requires Pillow. Photo and calorie updates must both pass their checks.
