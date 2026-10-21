import sys, json, numpy as np, soundfile as sf
out, dur = sys.argv[1], float(sys.argv[2]); cfg = json.loads(sys.argv[3])
sr=44100; n=int(sr*dur); mix=np.zeros(n); rng=np.random.default_rng(cfg.get('seed',1))
bpm=cfg.get('bpm',66); beat=60/bpm; chords=cfg['chords']; mf=lambda m:440*2**((m-69)/12)
def pluck(f,length,vel):
    t=np.arange(int(sr*length))/sr; env=np.exp(-t*cfg.get('decay',3.2))*(1-np.exp(-t*400))
    y=sum(a*np.sin(2*np.pi*f*h*t+rng.uniform(0,6)) * np.exp(-t*(h-1)*1.6) for h,a in [(1,1),(2,.42),(3,.18),(4,.08)])
    y+=0.35*np.sin(2*np.pi*f*1.003*t)*np.exp(-t*2.5)
    return y*env*vel
def add(sig,at):
    i=int(at*sr); j=min(n,i+len(sig))
    if i<n: mix[i:j]+=sig[:j-i]
chord_len=cfg.get('chord_beats',8)*beat; step=beat/cfg.get('sub',2); t=0.0; k=0
pat=cfg.get('pattern',[0,1,2,3,2,1])
while t<dur:
    ch=chords[int(t//chord_len)%len(chords)]
    # pad
    if abs((t%chord_len))<1e-6 or k==0:
        L=chord_len+1.5; tt=np.arange(int(sr*L))/sr
        env=np.minimum(tt/1.8,1)*np.minimum((L-tt)/1.5,1)
        pad=sum(np.sin(2*np.pi*mf(m)*tt)+0.5*np.sin(2*np.pi*mf(m)*2.003*tt) for m in ch[:3])*env*0.05
        add(pad,t)
    note=ch[pat[k%len(pat)]%len(ch)]+ (12 if pat[k%len(pat)]>=len(ch) else 0)+cfg.get('shift',12)
    vel=0.5+0.3*rng.random()*(1 if k%2==0 else .6)
    add(pluck(mf(note),2.4,vel*0.5),t+rng.uniform(0,0.012)); 
    if k%8==0: add(pluck(mf(ch[0]-12+cfg.get('shift',12)-12+12),3.0,0.35),t)
    t+=step; k+=1
# reverb
ir=rng.standard_normal(int(sr*2.6))*np.exp(-np.arange(int(sr*2.6))/sr*2.3); ir/=np.sqrt((ir**2).sum())
N=1<<int(np.ceil(np.log2(n+len(ir)))); wet=np.fft.irfft(np.fft.rfft(mix,N)*np.fft.rfft(ir,N),N)[:n]
y=mix*0.55+wet*0.75
# soft lowpass ~3.5k
F=np.fft.rfft(y); fr=np.fft.rfftfreq(n,1/sr); F*=1/(1+(fr/3500)**4); y=np.fft.irfft(F,n)
fi=int(sr*2.0); fo=int(sr*3.0); y[:fi]*=np.linspace(0,1,fi); y[-fo:]*=np.linspace(1,0,fo)
y=y/np.max(np.abs(y))*0.8
sf.write(out,y.astype(np.float32),sr)
