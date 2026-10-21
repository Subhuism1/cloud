const { chromium } = require('playwright-core'); const fs=require('fs'); const {PNG}=require('pngjs'); const {openInvite,scrollH}=require('./opener');
const slug=process.argv[2]; const dir=`../probe/${slug}`; fs.mkdirSync(dir,{recursive:true});
const diff=(a,b)=>{const A=PNG.sync.read(a),B=PNG.sync.read(b); if(A.width!==B.width||A.height!==B.height) return 99; let s=0; for(let i=0;i<A.data.length;i+=4*7){s+=Math.abs(A.data[i]-B.data[i])+Math.abs(A.data[i+1]-B.data[i+1])+Math.abs(A.data[i+2]-B.data[i+2]);} return s/(A.data.length/(4*7))/3;};
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox'],proxy:{server:process.env.HTTPS_PROXY}});
  const ctx=await b.newContext({viewport:{width:450,height:800},deviceScaleFactor:0.3}); const p=await ctx.newPage();
  try{ await p.goto(`https://saveourdate.in/templates/${slug}/live`,{waitUntil:'networkidle',timeout:60000}); }catch(e){ await p.goto(`https://saveourdate.in/templates/${slug}/live`,{timeout:60000}); }
  await p.waitForTimeout(1500); const g0=await p.screenshot(); const h0=await scrollH(p);
  const t0=Date.now(); const r=await openInvite(p); const openSecs=(Date.now()-t0)/1000; await p.waitForTimeout(800);
  const g1=await p.screenshot(); const openedDiff=diff(g0,g1);
  await p.mouse.move(225,450); let prev=g1, y=0, still=0, ds=[];
  for(let i=0;i<40;i++){ await p.mouse.wheel(0,450); await p.waitForTimeout(650); const g=await p.screenshot(); const d=diff(prev,g); ds.push(+d.toFixed(1)); prev=g; y+=450;
    if(d<1.2) still++; else still=0; if(still>=3 && i>=3) break; }
  const endY=y-450*3; const H=await scrollH(p);
  fs.writeFileSync(`${dir}/info3.json`,JSON.stringify({...r,openSecs,openedDiff:+openedDiff.toFixed(1),endY,H,ds}));
  await b.close();
})().catch(e=>{console.error(slug,'ERR',e.message);process.exit(1)});
