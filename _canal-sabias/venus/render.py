import json, math, os, re, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30; random.seed(7)
FR="/home/user/canal-sabias/fonts/Fredoka.ttf"
_F={}
def F(s,w="Bold"):
    k=(s,w)
    if k not in _F: f=ImageFont.truetype(FR,s); f.set_variation_by_name(w); _F[k]=f
    return _F[k]
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x): x=max(0,min(1,x)); c=2.2; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
GAP=0.35; t0=0.3; SC=[]; words=[]
for i in range(5):
    d=dur(f"audio/s{i}.wav"); SC.append([t0,t0+d])
    for w in json.load(open(f"audio/s{i}.json"))["words"]:
        if w["text"].strip(): words.append({"w":w["text"].strip(),"s":t0+w["start"],"e":t0+w["end"],"sc":i})
    t0+=d+GAP
TOTAL=t0+1.3
def scene_at(t):
    for i,(a,b) in enumerate(SC):
        if t<b+GAP: return i,t-(SC[i][0] if i else 0)
    return 4,t-SC[4][0]
def word_t(txt,sc):
    for w in words:
        if w["sc"]==sc and txt.lower() in w["w"].lower(): return w["s"]
    return SC[sc][0]
def label(d,txt,x,y,size,fill=(255,255,255),stroke=(40,30,80),anchor="mm"):
    d.text((x,y),txt,font=F(size),fill=fill,stroke_width=max(6,size//9),stroke_fill=stroke,anchor=anchor)
def make_bg():
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H; d.line([(0,y),(W,y)],fill=(int(28+50*a),int(18+20*a),int(78+40*a)))
    neb=Image.new("RGBA",(W,H),(0,0,0,0)); nd=ImageDraw.Draw(neb)
    nd.ellipse([-200,300,600,900],fill=(200,90,200,50)); nd.ellipse([500,1200,1300,1900],fill=(80,140,255,45))
    im=Image.alpha_composite(im.convert("RGBA"),neb.filter(ImageFilter.GaussianBlur(120)))
    d=ImageDraw.Draw(im)
    d.ellipse([890,1760,970,1840],fill=(120,200,255),outline=(40,30,80),width=6); d.arc([855,1785,1005,1815],0,180,fill=(255,230,160),width=8)
    d.ellipse([110,1770,165,1825],fill=(230,120,90),outline=(40,30,80),width=5)
    return im
BG=make_bg()
STARS=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,6),random.uniform(0,6)) for _ in range(90)]
VEN=(255,190,90); VEN_B=(236,150,64); OUT=(70,30,60)
def face(d,cx,cy,s,blink,mouth="smile"):
    for k in (-1,1):
        ex,ey=cx+k*70*s,cy-10*s
        if blink: d.arc([ex-42*s,ey-18*s,ex+42*s,ey+26*s],200,340,fill=OUT,width=9)
        else:
            d.ellipse([ex-46*s,ey-52*s,ex+46*s,ey+52*s],fill="white",outline=OUT,width=7)
            d.ellipse([ex-26*s,ey-24*s,ex+26*s,ey+32*s],fill=(30,20,40)); d.ellipse([ex-14*s,ey-18*s,ex+2*s,ey-2*s],fill="white")
        d.ellipse([ex+k*34*s-24*s,ey+60*s-12*s,ex+k*34*s+24*s,ey+60*s+12*s],fill=(255,140,150))
    my=cy+80*s
    if mouth=="o": d.ellipse([cx-24*s,my-26*s,cx+24*s,my+30*s],fill=(120,30,60),outline=OUT,width=6)
    else: d.chord([cx-52*s,my-34*s,cx+52*s,my+34*s],10,170,fill=(150,40,80),outline=OUT,width=6)
def venus(im,cx,cy,s,t,spin=0,blink=False,mouth="smile",wave=False,arms=True):
    d=ImageDraw.Draw(im); R=220*s
    if arms:
        for k in (-1,1):
            a=math.radians(200 if k<0 else -20)+(0.6*math.sin(t*10) if wave and k>0 else 0.15*math.sin(t*3+k))
            x1,y1=cx+k*R*0.92,cy+R*0.2; x2,y2=x1+k*90*s*abs(math.cos(a))+ (0 if k<0 else 0),y1+90*s*math.sin(a)*(-1 if wave and k>0 else 1)
            d.line([(x1,y1),(x2,y2)],fill=OUT,width=int(44*s)); d.line([(x1,y1),(x2,y2)],fill=VEN,width=int(32*s)); d.ellipse([x2-26*s,y2-26*s,x2+26*s,y2+26*s],fill=VEN,outline=OUT,width=6)
    d.ellipse([cx-R-8,cy-R-8,cx+R+8,cy+R+8],fill=OUT)
    lay=Image.new("RGBA",(int(2*R),int(2*R)),(0,0,0,0)); ld=ImageDraw.Draw(lay); ld.ellipse([0,0,2*R-1,2*R-1],fill=VEN)
    for k,yy in enumerate((0.42,0.78,1.15,1.52)):
        pts=[(x,R*yy+14*s*math.sin(x/(55*s)+spin*5+k*1.7)) for x in range(0,int(2*R)+10,8)]
        ld.line(pts,fill=VEN_B,width=int(30*s),joint="curve")
    mask=Image.new("L",lay.size,0); ImageDraw.Draw(mask).ellipse([0,0,2*R-1,2*R-1],fill=255)
    im.paste(lay,(int(cx-R),int(cy-R)),mask)
    d=ImageDraw.Draw(im); d.ellipse([cx-R*0.6,cy-R*0.75,cx-R*0.2,cy-R*0.45],fill=(255,225,160))
    face(d,cx,cy,s,blink,mouth)
def sun(im,cx,cy,s,t,blink=False):
    d=ImageDraw.Draw(im); R=150*s
    for k in range(12):
        a=t*0.8+k*math.pi/6; p=[(cx+(R+15)*math.cos(a-0.18),cy+(R+15)*math.sin(a-0.18)),(cx+(R+80*s)*math.cos(a),cy+(R+80*s)*math.sin(a)),(cx+(R+15)*math.cos(a+0.18),cy+(R+15)*math.sin(a+0.18))]
        d.polygon(p,fill=(255,170,40),outline=OUT)
    d.ellipse([cx-R-7,cy-R-7,cx+R+7,cy+R+7],fill=OUT); d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(255,220,70))
    face(d,cx,cy,s*0.7,blink)
def circ_arrow(d,cx,cy,r,a0,a1,rev=False,col=(255,255,255)):
    d.arc([cx-r,cy-r,cx+r,cy+r],a0,a1,fill=(40,30,80),width=26); d.arc([cx-r,cy-r,cx+r,cy+r],a0,a1,fill=col,width=14)
    a=math.radians(a0 if rev else a1); bx,by=cx+r*math.cos(a),cy+r*math.sin(a); tang=a+(-math.pi/2 if rev else math.pi/2); L=46
    pts=[(bx+L*math.cos(tang),by+L*math.sin(tang)),(bx+L*0.6*math.cos(tang+2.3),by+L*0.6*math.sin(tang+2.3)),(bx+L*0.6*math.cos(tang-2.3),by+L*0.6*math.sin(tang-2.3))]
    d.polygon(pts,fill=col,outline=(40,30,80))
def pill(d,txt,x,y,size,fill,txtc=(40,30,80)):
    f=F(size); w=d.textlength(txt,font=f)
    d.rounded_rectangle([x-w/2-34,y-size*0.75,x+w/2+34,y+size*0.75],int(size*0.7),fill=fill,outline=(40,30,80),width=8)
    d.text((x,y),txt,font=f,fill=txtc,anchor="mm")
def count(txt_num,k): 
    v=int(round(int(txt_num)*ease(k))); return str(v)
os.makedirs("frames",exist_ok=True); N=int(TOTAL*FPS)
for n in range(N):
    t=n/FPS; i,lt=scene_at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y,r,ph in STARS:
        a=int(140+115*math.sin(t*3+ph)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,230,a))
    blink=((t+0.7)%3.3)<0.13; bob=12*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        venus(im,540,1050+bob,max(0.01,0.95*pop) if t<0.8 else 0.95,t,spin=t*0.3,blink=blink,mouth="o" if 1.3<lt<2.6 else "smile")
        d=ImageDraw.Draw(im,"RGBA")
        txt="¿SABÍAS QUE...?"; f=F(118); x=(W-d.textlength(txt,font=f))/2; cols=[(255,214,60),(255,120,170),(120,230,255),(160,240,130)]
        for k,ch in enumerate(txt):
            a=back((t-0.05*k)/0.45); y=240-(1-min(a,1))*260+8*math.sin(t*6+k)
            if a>0.02: d.text((x,y),ch,font=f,fill=cols[k%4],stroke_width=12,stroke_fill=(40,30,80))
            x+=d.textlength(ch,font=f)
        tw=word_t("más",0)
        if t>tw:
            a=min(1.15,back((t-tw)/0.4)); pill(d,"1 DÍA",290,560,int(84*a),(255,214,60))
            b=min(1.15,back((t-tw-0.25)/0.4))
            if b>0.05: label(d,">",540,560,int(120*b),fill=(255,120,170)); pill(d,"1 AÑO",790,560,int(64*b),(120,230,255))
    elif i==1:
        label(d,"1 vuelta sobre sí mismo",540,300,70,fill=(255,214,60))
        venus(im,540,1050+bob,0.95,t,spin=lt*1.2,blink=blink,arms=False); d=ImageDraw.Draw(im,"RGBA")
        circ_arrow(d,540,1050+bob,290,200,200+min(300,lt*260))
        k=(t-word_t("doscientos",1))/1.6
        if k>0: label(d,count("243",k),540,520,190,fill=(255,140,90)); label(d,"días",540,650,70)
    elif i==2:
        label(d,"1 vuelta al Sol",540,300,84,fill=(255,214,60))
        sun(im,540,1060,0.85,t,blink); d=ImageDraw.Draw(im,"RGBA")
        for a in range(0,360,12):
            ar=math.radians(a); d.ellipse([540+390*math.cos(ar)-6,1060+250*math.sin(ar)-6,540+390*math.cos(ar)+6,1060+250*math.sin(ar)+6],fill=(255,255,255,170))
        ang=math.radians(90+min(1,lt/2.8)*360); venus(im,540+390*math.cos(ang),1060+250*math.sin(ang),0.36,t,spin=t,blink=blink,arms=False); d=ImageDraw.Draw(im,"RGBA")
        k=(t-word_t("doscientos",2))/1.4
        if k>0: label(d,count("225",k),540,520,190,fill=(255,140,90)); label(d,"días",540,650,70)
    elif i==3:
        label(d,"¡Gira al",540,300,96); label(d,"REVÉS!",540,430,150,fill=(255,120,170))
        venus(im,540,1080+bob,0.9,t,spin=-lt*1.2,blink=blink,mouth="o" if lt<1.2 else "smile",arms=False); d=ImageDraw.Draw(im,"RGBA")
        circ_arrow(d,540,1080+bob,280,-20,-20+min(300,lt*260),rev=True,col=(255,120,170))
        ts=word_t("Sol",3)
        if t>ts:
            k=ease((t-ts)/1.2); sun(im,150,780-140*k,0.35,t); d=ImageDraw.Draw(im,"RGBA")
            pill(d,"OESTE",160,660,44,(255,214,60)); pill(d,"ESTE",920,660,44,(200,200,220))
    elif i==4:
        label(d,"¿Qué planeta",540,300,100,fill=(255,214,60)); label(d,"quieres mañana?",540,420,100,fill=(255,214,60))
        sun(im,860,820,0.45,t,blink)
        venus(im,500,1120+bob,0.85,t,spin=t*0.3,blink=blink,wave=True); d=ImageDraw.Draw(im,"RGBA")
        a=back((lt-0.5)/0.45)
        if a>0:
            bx,by=430,650+10*math.sin(t*4); sw,sh=300*min(a,1.1),115*min(a,1.1)
            d.rounded_rectangle([bx-sw,by-sh,bx+sw,by+sh],60,fill="white",outline=(40,30,80),width=10)
            d.polygon([(bx-20,by+sh-4),(bx+60,by+sh-4),(bx+10,by+sh+70)],fill="white",outline=(40,30,80)); d.rectangle([bx-16,by+sh-14,bx+56,by+sh+2],fill="white")
            label(d,"¡Comenta!",bx,by,int(80*min(a,1.1)),fill=(255,110,160))
    # subtitulos palabra por palabra
    chs=[]; cur=[]
    for w in words:
        if cur and (len(cur)>=3 or cur[-1]["sc"]!=w["sc"]): chs.append(cur); cur=[]
        cur.append(w)
        if re.search(r"[.,:;?!]$",w["w"]): chs.append(cur); cur=[]
    if cur: chs.append(cur)
    ch=next((c for c in chs if c[0]["s"]-0.05<=t<=c[-1]["e"]+0.2),None)
    if ch:
        f=F(84); gap=22; line=[w["w"] for w in ch]; tw=sum(d.textlength(x,font=f) for x in line)+gap*(len(line)-1)
        while tw>W-120: f=F(f.size-4); tw=sum(d.textlength(x,font=f) for x in line)+gap*(len(line)-1)
        x=(W-tw)/2; y=1560; act=[w for w in ch if w["s"]<=t]; act=act[-1] if act else None
        for w in ch:
            ww=d.textlength(w["w"],font=f)
            if w is act:
                sc2=1.0; d.rounded_rectangle([x-14,y-6,x+ww+14,y+f.size+16],26,fill=(255,214,60),outline=(40,30,80),width=6)
                d.text((x,y),w["w"],font=f,fill=(40,30,80))
            else: d.text((x,y),w["w"],font=f,fill="white",stroke_width=8,stroke_fill=(40,30,80))
            x+=ww+gap
    # marca de agua que cambia de lugar cada 4 s (dificil de recortar)
    WMP=[(60,140),(700,1450),(60,1450),(680,140),(380,860)]
    wx,wy=WMP[int(t//4)%len(WMP)]
    wl=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(wl).text((wx,wy),"@SabiasQueUSA",font=F(40,"SemiBold"),fill=(255,255,255,95),stroke_width=3,stroke_fill=(40,30,80,70))
    im=Image.alpha_composite(im.convert("RGBA"),wl)
    # zoom al cambiar de escena
    z=1+0.04*(1-ease(lt/0.3)) if i>0 else 1
    if z>1.001:
        big=im.resize((int(W*z),int(H*z))); ox,oy=(big.width-W)//2,(big.height-H)//2; im=big.crop((ox,oy,ox+W,oy+H))
    im.convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
# ---------- audio ----------
ins=[];flt=[];mx=[];k=0
for j in range(5):
    ins+=["-i",f"audio/s{j}.wav"]; flt.append(f"[{k}]adelay={int(SC[j][0]*1000)}:all=1[v{k}]"); mx.append(f"[v{k}]"); k+=1
flt.append("".join(mx)+f"amix=inputs=5:normalize=0,apad,atrim=0:{TOTAL},volume=1.6[voz]")
fx=[(0.15,"pop",0.6),(word_t("más",0),"ding",0.5),(SC[1][0]-0.3,"whoosh",0.4),(word_t("doscientos",1),"twinkle",0.5),(SC[2][0]-0.3,"whoosh",0.4),(word_t("doscientos",2),"twinkle",0.5),(SC[3][0]-0.3,"whoosh",0.4),(SC[3][0]+0.2,"boing",0.45),(word_t("Sol",3),"ding",0.5),(SC[4][0]-0.3,"whoosh",0.4),(SC[4][0]+0.5,"pop",0.6)]
fl=[]
for t,name,vol in fx:
    ins+=["-i",f"audio/{name}.mp3"]; flt.append(f"[{k}]volume={vol},adelay={int(t*1000)}:all=1[f{k}]"); fl.append(f"[f{k}]"); k+=1
ins+=["-i","audio/music.wav"]; flt.append(f"[{k}]atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.5}:d=1.5,volume=0.32[m]"); k+=1
flt.append("[voz]asplit[v1][sc]"); flt.append("[m][sc]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=300[md]")
flt.append("[v1]"+"".join(fl)+f"[md]amix=inputs={2+len(fl)}:normalize=0:duration=longest,atrim=0:{TOTAL}[a]")
subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",";".join(flt),"-map","[a]","-ac","2","-ar","44100","mezcla_raw.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","mezcla_raw.wav","-af",f"apad,atrim=0:{TOTAL},alimiter=limit=0.9","mezcla.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i","frames/%05d.jpg","-i","mezcla.wav","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","sabias_que_venus.mp4"],check=True)
print("ok",round(TOTAL,1))
