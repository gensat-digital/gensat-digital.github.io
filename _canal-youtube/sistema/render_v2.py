# Short v2: voz ElevenLabs + subtitulos palabra por palabra + numeros animados + musica + efectos.
import json, sys, os, re, subprocess, urllib.request, uuid
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
spec=json.load(open(sys.argv[1])); out=sys.argv[2]; voice=spec.get("voice","gbTn1bmCvNgk0QEAVyfM")
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets")
work=out+"_work"; os.makedirs(work,exist_ok=True)
API="https://api.elevenlabs.io"
def post(url,body,ctype="application/json"):
    req=urllib.request.Request(API+url,data=body,headers={"Content-Type":ctype,"xi-api-key":"proxy-injected"})
    return urllib.request.urlopen(req).read()
def tts(text,path):
    b=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True}}).encode()
    open(path,"wb").write(post(f"/v1/text-to-speech/{voice}?output_format=mp3_44100_128",b))
def align(audio,text,path):
    bnd=uuid.uuid4().hex; body=b""
    body+=f"--{bnd}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{text}\r\n".encode()
    body+=f"--{bnd}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode()+open(audio,"rb").read()+f"\r\n--{bnd}--\r\n".encode()
    open(path,"w").write(post("/v1/forced-alignment",body,f"multipart/form-data; boundary={bnd}").decode())
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
GAP=0.25; TAIL=1.2
# 1) voz + alineacion
t0=0.0; words=[]; parts=[]
for i,sc in enumerate(spec["scenes"]):
    p=f"{work}/s{i}.mp3"; j=f"{work}/s{i}.json"
    if not os.path.exists(p): tts(sc["say"],p)
    if not os.path.exists(j): align(p,sc["say"],j)
    wv=f"{work}/p{i}.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error","-i",p,"-ar","44100","-ac","1",wv],check=True)
    d=dur(wv); sc["t0"]=t0; sc["t1"]=t0+d+GAP
    for w in json.load(open(j))["words"]:
        if w["text"].strip(): words.append({"w":w["text"].strip(),"s":t0+w["start"],"e":t0+w["end"],"scene":i})
    parts.append(p); t0=sc["t1"]
spec["scenes"][-1]["t1"]+=TAIL; total=spec["scenes"][-1]["t1"]
# 2) agrupar subtitulos (max 4 palabras, corta en puntuacion)
chunks=[]; cur=[]
for w in words:
    if cur and (len(cur)>=4 or cur[-1]["scene"]!=w["scene"]): chunks.append(cur); cur=[]
    cur.append(w)
    if re.search(r"[.,:;?!]$",w["w"]): chunks.append(cur); cur=[]
if cur: chunks.append(cur)
# 2b) B-roll: cuando la voz dice una palabra clave, aparece su ilustracion
import unicodedata, sys as _sys
_sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import icons
def norm(x): return "".join(ch for ch in unicodedata.normalize("NFD",x.lower()) if unicodedata.category(ch)!="Mn" and ch.isalnum())
BMAP={norm(k):v for k,v in spec.get("broll",{}).items()}
events=[]
for w in words:
    ic=BMAP.get(norm(w["w"]))
    if ic and (not events or events[-1]["icon"]!=ic) and not spec["scenes"][w["scene"]].get("nobroll"):
        events.append({"t":w["s"],"icon":ic,"scene":w["scene"]})
ICON_IMG={}
# 3) audio
sil=f"{work}/sil.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",str(GAP),sil],check=True)
# cada mp3 se pasa a wav primero (el concat directo de mp3 perdia el final)
wavs=[]
for k,p in enumerate(parts):
    wavs+=[f"{work}/p{k}.wav",sil]
ins=sum([["-i",w] for w in wavs],[])
raw=f"{work}/raw.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex","".join(f"[{k}]" for k in range(len(wavs)))+f"concat=n={len(wavs)}:v=0:a=1,apad=pad_dur={TAIL}[o]","-map","[o]",raw],check=True)
print("voz",round(dur(raw),2),"esperado",round(total,2))
voz=f"{work}/voz.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af","loudnorm=I=-15:TP=-1.5","-ar","44100",voz],check=True)
# efectos: whoosh al cambiar de escena, pop cuando aparece un numero
fx=[(sc["t0"],"whoosh") for sc in spec["scenes"][1:]]+[(e["t"],"pop") for e in events if not any(abs(e["t"]-sc["t0"])<0.3 for sc in spec["scenes"])]+[(sc["t0"]+0.05,"pop") for sc in spec["scenes"] if sc.get("num") or sc.get("options")]
music=spec.get("music",f"{A}/musica1.mp3")
inputs=["-i",voz,"-stream_loop","-1","-i",music]; flt=[f"[1]atrim=0:{total},afade=t=in:d=0.8,afade=t=out:st={total-1.8}:d=1.8,volume=0.33[m]","[0]asplit[v][sc]","[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]"]
mix=["[v]","[md]"]
for k,(t,name) in enumerate(fx):
    inputs+=["-i",f"{A}/{name}.mp3"]; idx=2+k
    flt.append(f"[{idx}]volume={0.35 if name=='whoosh' else 0.5},adelay={int(t*1000)}|{int(t*1000)}[f{k}]"); mix.append(f"[f{k}]")
flt.append("".join(mix)+f"amix=inputs={len(mix)}:duration=first:normalize=0,atrim=0:{total}[a]")
audio=f"{work}/audio.m4a"
subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(flt),"-map","[a]","-c:a","aac","-b:a","160k",audio],check=True)
# 4) video
B="/usr/share/fonts/opentype/inter/Inter-Black.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"; SB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F={}
def f(path,s):
    k=(path,int(s))
    if k not in F: F[k]=ImageFont.truetype(path,int(s))
    return F[k]
BG=(14,17,22); ACC=tuple(spec.get("accent",[46,204,113])); WH=(245,245,240); GR=(150,158,170); DK=(30,35,44)
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x):
    x=max(0,min(1,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def wrap(d,text,font,maxw):
    out,cur=[],""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur); cur=w
    out.append(cur); return out
def mix(c1,c2,a): return tuple(int(c1[k]+(c2[k]-c1[k])*a) for k in range(3))
def countup(s,a):
    m=re.search(r"[\d,\.]+",s)
    if not m or a>=1: return s
    raw=m.group(0).replace(",",""); 
    try: v=float(raw)
    except: return s
    nv=v*ease(a); txt=f"{int(round(nv)):,}" if "," in m.group(0) or v>=1000 else str(int(round(nv)))
    return s[:m.start()]+txt+s[m.end():]
fd=f"{work}/frames"; os.makedirs(fd,exist_ok=True)
N=int(round(total*FPS))
for n in range(N):
    t=n/FPS; sc=next(s for s in spec["scenes"] if s["t0"]<=t<s["t1"] or s is spec["scenes"][-1]); lt=t-sc["t0"]
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    off=int((n*1.5)%120)
    for y in range(-120,H,120): d.line([(0,y+off),(W,y+off)],fill=(22,26,33),width=2)
    d.rectangle([0,0,int(W*t/total),12],fill=ACC)
    d.text((70,110),spec["tag"],font=f(R,40),fill=GR)
    y=300
    if sc.get("num"):
        a=back(lt/0.45); base=250
        txt=countup(sc["num"],lt/1.0) if sc.get("count") else sc["num"]
        while d.textlength(sc["num"],font=f(B,base))>W-140: base-=10
        fn=f(B,max(10,base*(0.5+0.5*a))); d.text((70,y+int((1-min(a,1))*30)),txt,font=fn,fill=ACC); y+=int(base*1.25)
    if sc.get("text"):
        fn=f(B,sc.get("size",76))
        for li,l in enumerate(wrap(d,sc["text"],fn,W-140)):
            a=ease((lt-li*0.1)/0.35); d.text((70,y+int((1-a)*30)),l,font=fn,fill=mix(BG,WH,a)); y+=int(fn.size*1.18)
    if sc.get("options"):
        y+=20
        for k,o in enumerate(sc["options"]):
            a=ease((lt-0.3-k*0.45)/0.3)
            if a<=0: continue
            hl=sc.get("reveal") is not None and k==sc["reveal"] and lt>sc.get("reveal_at",99)
            fo=f(SB,56)
            while d.textlength(o,font=fo)>W-220: fo=f(SB,fo.size-2)
            d.rounded_rectangle([70,y,W-70,y+120],28,fill=mix(BG,ACC if hl else DK,a))
            d.text((110,y+60-fo.size//2-6),o,font=fo,fill=mix(BG,BG if hl else WH,a)); y+=145
    if sc.get("bar") is not None:
        v=sc["bar"]*ease((lt-0.3)/0.9); d.rounded_rectangle([70,y+30,W-70,y+90],30,fill=DK)
        if v>0: d.rounded_rectangle([70,y+30,70+max(60,int((W-140)*v)),y+90],30,fill=ACC)
    if sc.get("sub"):
        a=ease((lt-0.6)/0.4)
        for l in wrap(d,sc["sub"],f(R,46),W-140): d.text((70,1480),l,font=f(R,46),fill=mix(BG,GR,a))
    ev=None
    for e in events:
        if e["t"]<=t: ev=e
    if ev and t-ev["t"]<4.5 and spec["scenes"][ev["scene"]] is sc:
        if ev["icon"] not in ICON_IMG: ICON_IMG[ev["icon"]]=icons.get(ev["icon"],ACC)
        a=back((t-ev["t"])/0.35); sz=max(2,int(380*min(a,1.15)))
        ic=ICON_IMG[ev["icon"]].resize((sz,sz)); bob=int(8*__import__("math").sin((t-ev["t"])*3))
        im.paste(ic,(W//2-sz//2,1035-sz//2+bob),ic)
    # subtitulos palabra por palabra
    ch=next((c for c in chunks if c[0]["s"]-0.05<=t<=c[-1]["e"]+0.25),None)
    if ch:
        fs=f(B,82); line=" ".join(w["w"] for w in ch); GAPW=26
        while d.textlength(line,font=fs)+GAPW*len(ch)>W-140 and fs.size>50: fs=f(B,fs.size-4)
        x=(W-d.textlength(line,font=fs)-GAPW*(len(ch)-1))/2; cy=1270
        cur=[w for w in ch if w["s"]<=t]; cur=cur[-1] if cur else None
        for w in ch:
            ww=d.textlength(w["w"],font=fs); act=w is cur
            if act: d.rounded_rectangle([x-12,cy-8,x+ww+12,cy+fs.size+18],18,fill=ACC)
            d.text((x,cy),w["w"],font=fs,fill=BG if act else WH); x+=ww+d.textlength(" ",font=fs)+GAPW
    d.text((70,H-170),spec["handle"],font=f(B,44),fill=WH)
    # zoom suave al entrar a cada escena
    z=1+0.035*(1-ease(lt/0.35))
    if z>1.001:
        im=im.resize((int(W*z),int(H*z))); cx,cyy=(im.width-W)//2,(im.height-H)//2; im=im.crop((cx,cyy,cx+W,cyy+H))
    im.save(f"{fd}/{n:05d}.jpg",quality=92)
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{fd}/%05d.jpg","-i",audio,"-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","copy","-shortest",out],check=True)
subprocess.run(["rm","-rf",fd]); print("ok",out,round(total,1),"s")
