// Check actual loaded photo assets and the enlarged source-attributed viewer.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.join(__dirname,'..');
const base=process.env.PREVIEW_URL||'http://127.0.0.1:8765';
const catalog=JSON.parse(fs.readFileSync(path.join(root,'assets/photos/catalog.json')));
const qa=path.join(root,'deliverables/nutrition/qa');
fs.mkdirSync(qa,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 const results=[];
 try {
  for(const width of [390,1440]){
   const context=await browser.newContext({viewport:{width,height:1000}});
   const page=await context.newPage();
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/#neptunes');
   await page.locator('#neptunes[open]').waitFor();
   assert.equal(await page.locator('.photo-gallery').count(),26);
   assert.equal(await page.locator('.dish-photo').count(),15);
   // Decode every catalog file in the browser, including offscreen/lazy images.
   const images=await page.evaluate(async urls=>Promise.all(urls.map(async src=>{
    const im=new Image();im.src=src;
    try{await im.decode();return {src,ok:im.naturalWidth>=220,width:im.naturalWidth,height:im.naturalHeight};}
    catch{return {src,ok:false};}
   })),catalog.map(p=>p.local));
   assert.equal(images.filter(p=>!p.ok).length,0,JSON.stringify(images.filter(p=>!p.ok)));
   await page.locator('#neptunes .tab').filter({hasText:'Breakfast'}).click();
   const eggs=page.locator('#neptunes .panel:not([hidden]) .dish').filter({hasText:'Classic Eggs Benedict'});
   assert.equal(await eggs.locator('.dish-photo').count(),1);
   await eggs.locator('.dish-photo').click();
   await page.locator('#photo-viewer[open]').waitFor();
   await page.locator('#photo-large').evaluate(im=>im.decode());
   assert.match(await page.locator('#photo-caption').innerText(),/pictured hash browns are extra/);
   assert.match(await page.locator('#photo-credit').innerText(),/Shoreline Journeys/);
   assert.match(await page.locator('#photo-credit').innerText(),/do not establish calories/);
   await page.screenshot({path:path.join(qa,`${width}-new-photo-viewer.png`)});
   await page.locator('#photo-viewer button').click();
   await page.locator('#q').fill('Soupe à l’Oignon');
   await page.locator('.r-count').waitFor();
   assert.equal(await page.locator('.r-venue .dish-photo').count(),1);
   await page.locator('.r-venue .dish-photo img').evaluate(im=>im.decode());
   await page.locator('.r-venue').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(qa,`${width}-new-soup-photo.png`)});
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   assert.deepEqual(errors,[]);
   results.push({width,catalogPhotos:images.length,galleries:26,dishPhotosRendered:15,imagesDecoded:true,errors});
   await context.close();
  }
  fs.writeFileSync(path.join(qa,'photo-results.json'),JSON.stringify({base,results},null,2)+'\n');
  console.log(JSON.stringify({passed:true,base,results},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
