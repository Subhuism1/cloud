import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
voice, speed, out, segf = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
segs = json.load(open(segf))  # [[text, pause_after],...]
k = Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
sr=24000; audio=[]; t=0.0; marks=[]
for text,pause in segs:
    s,sr = k.create(text, voice=voice, speed=speed, lang='en-us')
    marks.append([round(t,2), round(t+len(s)/sr,2), text[:40]])
    audio.append(s); t+=len(s)/sr
    audio.append(np.zeros(int(sr*pause),dtype=np.float32)); t+=pause
a=np.concatenate(audio)
a=a/np.max(np.abs(a))*0.89
sf.write(out,a,sr)
json.dump(marks,open(out+'.json','w'))
print(round(len(a)/sr,1),'sec'); [print(m) for m in marks]
