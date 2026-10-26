/* Offline support for spotty resort Wi-Fi: the page is fetched network-first (so updates show up
   immediately when online) and falls back to the last cached copy; fonts and icons are cache-first. */
const CACHE = 'menu-book-v4-calories-photos';
const CORE = ['./', 'index.html', 'favicon.svg', 'manifest.webmanifest', 'apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {
    const root = new URL('./', self.location).href;
    const home = url.href === root || url.href === new URL('index.html', root).href;
    // The report has its own cache key; visiting it must not replace the menu.
    const key = home ? root : req;
    e.respondWith(fetch(req).then(res => {
      if (res.ok) {
        const copy = res.clone();
        e.waitUntil(caches.open(CACHE).then(c => c.put(key, copy)).catch(() => {}));
      }
      return res;
    }).catch(async () => (await caches.match(key)) ||
      (home ? await caches.match(new URL('index.html', root).href) : null) || Response.error()));
    return;
  }
  const cacheable = url.origin === location.origin || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (!cacheable) return;
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
    if (res.ok || res.type === 'opaque') { const copy = res.clone(); e.waitUntil(caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {})); }
    return res;
  })));
});
