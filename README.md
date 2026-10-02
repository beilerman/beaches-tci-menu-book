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

Photo galleries use locally stored WebP images in `assets/photos/`, with provenance and dish matches in `catalog.json` (also embedded as `PHOTOS` in the page). Loaded photos cache for offline revisits; photos not yet loaded still require a connection. Guest pictures reflect earlier visits, not guaranteed current presentation.
