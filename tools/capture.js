// usage: node capture.js <slug> <outdir> <seconds> <pxPerSec> <holdStartSec>
const { chromium } = require('playwright-core');
const fs = require('fs');
const [slug, out, secs] = [process.argv[2], process.argv[3], +process.argv[4]];
const WP = JSON.parse(process.argv[5]); // [[t,y],...]
const target = t => { if (t<=WP[0][0]) return WP[0][1]; for (let i=1;i<WP.length;i++){ if (t<=WP[i][0]) { const [t0,y0]=WP[i-1],[t1,y1]=WP[i]; const u=(t-t0)/(t1-t0); const e=u*u*(3-2*u)*0.35+u*0.65; return y0+(y1-y0)*e; } } return WP[WP.length-1][1]; };
(async () => {
  fs.mkdirSync(out, {recursive:true});
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'], proxy: proxy?{server:proxy}:undefined });
  const ctx = await b.newContext({ viewport:{width:450,height:800}, deviceScaleFactor:2.4 });
  const p = await ctx.newPage();
  await p.goto(`https://saveourdate.in/templates/${slug}/live`, {waitUntil:'networkidle', timeout:60000});
  await p.waitForTimeout(1500);
  const cdp = await ctx.newCDPSession(p);
  const frames = [];
  let n = 0;
  cdp.on('Page.screencastFrame', async f => {
    const name = `f${String(n++).padStart(5,'0')}.jpg`;
    fs.writeFileSync(`${out}/${name}`, Buffer.from(f.data,'base64'));
    frames.push({name, t:f.metadata.timestamp});
    cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{});
  });
  await cdp.send('Page.startScreencast',{format:'jpeg',quality:92,everyNthFrame:1,maxWidth:1080,maxHeight:1920});
  await p.mouse.move(225,450);
  const t0 = Date.now();
  let cur = 0;
  while ((Date.now()-t0)/1000 < secs) {
    const t=(Date.now()-t0)/1000; const want = target(t); const d = want-cur;
    if (Math.abs(d)>0.5) { await p.mouse.wheel(0, d); cur += d; }
    await p.waitForTimeout(16);
  }
  await cdp.send('Page.stopScreencast');
  fs.writeFileSync(`${out}/frames.txt`, frames.map((f,i)=> `file '${f.name}'\nduration ${i<frames.length-1 ? (frames[i+1].t-f.t).toFixed(4) : 0.04}`).join('\n')+`\nfile '${frames[frames.length-1].name}'\n`);
  console.log('frames', frames.length, 'span', (frames[frames.length-1].t-frames[0].t).toFixed(1));
  await b.close();
})();
