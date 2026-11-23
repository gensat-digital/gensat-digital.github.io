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
# ---------- fondo marino ----------
def make_bg():
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H; d.line([(0,y),(W,y)],fill=(int(90-60*a),int(210-110*a),int(235-90*a)))
    ray=Image.new("RGBA",(W,H),(0,0,0,0)); rd=ImageDraw.Draw(ray)
    for k in range(6):
        x=120+k*170; rd.polygon([(x,0),(x+90,0),(x+260,H*0.7),(x+150,H*0.7)],fill=(255,255,255,22))
    im=Image.alpha_composite(im.convert("RGBA"),ray.filter(ImageFilter.GaussianBlur(25)))
    d=ImageDraw.Draw(im)
    d.ellipse([-300,1650,W+300,2300],fill=(244,214,150)); d.ellipse([-300,1660,W+300,2310],outline=(200,160,100),width=8)
    for x,y,c in [(160,1760,(255,150,150)),(880,1740,(255,200,120)),(520,1820,(250,180,200))]:
        d.pieslice([x-45,y-45,x+45,y+45],180,360,fill=c,outline=(120,70,60),width=5)
        for k in range(4): d.line([(x,y),(x+45*math.cos(math.radians(190+k*45)),y+45*math.sin(math.radians(190+k*45)))],fill=(120,70,60),width=3)
    return im
BG=make_bg()
BUB=[(random.uniform(0,W),random.uniform(0,H),random.uniform(8,26),random.uniform(60,160)) for _ in range(28)]
def seaweed(d,x,t,h,col,ph):
    pts=[(x+28*math.sin(t*1.6+ph+k*0.5)*(k/12),1760-k*h/12) for k in range(13)]
    d.line(pts,fill=(30,90,60),width=46,joint="curve"); d.line(pts,fill=col,width=34,joint="curve")
# ---------- pulpo ----------
PINK=(255,128,178); PINK_D=(226,92,148); OUT=(96,28,70)
def tentacle(d,x0,y0,ang,L,t,ph,wave=1.0,wavey=False):
    pts=[]
    for k in range(18):
        s=k/17; a=ang+math.sin(t*3+ph+s*3)*0.35*wave*s+ (0.9*math.sin(t*9)*s if wavey else 0)
        if k==0: x,y=x0,y0
        else: x+=math.cos(a)*L/17; y+=math.sin(a)*L/17
        pts.append((x,y))
    for k,(x,y) in enumerate(pts):
        r=34*(1-k/18)+8; d.ellipse([x-r-6,y-r-6,x+r+6,y+r+6],fill=OUT)
    for k,(x,y) in enumerate(pts):
        r=34*(1-k/18)+8; d.ellipse([x-r,y-r,x+r,y+r],fill=PINK)
    for k in range(3,17,3):
        x,y=pts[k]; r=7*(1-k/18)+3; d.ellipse([x-r,y-r,x+r,y+r],fill=(255,205,225))
def octopus(im,cx,cy,t,sc=1.0,face="smile",blink=False,wave=False):
    d=ImageDraw.Draw(im)
    angs=[math.radians(a) for a in (160,140,118,100,80,62,40,20)]
    for i,a in enumerate(angs):
        tentacle(d,cx+(i-3.5)*48*sc,cy+150*sc,a,330*sc,t,i*0.8,wavey=(wave and i==7))
    hw,hh=230*sc,215*sc
    d.ellipse([cx-hw-8,cy-hh-8,cx+hw+8,cy+hh+40*sc+8],fill=OUT); d.ellipse([cx-hw,cy-hh,cx+hw,cy+hh+40*sc],fill=PINK)
    d.ellipse([cx-hw*0.55,cy-hh*0.8,cx-hw*0.15,cy-hh*0.45],fill=(255,170,205))
    for sx,sy,r in [(110,-120,22),(150,-40,14),(-150,-60,16)]: d.ellipse([cx+sx*sc-r,cy+sy*sc-r,cx+sx*sc+r,cy+sy*sc+r],fill=PINK_D)
    for s in (-1,1):
        ex,ey=cx+s*85*sc,cy+20*sc
        if blink: d.arc([ex-48*sc,ey-20*sc,ex+48*sc,ey+30*sc],200,340,fill=OUT,width=10)
        else:
            d.ellipse([ex-55*sc,ey-62*sc,ex+55*sc,ey+62*sc],fill="white",outline=OUT,width=7)
            d.ellipse([ex-30*sc,ey-28*sc,ex+30*sc,ey+38*sc],fill=(30,20,40)); d.ellipse([ex-16*sc,ey-20*sc,ex+2*sc,ey-2*sc],fill="white"); d.ellipse([ex+8*sc,ey+10*sc,ex+16*sc,ey+18*sc],fill="white")
        d.ellipse([ex+s*40*sc-28*sc,ey+70*sc-14*sc,ex+s*40*sc+28*sc,ey+70*sc+14*sc],fill=(255,160,190))
    my=cy+110*sc
    if face=="o": d.ellipse([cx-28*sc,my-30*sc,cx+28*sc,my+34*sc],fill=(120,30,60),outline=OUT,width=6)
    else:
        d.chord([cx-60*sc,my-40*sc,cx+60*sc,my+40*sc],10,170,fill=(150,40,80),outline=OUT,width=6); d.ellipse([cx-24*sc,my+10*sc,cx+24*sc,my+36*sc],fill=(255,120,140))
def heart(d,x,y,s,col=(235,60,90),out=(110,20,40)):
    for c,pad in ((out,8),(col,0)):
        r=s*0.3+pad; d.ellipse([x-s*0.5-pad,y-s*0.45-pad,x-s*0.5+2*r-pad*0,y-s*0.45+2*r-pad*0],fill=c) if False else None
        d.ellipse([x-s*0.55-pad,y-s*0.5-pad,x+pad*0.0,y+s*0.05+pad],fill=c); d.ellipse([x-pad*0.0,y-s*0.5-pad,x+s*0.55+pad,y+s*0.05+pad],fill=c)
        d.polygon([(x-s*0.53-pad*0.9,y-s*0.12),(x+s*0.53+pad*0.9,y-s*0.12),(x,y+s*0.55+pad*1.3)],fill=c)
    d.ellipse([x-s*0.38,y-s*0.36,x-s*0.2,y-s*0.2],fill=(255,190,200))
def label(d,txt,x,y,size,fill=(255,255,255),stroke=(40,30,80),anchor="mm"):
    d.text((x,y),txt,font=F(size),fill=fill,stroke_width=max(6,size//9),stroke_fill=stroke,anchor=anchor)
def arrow(d,a,b,col=(255,255,255),w=12):
    d.line([a,b],fill=(40,30,80),width=w+10); d.line([a,b],fill=col,width=w)
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); L=34
    pts=[b,(b[0]-L*math.cos(ang-0.5),b[1]-L*math.sin(ang-0.5)),(b[0]-L*math.cos(ang+0.5),b[1]-L*math.sin(ang+0.5))]
    d.polygon(pts,fill=col,outline=(40,30,80))
def drop(d,x,y,s,col):
    d.polygon([(x,y-s*1.1),(x-s*0.72,y+s*0.1),(x+s*0.72,y+s*0.1)],fill=(40,30,80)); d.ellipse([x-s*0.8,y-s*0.5,x+s*0.8,y+s*0.95],fill=(40,30,80))
    d.polygon([(x,y-s*0.98),(x-s*0.62,y+s*0.1),(x+s*0.62,y+s*0.1)],fill=col); d.ellipse([x-s*0.7,y-s*0.42,x+s*0.7,y+s*0.85],fill=col)
    d.ellipse([x-s*0.4,y-s*0.1,x-s*0.15,y+s*0.25],fill=(255,255,255))
def mix(a,b,k): return tuple(int(a[i]+(b[i]-a[i])*k) for i in range(3))
# ---------- cuadros ----------
os.makedirs("frames",exist_ok=True); N=int(TOTAL*FPS)
for n in range(N):
    if os.path.exists(f'frames/{n:05d}.jpg') and os.environ.get('SKIP'): continue
    t=n/FPS; i,lt=scene_at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v in BUB:
        y=(y0-t*v)%H; xx=x+12*math.sin(t*2+y0); d.ellipse([xx-r,y-r,xx+r,y+r],outline=(255,255,255,150),width=4); d.ellipse([xx-r*0.5,y-r*0.6,xx-r*0.1,y-r*0.2],fill=(255,255,255,150))
    seaweed(d,70,t,520,(70,190,110),0); seaweed(d,150,t,380,(90,210,120),1.3); seaweed(d,1000,t,560,(70,190,110),2.1); seaweed(d,920,t,360,(90,210,120),0.7)
    pop=back((t-0.15)/0.5); bob=14*math.sin(t*2.2)
    cx,cy=540,1020+bob; scl=max(0.01,0.82*pop) if t<0.8 else 0.82
    if i==3: cx=430
    if i==4: cx,cy=540,1080+bob
    blink=((t+0.7)%3.3)<0.13
    face="o" if (i==3 and lt<2.0) or (i==0 and 1.2<lt<2.4) else "smile"
    octopus(im,cx,cy,t,scl,face,blink,wave=(i==4))
    d=ImageDraw.Draw(im,"RGBA")
    # titulo ¿SABIAS QUE...?
    if i==0 or t<SC[0][1]+0.2:
        txt="¿SABÍAS QUE...?"; f=F(118); x=(W-d.textlength(txt,font=f))/2; cols=[(255,214,60),(255,120,170),(120,230,255),(160,240,130)]
        for k,ch in enumerate(txt):
            a=back((t-0.05*k)/0.45); y=260-(1-min(a,1))*260+8*math.sin(t*6+k)
            if a>0.02: d.text((x,y),ch,font=f,fill=cols[k%4],stroke_width=12,stroke_fill=(40,30,80))
            x+=d.textlength(ch,font=f)
        tw=word_t("tres",0)
        if t>tw:
            a=back((t-tw)/0.4); label(d,"3",540,560,int(190*min(a,1.2)),fill=(255,90,120))
            for k in range(3):
                hk=back((t-tw-0.15*k)/0.35); heart(d,330+k*210,760,90*min(hk,1.2)*(1+0.08*math.sin(t*10)))
    elif i==1:
        label(d,"2 corazones",540,300,100,fill=(255,214,60)); label(d,"van a las branquias",540,410,56)
        for s in (-1,1):
            hk=back((lt-0.4-(0 if s<0 else 0.25))/0.4); hx,hy=cx+s*300,cy+120
            if hk>0: heart(d,hx,hy,110*min(hk,1.2)*(1+0.1*max(0,math.sin(t*9)))); label(d,"branquia",hx,hy+120,40)
            for k in range(3):
                by=hy-90-((t*120+k*60)%180); d.ellipse([hx-14+s*10,by-14,hx+14+s*10,by+14],outline="white",width=4)
    elif i==2:
        label(d,"1 corazón",540,300,100,fill=(255,214,60)); label(d,"para todo el cuerpo",540,410,56)
        hk=back((lt-0.2)/0.45); heart(d,cx,cy-30,170*min(hk,1.2)*(1+0.1*max(0,math.sin(t*9))))
        if lt>0.7:
            for a in (150,120,90,60,30):
                ar=math.radians(a); k=ease((lt-0.7)/0.5); r0=150; r1=150+200*k
                arrow(d,(cx+r0*math.cos(ar),cy+130+r0*math.sin(ar)*0.6),(cx+r1*math.cos(ar),cy+130+r1*math.sin(ar)*0.9))
    elif i==3:
        label(d,"¡Su sangre es",540,300,96); label(d,"AZUL!",540,430,150,fill=(90,170,255))
        k=ease((lt-0.6)/1.0); col=mix((230,50,70),(60,130,255),k); s=110*min(1.15,back((lt-0.1)/0.4))
        drop(d,830,1000+8*math.sin(t*3),s,col)
        if lt>1.6:
            a=back((lt-1.6)/0.4); r=80*min(a,1.15)
            d.ellipse([830-r,1240-r,830+r,1240+r],fill=(214,130,70),outline=(40,30,80),width=8); label(d,"Cu",830,1240,int(70*min(a,1.15)),fill=(255,240,220))
            label(d,"cobre",830,1350,46)
        if 0.6<lt<1.8:
            for k in range(6):
                ang=k*1.05+t*2; rr=150+20*math.sin(t*8); sx,sy=830+rr*math.cos(ang),1000+rr*math.sin(ang)
                d.regular_polygon((sx,sy,14),4,rotation=45,fill=(255,250,180))
    elif i==4:
        label(d,"¿Qué animal",540,300,100,fill=(255,214,60)); label(d,"quieres mañana?",540,420,100,fill=(255,214,60))
        a=back((lt-0.5)/0.45); bx,by=540,650+10*math.sin(t*4)
        if a>0:
            sw,sh=360*min(a,1.1),130*min(a,1.1)
            d.rounded_rectangle([bx-sw,by-sh,bx+sw,by+sh],60,fill="white",outline=(40,30,80),width=10)
            d.polygon([(bx-60,by+sh-4),(bx+20,by+sh-4),(bx-80,by+sh+70)],fill="white",outline=(40,30,80))
            d.rectangle([bx-56,by+sh-14,bx+16,by+sh+2],fill="white")
            label(d,"¡Comenta! 👇".replace(" 👇",""),bx,by,int(86*min(a,1.1)),fill=(255,110,160))
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
fx=[(0.15,"pop",0.6),(word_t("tres",0),"ding",0.5),(SC[1][0]-0.3,"whoosh",0.4),(SC[1][0]+0.4,"boing",0.4),(SC[1][0]+0.3,"bubbles",0.3),(SC[2][0]-0.3,"whoosh",0.4),(SC[2][0]+0.2,"boing",0.45),(SC[3][0]-0.3,"whoosh",0.4),(SC[3][0]+1.6,"ding",0.5),(SC[4][0]-0.3,"whoosh",0.4),(SC[4][0]+0.5,"pop",0.6)]
fl=[]
for t,name,vol in fx:
    ins+=["-i",f"audio/{name}.mp3"]; flt.append(f"[{k}]volume={vol},adelay={int(t*1000)}:all=1[f{k}]"); fl.append(f"[f{k}]"); k+=1
ins+=["-i","audio/music.wav"]; flt.append(f"[{k}]atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.5}:d=1.5,volume=0.32[m]"); k+=1
flt.append("[voz]asplit[v1][sc]"); flt.append("[m][sc]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=300[md]")
flt.append("[v1]"+"".join(fl)+f"[md]amix=inputs={2+len(fl)}:normalize=0:duration=longest,atrim=0:{TOTAL}[a]")
subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",";".join(flt),"-map","[a]","-ac","2","-ar","44100","mezcla_raw.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","mezcla_raw.wav","-af",f"apad,atrim=0:{TOTAL},alimiter=limit=0.9","mezcla.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i","frames/%05d.jpg","-i","mezcla.wav","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","sabias_que_pulpo.mp4"],check=True)
print("ok",round(TOTAL,1))
