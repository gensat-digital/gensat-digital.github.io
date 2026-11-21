# Genera un Short vertical 1080x1920 con tipografia animada (sin stock, sin rostro).
import json, sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
spec=json.load(open(sys.argv[1])); out=sys.argv[2]
B="/usr/share/fonts/opentype/inter/Inter-Black.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
if not os.path.exists(B): B=R="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fb=lambda s:ImageFont.truetype(B,s); fr=lambda s:ImageFont.truetype(R,s)
BG=(14,17,22); ACC=tuple(spec.get("accent",[46,204,113])); WHITE=(245,245,240); GREY=(150,158,170)
def wrap(d,text,font,maxw):
    words,lines,cur=text.split(),[],""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
frames_dir=out+"_f"; os.makedirs(frames_dir,exist_ok=True)
n=0; scenes=spec["scenes"]
for si,sc in enumerate(scenes):
    dur=int(sc["sec"]*FPS)
    for i in range(dur):
        t=i/FPS; im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
        # fondo: rejilla sutil que se desplaza
        off=int((n*1.5)%120)
        for y in range(-120,H,120): d.line([(0,y+off),(W,y+off)],fill=(22,26,33),width=2)
        # barra de progreso
        d.rectangle([0,0,int(W*(n/sum(int(s['sec']*FPS) for s in scenes))),12],fill=ACC)
        d.text((70,110),spec["tag"],font=fr(40),fill=GREY)
        if sc.get("num"):
            a=ease(t/0.4); base=260
            while d.textlength(sc["num"],font=fb(base))>W-140: base-=10
            f=fb(int(base*(0.6+0.4*a)))
            d.text((70,330),sc["num"],font=f,fill=ACC)
        f=fb(sc.get("size",96)); lines=wrap(d,sc["text"],f,W-140)
        y=820 if sc.get("num") else 700
        shown=ease(t/0.5)
        for li,l in enumerate(lines):
            a=ease((t-li*0.12)/0.35); dy=int((1-a)*40)
            col=tuple(int(BG[k]+(WHITE[k]-BG[k])*a) for k in range(3))
            d.text((70,y+dy),l,font=f,fill=col); y+=int(f.size*1.15)
        if sc.get("sub"):
            a=ease((t-0.5)/0.4); col=tuple(int(BG[k]+(GREY[k]-BG[k])*a) for k in range(3))
            for l in wrap(d,sc["sub"],fr(54),W-140): y+=10; d.text((70,y+20),l,font=fr(54),fill=col); y+=60
        if sc.get("bar") is not None:
            v=sc["bar"]*ease(t/0.8); d.rounded_rectangle([70,1500,W-70,1560],30,fill=(30,35,44))
            d.rounded_rectangle([70,1500,70+int((W-140)*v),1560],30,fill=ACC)
        d.text((70,H-170),spec["handle"],font=fb(44),fill=WHITE)
        im.save(f"{frames_dir}/{n:05d}.png"); n+=1
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{frames_dir}/%05d.png",
  "-f","lavfi","-i","anoisesrc=c=brown:a=0.02,lowpass=f=400",
  "-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","aac","-b:a","128k",out],check=True)
subprocess.run(["rm","-rf",frames_dir]); print("ok",out,n/FPS,"s")
