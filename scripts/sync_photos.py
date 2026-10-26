#!/usr/bin/env python3
"""Validate and embed the credited photo catalog. No downloads or fuzzy matching."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    photos=json.loads((ROOT/'assets/photos/catalog.json').read_text())
    rows=json.loads(subprocess.check_output(['node',str(ROOT/'scripts/menu_inventory.cjs')]))
    names={}
    for r in rows:names.setdefault(r['venue_id'],set()).add(r['name'])
    page=(ROOT/'index.html').read_text()
    venue_ids=set(re.findall(r"\{id:'([^']+)', name:",page))
    paths=set()
    for p in photos:
        if p['venue'] not in venue_ids:raise ValueError('Unknown venue '+p['venue'])
        if not p['source'].startswith('https://') or not p['src'].startswith('https://') or not p['credit'] or not p['caption']:
            raise ValueError('Missing photo provenance '+p['file'])
        if p['local'] in paths:raise ValueError('Duplicate photo path '+p['local'])
        paths.add(p['local'])
        if set(p['dishes'])-names.get(p['venue'],set()):raise ValueError('Photo match not in this venue '+p['file'])
        file=ROOT/p['local']
        if not file.is_file():raise ValueError('Missing photo '+p['local'])
        with Image.open(file) as im:
            if min(im.size)<220:raise ValueError('Undersized photo '+p['file'])
            im.verify()
        if p.get('sha256') and hashlib.sha256(file.read_bytes()).hexdigest()!=p['sha256']:
            raise ValueError('Reviewed photo changed '+p['file'])
    embedded='const PHOTOS = '+json.dumps(photos,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';'
    page,n=re.subn(r'^const PHOTOS = .*?;$',lambda _:embedded,page,count=1,flags=re.M)
    if n!=1:raise ValueError('Missing PHOTOS data boundary')
    if args.check:
        if (ROOT/'index.html').read_text()!=page:raise SystemExit('Embedded photo catalog is stale')
    else:(ROOT/'index.html').write_text(page)
    matches=sum(len(p['dishes']) for p in photos)
    print(json.dumps({'photos':len(photos),'venues':len({p['venue'] for p in photos}),'named_dish_photo_matches':matches}))

if __name__=='__main__':main()
