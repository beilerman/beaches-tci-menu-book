// The calorie report must never overwrite the cached menu navigation.
const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const base=process.env.PREVIEW_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const context=await browser.newContext();
  const page=await context.newPage();
  const report=base+'/deliverables/nutrition/beaches-calorie-estimates.html';
  await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  await page.evaluate(async()=>{await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready;});
  await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
  await page.reload({waitUntil:'domcontentloaded'});
  assert.equal(await page.locator('.calorie').count(),505);
  await page.goto(report,{waitUntil:'domcontentloaded'});
  assert.equal(await page.locator('tbody tr').count(),533);
  await page.waitForFunction(async url=>!!(await caches.match(url)),report);
  await context.setOffline(true);
  await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  assert.equal(await page.locator('.calorie').count(),505);
  await page.goto(report,{waitUntil:'domcontentloaded'});
  assert.equal(await page.locator('tbody tr').count(),533);
  console.log(JSON.stringify({passed:true,base,offlineMenuCalories:505,offlineReportRows:533}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
