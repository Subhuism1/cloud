// generic invitation opener
const scrollH = p => p.evaluate(()=>{ const de=document.documentElement; let h=de.scrollHeight;
  for (const e of document.querySelectorAll('*')) { const o=getComputedStyle(e).overflowY; if ((o=='auto'||o=='scroll') && e.scrollHeight>e.clientHeight+100) h=Math.max(h,e.scrollHeight); } return h; });
async function clickText(p, re) {
  for (const fr of p.frames()) {
  let off={x:0,y:0}; if (fr!==p.mainFrame()) { try{ const bb=await (await fr.frameElement()).boundingBox(); if(!bb) continue; off=bb; }catch(e){continue;} }
  const pt = await fr.evaluate(src => { const re=new RegExp(src,'i'); let best=null;
    for (const pass of ['button,[role=button],a', 'div,span,p,h1,h2,h3,li,img']) {
      for (const e of document.querySelectorAll(pass)) {
        const t=(e.innerText||e.alt||'').trim(); if (!t||t.length>45||!re.test(t)) continue;
        const r=e.getBoundingClientRect(); if (r.width<8||r.height<8||r.bottom<0||r.top>innerHeight) continue;
        const area=r.width*r.height; if (!best||area<best.area) best={x:r.left+r.width/2,y:r.top+r.height/2,area}; }
      if (best) break; }
    return best; }, re.source);
  if (pt) { await p.mouse.click(off.x+pt.x, off.y+pt.y); return true; }
  }
  return false;
}
const clickTextExists = async p => { for (const fr of p.frames()) { try { if (await fr.evaluate(()=>{ const re=/tap to open|open invitation|open the invitation|welcome the dawn|tap to begin|pull the rope/i;
  return [...document.querySelectorAll('button,a,div,span,p')].some(e=>{const t=(e.innerText||'').trim(); if(!t||t.length>45||!re.test(t)) return false; const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); return r.width>8&&r.height>8&&r.top<innerHeight&&r.bottom>0&&cs.visibility!='hidden'&&parseFloat(cs.opacity)>0.5;}); })) return true; } catch(e){} } return false; };
async function openInvite(p) {
  const text = () => p.evaluate(()=>document.body.innerText.slice(0,600));
  await p.waitForTimeout(2200);
  let t = await text(); const pre=[];
  if (/choose your hero background/i.test(t)) { await clickText(p,/default|lantern|^luxe/); pre.push({kind:'text',src:'default|lantern|^luxe',wait:2500}); await p.waitForTimeout(2500); }
  if (/choose your faith/i.test(t)) { await clickText(p,/hinduism/); pre.push({kind:'text',src:'hinduism',wait:2500}); await p.waitForTimeout(2500); }
  const {PNG}=require('pngjs');
  const diff=(x,y)=>{const A=PNG.sync.read(x),B=PNG.sync.read(y); if(A.width!==B.width||A.height!==B.height) return 99; let s=0,n=0; for(let i=0;i<A.data.length;i+=28){s+=Math.abs(A.data[i]-B.data[i])+Math.abs(A.data[i+1]-B.data[i+1])+Math.abs(A.data[i+2]-B.data[i+2]);n++;} return s/n/3;};
  const pts=[[225,430],[225,500],[225,380],[225,570],[225,300],[225,650]];
  for (let i=0;i<6;i++) {
    if (await scrollH(p) > 1100) return {ok:true,actions:pre};
    const before=await p.screenshot({scale:'css',clip:{x:0,y:0,width:450,height:800}});
    const hit = await clickText(p,/tap to open|open invitation|open the invitation|welcome the dawn|tap to begin|pull the rope|^open$|enter/);
    if (!hit) await p.mouse.click(...pts[i%pts.length]);
    await p.waitForTimeout(3400);
    const act = hit ? {kind:'text',src:'tap to open|open invitation|open the invitation|welcome the dawn|tap to begin|pull the rope|^open$|enter',wait:3400} : {kind:'point',pt:pts[i%pts.length],wait:3400};
    if (hit && !(await clickTextExists(p))) return {ok:true,hit:true,actions:pre.concat([act])};
    const after=await p.screenshot({scale:'css',clip:{x:0,y:0,width:450,height:800}});
    if (!hit && diff(before,after)>9) return {ok:true,visual:true,actions:pre.concat([act])};
  }
  if (await scrollH(p) > 1100) return {ok:true,actions:pre};
  if (await clickText(p,/skip/)) { await p.waitForTimeout(3000); if (await scrollH(p) > 1100) return {ok:true,skipped:true,actions:pre.concat([{kind:'text',src:'skip',wait:3000}])}; }
  return {ok:false,actions:pre};
}
async function replay(p, actions){ for (const a of actions||[]) { if (a.kind==='text') await clickText(p,new RegExp(a.src,'i')); else await p.mouse.click(a.pt[0],a.pt[1]); await p.waitForTimeout(a.wait||2500); } }
module.exports = { openInvite, scrollH, replay };
