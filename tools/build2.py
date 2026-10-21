import json, sys, subprocess, os, shutil
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-cloud/02f5615b-cee2-533b-b799-a291afed47c6/scratchpad'
cfg=json.load(open(sys.argv[1])); slug=cfg['slug']; W,H=1080,1920
work=f'{S}/w_{slug}'; os.makedirs(work+'/ov',exist_ok=True)
def run(*a,**k): subprocess.run(a,check=True,**k)
# 1. voice
segs=[[t,p] for t,p in cfg['segs']]
json.dump(segs,open(f'{work}/segs.json','w'))
if not os.path.exists(f'{work}/voice.wav'):
    run(f'{S}/kokoro/v/bin/python',f'{S}/kokoro/tts.py',cfg.get('voice','af_heart'),str(cfg.get('speed',1.04)),f'{work}/voice.wav',f'{work}/segs.json',cwd=f'{S}/kokoro')
    # tts.py writes relative to cwd? ensure path
M=json.load(open(f'{work}/voice.wav.json')); D=round(M[-1][1]+1.6,1)
print('duration',D,M)
# 2. waypoints
m=M
pi=json.load(open(f'{S}/probe/{slug}/info3.json'))
maxY=max(pi['endY'], pi['H']-850 if pi['H']>1100 else 0)
s0=m[2][0]-0.5; s1=m[4][0]+1.2
Yend=min(0.95*maxY, 780*(s1-s0)); Yend=max(Yend,300)
pf=cfg.get('plateau',0.3); d3=m[2][1]-m[2][0]
wp=[[0,0],[s0,0],[m[2][0]+0.3*d3,pf*0.75*Yend],[m[2][0]+0.5*d3,pf*0.85*Yend],[m[2][1],0.72*Yend],[m[3][1],0.88*Yend],[s1,Yend],[D+1,Yend+60]]
wp=[[round(t,2),round(y)] for t,y in wp]
if not os.path.exists(f'{work}/cap/frames.txt'):
    run('node',f'{S}/pw/capture2.js',slug,f'{work}/cap',str(D+0.6),json.dumps(wp),json.dumps(pi.get('actions') or []),str(cfg.get('openAt',1.8)),cwd=f'{S}/pw')
# 3. overlays
def F(name,size): return ImageFont.truetype(subprocess.run(['fc-match','-f','%{file}',name],capture_output=True,text=True).stdout,size)
serif=lambda s:F(cfg.get('serif','Bitstream Charter:bold'),s); sans=lambda s:F('Inter:semibold',s); sansb=lambda s:F('Inter:extrabold',s)
GOLD=tuple(cfg['gold']); CREAM=(255,247,230); TINT=tuple(cfg['tint']); ENDBG=tuple(cfg['endbg'])+(238,)
def center(d,y,t,f,fill,maxw=820):
    size=f.size
    while d.textlength(t,font=f)>maxw and size>24:
        size-=3; f=ImageFont.truetype(f.path,size)
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
PY=cfg.get('panel_y',1290)
def panel(name,lines,y0=None,pad=46,alpha=165,w=900):
    y0=y0 or PY
    im=Image.new('RGBA',(W,H),(0,0,0,0)); hgt=pad*2+sum(f.size+22 for _,f,_ in lines)-22; x0=(W-w)//2
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle((x0,y0,x0+w,y0+hgt),radius=48,fill=TINT+(alpha,),outline=GOLD+(120,),width=2)
    im.alpha_composite(ov); d=ImageDraw.Draw(im); y=y0+pad
    for t,f,c in lines: center(d,y,t,f,c); y+=f.size+22
    im.save(f'{work}/ov/{name}.png')
panel('hook',[(cfg['hook'][0],serif(62),CREAM),(cfg['hook'][1],serif(62),GOLD)])
panel('name',[(cfg['title'].upper(),serif(100),GOLD),(cfg['name_sub'],sans(36),CREAM)])
panel('c1',[(cfg['c1'][0],serif(64),CREAM),(cfg['c1'][1],sans(44),GOLD)])
panel('c3',[('RSVP in one tap',serif(76),CREAM),('Track every reply on your dashboard',sans(40),GOLD)])
panel('price',[('ONE-TIME  ·  NO SUBSCRIPTION',sans(36),GOLD),(f"₹{cfg['inr']}",sansb(190),CREAM),(f"or  ${cfg['usd']}  outside India",sans(58),GOLD),('Available worldwide',sans(46),CREAM)],pad=44,alpha=215,y0=min(PY+30,1310))
bg=Image.new('RGBA',(W,H),ENDBG); d=ImageDraw.Draw(bg)
center(d,520,'saveourdate.in',serif(110),GOLD); center(d,700,'Wedding invitation websites',sans(46),CREAM)
center(d,810,'Templates from  ₹299  /  $4',sansb(64),CREAM); center(d,930,'Available worldwide',sans(50),GOLD)
d.rounded_rectangle((150,1130,930,1330),radius=100,fill=GOLD+(255,))
center(d,1160,f"Comment  “{cfg['kw'].upper()}”",sansb(76),ENDBG[:3],maxw=700); center(d,1262,'and I’ll send you the link',sans(38),ENDBG[:3])
bg.save(f'{work}/ov/end.png')
# 4. compose
tl=[('hook',0.2,m[0][1]),('name',m[1][0]-0.05,m[1][1]+0.05),('c1',m[2][0],m[2][1]),('c3',m[3][0],m[3][1]+0.1),('price',m[4][0],m[4][1]+0.1),('end',m[5][0],D)]
zoom=cfg.get('zoom',0.07); zdir=cfg.get('zdir','in'); drift=cfg.get('drift',0)
zexp=(f'1.06+{zoom}*t/{D}' if zdir=='in' else f'1.06+{zoom}*(1-t/{D})')
inputs=[]; fc=[f"[0:v]fps=30,trim=duration={D},setpts=PTS-STARTPTS,scale=w='trunc(1080*({zexp})/2)*2':h='trunc(1920*({zexp})/2)*2':eval=frame:flags=lanczos,crop=1080:1920:x='(iw-1080)/2+{drift}*sin(t*0.7)':y='(ih-1920)/2',unsharp=5:5:0.7,format=rgba[b0]"]
for i,(n,a,b) in enumerate(tl,1):
    inputs+=['-loop','1','-t',str(D),'-i',f'{work}/ov/{n}.png']
    fo='' if n=='end' else f",fade=t=out:st={round(b-0.4,2)}:d=0.4:alpha=1"
    fc.append(f"[{i}:v]format=rgba,fade=t=in:st={round(a,2)}:d=0.5:alpha=1{fo}[o{i}]")
last='b0'
for i in range(1,len(tl)+1): fc.append(f"[{last}][o{i}]overlay[b{i}]"); last=f'b{i}'
fc.append(f"[{last}]format=yuv420p[v]")
run('ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{work}/cap/frames.txt',*inputs,'-filter_complex',';'.join(fc),'-map','[v]','-t',str(D),'-r','30','-c:v','libx264','-crf','24','-preset','medium','-pix_fmt','yuv420p',f'{work}/silent.mp4')
# 5. music + mix
run(f'{S}/kokoro/v/bin/python',f'{S}/music.py',f'{work}/music.wav',str(D+2),json.dumps(cfg['music']))
os.makedirs(os.environ.get('OUTDIR','/home/user/cloud/out'),exist_ok=True); out=f"{os.environ.get('OUTDIR','/home/user/cloud/out')}/{slug}_final.mp4"
run('ffmpeg','-y','-loglevel','error','-i',f'{work}/silent.mp4','-i',f'{work}/voice.wav','-i',f'{work}/music.wav','-filter_complex',f"[1:a]aresample=48000,apad=whole_dur={D},asplit=2[v][k];[2:a]aresample=48000,volume=0.42,atrim=0:{D}[m0];[m0][k]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=500:makeup=1[m];[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]",'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(D),out)
print('OK',out,D)
