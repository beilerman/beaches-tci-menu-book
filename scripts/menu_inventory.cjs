// Read only the page's authored data literals; never run its UI in Node.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
const start = html.indexOf('const P =');
const end = html.indexOf('const BARS =', start);
if (start < 0 || end < 0) throw new Error('Menu data boundaries missing');
const {VENUES, DRINKS} = vm.runInNewContext(html.slice(start, end) + ';({VENUES,DRINKS})', {}, {timeout:1000});
const rows = [];
function add(v,m,s,it) {
  rows.push({id:`${v.id}|${m.label}|${s.t}|${it[0]}`,venue:v.name,venue_id:v.id,
    meal:m.meal,menu:m.label,menu_date:m.date||null,section:s.t,kids:!!s.kids,
    guest:!!s.guest||m.kind==='guest',name:it[0],description:it[1]||'',
    menu_source:m.url||null,section_note:s.note||null});
}
for (const v of VENUES) for (const m of v.menus||[]) for (const s of m.sections||[])
  for (const it of s.items) add(v,m,s,it);
for (const s of DRINKS) for (const it of s.items)
  add({id:'drinks',name:'Bars & drinks'},{label:s.t,meal:'drinks'},s,it);
process.stdout.write(JSON.stringify(rows));
