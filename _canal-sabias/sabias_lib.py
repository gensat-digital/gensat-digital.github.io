# Base comun de los Shorts de ¿Sabías Que? USA: tiempos, textos, subtitulos, marca de agua, agradecimiento, cierre y audio.
import json, math, os, re, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
FR="/home/user/canal-sabias/fonts/Fredoka.ttf"; OUT=(40,30,80)
_F={}
def F(s,w="Bold"):
    k=(int(s),w)
    if k not in _F: f=ImageFont.truetype(FR,int(s)); f.set_variation_by_name(w); _F[k]=f
    return _F[k]
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x): x=max(0,min(1,x)); c=2.2; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
def mix(a,b,k): return tuple(int(a[i]+(b[i]-a[i])*k) for i in range(3))
class Timeline:
    def __init__(s,n,gap=0.35,start=0.3,tail=1.3):
        s.GAP=gap; t0=start; s.SC=[]; s.words=[]
        for i in range(n):
            d=dur(f"audio/s{i}.wav"); s.SC.append([t0,t0+d])
            for w in json.load(open(f"audio/s{i}.json"))["words"]:
                if w["text"].strip(): s.words.append({"w":w["text"].strip(),"s":t0+w["start"],"e":t0+w["end"],"sc":i})
            t0+=d+gap
        s.TOTAL=t0+tail; s.n=n
        s.chunks=[]; cur=[]
        for w in s.words:
            if cur and (len(cur)>=3 or cur[-1]["sc"]!=w["sc"]): s.chunks.append(cur); cur=[]
            cur.append(w)
            if re.search(r"[.,:;?!]$",w["w"]): s.chunks.append(cur); cur=[]
        if cur: s.chunks.append(cur)
    def at(s,t):
        for i,(a,b) in enumerate(s.SC):
            if t<b+s.GAP: return i,t-(s.SC[i][0] if i else 0)
        return s.n-1,t-s.SC[-1][0]
    def wt(s,txt,sc):
        for w in s.words:
            if w["sc"]==sc and txt.lower() in w["w"].lower(): return w["s"]
        return s.SC[sc][0]
def label(d,txt,x,y,size,fill=(255,255,255),stroke=OUT,anchor="mm"):
    d.text((x,y),txt,font=F(size),fill=fill,stroke_width=max(6,int(size)//9),stroke_fill=stroke,anchor=anchor)
def sparkle(d,x,y,r,col=(255,240,160)):
    d.polygon([(x,y-r),(x+r*0.28,y-r*0.28),(x+r,y),(x+r*0.28,y+r*0.28),(x,y+r),(x-r*0.28,y+r*0.28),(x-r,y),(x-r*0.28,y-r*0.28)],fill=col)
def heart(d,x,y,s,col=(235,60,90),out=(110,20,40)):
    for c,pad in ((out,8),(col,0)):
        d.ellipse([x-s*0.55-pad,y-s*0.5-pad,x,y+s*0.05+pad],fill=c); d.ellipse([x,y-s*0.5-pad,x+s*0.55+pad,y+s*0.05+pad],fill=c)
        d.polygon([(x-s*0.53-pad*0.9,y-s*0.12),(x+s*0.53+pad*0.9,y-s*0.12),(x,y+s*0.55+pad*1.3)],fill=c)
def title_sabias(d,t,y0=240):
    txt="¿SABÍAS QUE...?"; f=F(118); x=(W-d.textlength(txt,font=f))/2; cols=[(255,214,60),(255,120,170),(120,230,255),(160,240,130)]
    for k,ch in enumerate(txt):
        a=back((t-0.05*k)/0.45); y=y0-(1-min(a,1))*260+8*math.sin(t*6+k)
        if a>0.02: d.text((x,y),ch,font=f,fill=cols[k%4],stroke_width=12,stroke_fill=OUT)
        x+=d.textlength(ch,font=f)
def thanks(d,t,user,t_end):
    """Agradecimiento al seguidor que pidio el video (arriba, con corazones)."""
    a=back(t/0.45); out=ease((t-t_end)/0.4)
    if a<=0.02 or out>=1: return
    y=200-out*300; sc=min(a,1.1)
    f1=F(80*sc); f2=F(58*sc,"SemiBold")
    w=max(d.textlength("¡Gracias!",font=f1),d.textlength(user,font=f2))+120
    d.rounded_rectangle([W/2-w/2,y-80*sc,W/2+w/2,y+110*sc],50,fill=(255,255,255),outline=OUT,width=10)
    d.text((W/2,y-10*sc),"¡Gracias!",font=f1,fill=(255,90,150),anchor="mm")
    d.text((W/2,y+62*sc),user,font=f2,fill=(70,110,220),anchor="mm")
    for k,(hx,hy) in enumerate([(W/2-w/2-10,y-70),(W/2+w/2+10,y-60),(W/2+w/2-30,y+120)]):
        heart(d,hx,hy+6*math.sin(t*5+k),46*sc)
def thumb(d,x,y,s,col):
    d.rounded_rectangle([x-s*0.55,y-s*0.05,x-s*0.25,y+s*0.6],int(s*0.08),fill=col,outline=OUT,width=7)
    d.rounded_rectangle([x-s*0.2,y-s*0.1,x+s*0.55,y+s*0.6],int(s*0.18),fill=col,outline=OUT,width=7)
    d.polygon([(x-s*0.2,y),(x-s*0.05,y-s*0.6),(x+s*0.15,y-s*0.55),(x+s*0.1,y-s*0.08)],fill=col,outline=OUT)
def combub(d,x,y,s,col):
    d.rounded_rectangle([x-s*0.6,y-s*0.45,x+s*0.6,y+s*0.35],int(s*0.3),fill=col,outline=OUT,width=7)
    d.polygon([(x-s*0.25,y+s*0.3),(x+s*0.05,y+s*0.3),(x-s*0.35,y+s*0.65)],fill=col,outline=OUT)
    for k in (-1,0,1): d.ellipse([x+k*s*0.28-s*0.09,y-s*0.1-s*0.09,x+k*s*0.28+s*0.09,y-s*0.1+s*0.09],fill=OUT)
def share(d,x,y,s,col):
    pts=[(x-s*0.55,y+s*0.45),(x-s*0.55,y),(x+s*0.05,y-s*0.2),(x+s*0.05,y-s*0.55),(x+s*0.6,y),(x+s*0.05,y+s*0.55),(x+s*0.05,y+s*0.2),(x-s*0.25,y+s*0.2)]
    d.polygon(pts,fill=col,outline=OUT); d.line(pts+[pts[0]],fill=OUT,width=7)
def subbtn(d,x,y,s,col):
    d.rounded_rectangle([x-s*0.62,y-s*0.42,x+s*0.62,y+s*0.42],int(s*0.22),fill=(235,40,40),outline=OUT,width=7)
    d.polygon([(x-s*0.16,y-s*0.22),(x-s*0.16,y+s*0.22),(x+s*0.24,y)],fill="white")
CTA_LINE="¡Suscríbete para más videos de ¿Sabías Que?, dale like, comenta qué animal quieres para mañana y comparte este video!"
def cta(d,t,tl,sc):
    """Cierre obligatorio: suscríbete, like, comenta y comparte (cada uno se ilumina cuando se dice)."""
    label(d,"¿Te gustó?",W/2,330,104,fill=(255,214,60))
    items=[("suscr",subbtn,"Suscríbete",(235,40,40)),("like",thumb,"¡Like!",(120,200,255)),("comenta",combub,"Comenta",(255,214,60)),("comparte",share,"Comparte",(160,240,130))]
    for k,(key,fn,txt,col) in enumerate(items):
        t0=tl.wt(key,sc); a=back((t-t0)/0.35)
        if a<=0.02: continue
        x=W/2+(k-1.5)*250; y=590+12*math.sin(t*5+k); s=112*min(a,1.15)*(1.12 if t0<=t<t0+0.6 else 1)
        d.ellipse([x-s*0.95,y-s*0.95,x+s*0.95,y+s*0.95],fill=(255,255,255),outline=OUT,width=8)
        fn(d,x,y,s*0.8,col); label(d,txt,x,y+s*1.3,40)
def subs(d,t,tl):
    ch=next((c for c in tl.chunks if c[0]["s"]-0.05<=t<=c[-1]["e"]+0.2),None)
    if not ch: return
    f=F(84); gap=22; line=[w["w"] for w in ch]; tw=sum(d.textlength(x,font=f) for x in line)+gap*(len(line)-1)
    while tw>W-120: f=F(f.size-4); tw=sum(d.textlength(x,font=f) for x in line)+gap*(len(line)-1)
    x=(W-tw)/2; y=1560; act=[w for w in ch if w["s"]<=t]; act=act[-1] if act else None
    for w in ch:
        ww=d.textlength(w["w"],font=f)
        if w is act:
            d.rounded_rectangle([x-14,y-6,x+ww+14,y+f.size+16],26,fill=(255,214,60),outline=OUT,width=6); d.text((x,y),w["w"],font=f,fill=OUT)
        else: d.text((x,y),w["w"],font=f,fill="white",stroke_width=8,stroke_fill=OUT)
        x+=ww+gap
def finish(im,t,i,lt):
    WMP=[(60,140),(700,1450),(60,1450),(680,140),(380,860)]; wx,wy=WMP[int(t//4)%len(WMP)]
    wl=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(wl).text((wx,wy),"@SabiasQueUSA",font=F(40,"SemiBold"),fill=(255,255,255,95),stroke_width=3,stroke_fill=(40,30,80,70))
    im=Image.alpha_composite(im.convert("RGBA"),wl)
    z=1+0.04*(1-ease(lt/0.3)) if i>0 else 1
    if z>1.001:
        big=im.resize((int(W*z),int(H*z))); ox,oy=(big.width-W)//2,(big.height-H)//2; im=big.crop((ox,oy,ox+W,oy+H))
    return im
def build_audio_video(tl,fx,out):
    ins=[];flt=[];mx=[];k=0
    for j in range(tl.n):
        ins+=["-i",f"audio/s{j}.wav"]; flt.append(f"[{k}]adelay={int(tl.SC[j][0]*1000)}:all=1[v{k}]"); mx.append(f"[v{k}]"); k+=1
    flt.append("".join(mx)+f"amix=inputs={tl.n}:normalize=0,apad,atrim=0:{tl.TOTAL},volume=1.6[voz]")
    fl=[]
    for t,name,vol in fx:
        ins+=["-i",f"audio/{name}.mp3"]; flt.append(f"[{k}]volume={vol},adelay={int(max(0,t)*1000)}:all=1[f{k}]"); fl.append(f"[f{k}]"); k+=1
    ins+=["-stream_loop","-1","-i","audio/music.wav"]; flt.append(f"[{k}]atrim=0:{tl.TOTAL},afade=t=out:st={tl.TOTAL-1.5}:d=1.5,volume=0.32[m]"); k+=1
    flt.append("[voz]asplit[v1][sc]"); flt.append("[m][sc]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=300[md]")
    flt.append("[v1]"+"".join(fl)+f"[md]amix=inputs={2+len(fl)}:normalize=0:duration=longest,atrim=0:{tl.TOTAL}[a]")
    subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",";".join(flt),"-map","[a]","-ac","2","-ar","44100","mezcla_raw.wav"],check=True)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","mezcla_raw.wav","-af",f"apad,atrim=0:{tl.TOTAL},alimiter=limit=0.9","mezcla.wav"],check=True)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i","frames/%05d.jpg","-i","mezcla.wav","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out],check=True)
