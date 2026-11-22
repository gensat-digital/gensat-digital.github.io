import math, os, subprocess, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import chars as C
W,H,FPS=1080,1920,30
A="audio"; random.seed(3)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def ss(x): x=max(0,min(1,x)); return x*x*(3-2*x)
# ---------- linea de tiempo ----------
SC=[("sala",0.0,7.0),("cuarto",7.0,13.6),("recuerdo",13.6,20.2),("puerta",20.2,27.8),("abrazo",27.8,36.4),("cierre",36.4,44.5)]
TOTAL=44.5
LINES=[("l1",1.5,"Daniel","¡Otra vez, Mateo! ¡Nunca tienes cuidado!"),
       ("l2",9.3,"Jesús","Daniel… ¿a quién escuchaste gritar así por primera vez?"),
       ("l3",15.8,"Jesús","De niño aprendiste que un error se paga con gritos."),
       ("l4",22.2,"Jesús","Él no recordará el vaso roto. Recordará cómo lo hiciste sentir."),
       ("l5",29.4,"Daniel","Perdóname, hijo. El vaso no importa. Tú sí importas.")]
for i,(k,t0,who,txt) in enumerate(LINES): LINES[i]=(k,t0,who,txt,t0+dur(f"{A}/{k}.mp3"))
# envolvente de la boca (amplitud de cada voz por frame)
import wave, struct, array
ENV={}
for k,*_ in LINES:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{A}/{k}.mp3","-ac","1","-ar","8000",f"/tmp/{k}.wav"],check=True)
    wv=wave.open(f"/tmp/{k}.wav"); n=wv.getnframes(); data=array.array("h",wv.readframes(n))
    step=8000//FPS; env=[]
    for i in range(0,len(data),step):
        seg=data[i:i+step]; env.append((sum(x*x for x in seg)/max(1,len(seg)))**0.5)
    m=max(env) or 1; ENV[k]=[min(1,e/m*1.4) for e in env]
def mouth(who,t):
    for k,t0,w,txt,t1 in LINES:
        if w==who and t0<=t<t1:
            i=int((t-t0)*FPS); e=ENV[k]; return e[i] if i<len(e) else 0
    return 0
def blink(t,seed): return ((t+seed*1.7)%3.9)<0.12
# ---------- fondos ----------
def grad(top,bot):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H; d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*a) for i in range(3)))
    return im
def bg_sala():
    im=grad((252,226,190),(240,200,160)); d=ImageDraw.Draw(im)
    d.rectangle([0,1380,W,H],fill=(178,120,80)); 
    for y in range(1380,H,70): d.line([(0,y),(W,y)],fill=(160,104,68),width=4)
    d.line([(0,1380),(W,1380)],fill=C.OUT,width=6)
    # ventana con sol
    d.rounded_rectangle([90,330,470,820],20,fill=(255,236,190),outline=C.OUT,width=6); d.line([(280,330),(280,820)],fill=C.OUT,width=6); d.line([(90,575),(470,575)],fill=C.OUT,width=6)
    d.ellipse([300,380,420,500],fill=(255,210,120))
    # puerta a la derecha
    d.rectangle([760,560,1040,1385],fill=(255,244,220),outline=C.OUT,width=6)
    # sillon y mesita
    d.rounded_rectangle([40,1020,560,1300],40,fill=(214,120,90),outline=C.OUT,width=6); d.rounded_rectangle([40,930,560,1080],40,fill=(226,138,104),outline=C.OUT,width=6)
    d.ellipse([170,200,290,320],fill=(255,240,210),outline=C.OUT,width=5)  # lampara
    return im
def bg_cuarto():
    im=grad((235,212,196),(214,184,168)); d=ImageDraw.Draw(im)
    d.rectangle([0,1420,W,H],fill=(150,110,90)); d.line([(0,1420),(W,1420)],fill=C.OUT,width=6)
    d.rounded_rectangle([60,520,360,860],16,fill=(200,215,230),outline=C.OUT,width=6)  # cuadro/ventana
    d.ellipse([820,300,1000,480],fill=(255,226,160)); d.polygon([(860,470),(960,470),(940,560),(880,560)],fill=(240,190,120),outline=C.OUT)
    # cama
    d.rounded_rectangle([80,1060,1000,1300],30,fill=(120,150,180),outline=C.OUT,width=6); d.rounded_rectangle([60,900,180,1360],20,fill=(140,96,70),outline=C.OUT,width=6)
    d.rounded_rectangle([200,1010,420,1090],30,fill=(245,240,230),outline=C.OUT,width=6)
    return im
def bg_puerta():
    im=grad((250,226,192),(236,196,156)); d=ImageDraw.Draw(im)
    d.rectangle([0,1400,W,H],fill=(178,120,80)); d.line([(0,1400),(W,1400)],fill=C.OUT,width=6)
    d.rectangle([0,0,90,H],fill=(150,100,70)); d.rectangle([0,0,W,70],fill=(150,100,70))  # marco de puerta en primer plano
    return im
def bg_cierre():
    im=grad((255,228,180),(240,170,120)); d=ImageDraw.Draw(im,"RGBA")
    for k in range(9):
        a=math.radians(-90+(k-4)*12); d.polygon([(W/2,-200),(W/2+2400*math.cos(a-0.05),-200+2400*math.sin(a+1.6)),(W/2+2400*math.cos(a+0.05),-200+2400*math.sin(a+1.6))],fill=(255,255,240,28))
    return im.filter(ImageFilter.GaussianBlur(6))
BG={"sala":bg_sala(),"cuarto":bg_cuarto(),"puerta":bg_puerta(),"cierre":bg_cierre()}
BG["recuerdo"]=bg_sala(); BG["abrazo"]=BG["sala"]
FB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; FBL="/usr/share/fonts/opentype/inter/Inter-Black.otf"; FSER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def font(p,s): return ImageFont.truetype(p,s)
def glass(d,x,y,broken=False,s=1):
    if not broken:
        d.polygon([(x-30*s,y-90*s),(x+30*s,y-90*s),(x+24*s,y),(x-24*s,y)],fill=(230,240,245),outline=C.OUT); d.polygon([(x-26*s,y-55*s),(x+26*s,y-55*s),(x+24*s,y),(x-24*s,y)],fill=(250,160,40))
    else:
        d.ellipse([x-150*s,y-20*s,x+150*s,y+30*s],fill=(250,160,40))
        for dx,dy,r in [(-90,-10,22),(40,5,26),(100,-15,18),(-20,15,16),(130,10,14)]:
            d.polygon([(x+dx*s,y+dy*s-r*s),(x+dx*s+r*s,y+dy*s+r*0.4*s),(x+dx*s-r*0.6*s,y+dy*s+r*0.5*s)],fill=(225,240,248),outline=C.OUT)
def tears(d,x,y,t,s=1):
    for k in range(2):
        ph=(t*0.9+k*0.5)%1
        for sgn in (-1,1):
            tx=x+sgn*28*s; ty=y+ph*70*s
            d.ellipse([tx-7*s,ty-10*s,tx+7*s,ty+8*s],fill=(120,180,235,int(255*(1-ph))))
def crack(im,x,y,heal=0,t=0):
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    pts=[(x-10,y-70),(x+18,y-30),(x-14,y+5),(x+20,y+40),(x-6,y+80)]
    a=1-heal
    if a>0.01:
        glow=int(110*a*(0.8+0.2*math.sin(t*4)))
        d.line(pts,fill=(160,40,90,glow),width=46,joint="curve")
        lay=lay.filter(ImageFilter.GaussianBlur(14)); d=ImageDraw.Draw(lay)
        d.line(pts,fill=(25,15,30,int(255*a)),width=12,joint="curve"); d.line(pts,fill=(230,90,150,int(220*a)),width=3,joint="curve")
    if heal>0:
        g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); R=60+260*heal
        gd.ellipse([x-R,y-R,x+R,y+R],fill=(255,220,140,int(170*math.sin(math.pi*min(heal,1)))))
        lay=Image.alpha_composite(lay,g.filter(ImageFilter.GaussianBlur(40)))
    im.alpha_composite(lay)
def sepia(im):
    g=ImageOps.grayscale(im.convert("RGB")); s=ImageOps.colorize(g,(60,38,20),(250,226,180))
    v=Image.new("L",(W,H),0); vd=ImageDraw.Draw(v); vd.ellipse([-200,-100,W+200,H+100],fill=255); v=v.filter(ImageFilter.GaussianBlur(160))
    dark=Image.new("RGB",(W,H),(30,20,10)); return Image.composite(s,dark,v).convert("RGBA")
def glow_behind(im,x,y,r,a=90):
    g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).ellipse([x-r,y-r,x+r,y+r],fill=(255,240,200,a)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(60)))
GLOW_CACHE={}
def jglow(im,x,y,r):
    k=(int(x),int(y),int(r))
    if k not in GLOW_CACHE:
        g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).ellipse([x-r,y-r,x+r,y+r],fill=(255,240,200,80)); GLOW_CACHE[k]=g.filter(ImageFilter.GaussianBlur(60))
    im.alpha_composite(GLOW_CACHE[k])
# ---------- escenas ----------
def scene(name,lt,t):
    im=BG[name].copy().convert("RGBA"); d=ImageDraw.Draw(im,"RGBA")
    if name=="sala":
        # Mateo empuja el vaso a t=0.6; Daniel grita; Jesus en la puerta
        jglow(im,870,1000,260); d=ImageDraw.Draw(im,"RGBA")
        C.person(d,C.JESUS,870,1385,780,expr="sad",blink=blink(t,2),look=-1)
        shake=int(6*math.sin(t*40)) if 1.5<t<5.0 else 0
        C.person(d,C.DANIEL,280+shake,1560,1080,pose="point" if t>1.4 else "stand",expr="angry" if t>1.2 else "neutral",mouth=mouth("Daniel",t),blink=blink(t,0),look=1,arm=int(8*math.sin(t*6)))
        mx=640
        C.person(d,C.MATEO,mx,1600,600,expr="sad" if t>0.7 else "neutral",blink=blink(t,1),look=-1,child=True)
        glass(d,mx+150,1610,broken=t>0.6) if t>0.6 else glass(d,mx+90-120*ss(lt/0.6),1470+140*ss(lt/0.6),False)
        if t>1.0: tears(d,mx,1600-600+90+20,t,1)
    elif name=="cuarto":
        come=ease((lt-0.4)/1.0)
        C.person(d,C.DANIEL,360,1500,1060,pose="sit",expr="angry" if lt<5.0 else "sad",blink=blink(t,0),look=1 if lt>1 else 0)
        if come>0:
            lay=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
            jglow(lay,760,1050,240); ld=ImageDraw.Draw(lay)
            C.person(ld,C.JESUS,760,1500,1080,pose="sit",expr="neutral",mouth=mouth("Jesús",t),blink=blink(t,2),look=-1)
            lay.putalpha(Image.eval(lay.getchannel("A"),lambda a:int(a*come))); im.alpha_composite(lay)
    elif name=="recuerdo":
        trem=int(5*math.sin(t*50))
        C.person(d,C.PADRE,260,1620,1200,pose="point",expr="angry",mouth=0.5+0.5*abs(math.sin(t*9)) if lt<3.5 else 0.2,look=1,arm=int(10*math.sin(t*7)))
        C.person(d,C.NINO,700+trem,1600,580,pose="tremble",expr="sad",blink=blink(t,1),look=-1,child=True)
        glass(d,820,1610,broken=True)
        tears(d,700+trem,1100,t,1)
        im=sepia(im)
    elif name=="puerta":
        jglow(im,290,1000,250); d=ImageDraw.Draw(im,"RGBA")
        C.person(d,C.JESUS,290,1420,1000,expr="sad",mouth=mouth("Jesús",t),blink=blink(t,2),look=1)
        C.person(d,C.DANIEL,520,1440,1000,expr="sad",blink=blink(t,0),look=1)
        mi=C.person(d,C.MATEO,800,1540,640,pose="hugknees",expr="sad",blink=blink(t,1),child=True)
        tears(d,800,mi["head"][1]+mi["head"][2]*0.2,t,1)
        crack(im,800,mi["sh_y"]+100,0,t)
    elif name=="abrazo":
        jglow(im,880,980,230); d=ImageDraw.Draw(im,"RGBA")
        sm=1 if lt>4.5 else 0
        jc=dict(C.JESUS); jc["smile"]=sm
        C.person(d,jc,880,1400,800,expr="neutral" if sm else "sad",blink=blink(t,2),look=-1)
        k=ease(lt/0.9); mx=560
        dd=dict(C.DANIEL); dd["smile"]=1 if lt>6.2 else 0
        dxp=int(330-80*k)
        info=C.person(d,dd,mx-dxp+60,1640,1000,pose="kneel",expr="sad",mouth=mouth("Daniel",t),blink=blink(t,0),look=1)
        mc=dict(C.MATEO); mc["smile"]=1 if lt>5.5 else 0
        mi=C.person(d,mc,mx,1640,620,expr="sad" if lt<4 else "neutral",blink=blink(t,1),child=True,look=-1)
        if k>0.2:
            sx=mx-dxp+60+info["tw"]*0.46; sy=info["sh_y"]+70
            hx=mx+mi["tw"]*0.5+10; hy=mi["sh_y"]+75
            C.limb(d,(sx,sy),(hx,hy),70,C.DANIEL["shirt"],1000)
            d.ellipse([hx-36,hy-36,hx+36,hy+36],fill=C.SKIN,outline=C.OUT,width=6)
        if lt<4: tears(d,mx,mi["head"][1]+mi["head"][2]*0.2,t,1)
        crack(im,mx,mi["sh_y"]+110,ss((lt-3.2)/2.8),t)
    elif name=="cierre":
        f1=font(FBL,74); f2=font(FSER,46); f3=font(FB,40)
        def center(txt,f,y,a,col):
            lines=[]; cur=""
            for w in txt.split():
                tt=(cur+" "+w).strip()
                if d.textlength(tt,font=f)<W-160: cur=tt
                else: lines.append(cur); cur=w
            lines.append(cur)
            for l in lines:
                d.text(((W-d.textlength(l,font=f))/2+3,y+3),l,font=f,fill=(120,60,30,int(90*a)))
                d.text(((W-d.textlength(l,font=f))/2,y),l,font=f,fill=col+(int(255*a),)); y+=int(f.size*1.25)
            return y
        a1=ease((lt-0.5)/1.0); a2=ease((lt-2.6)/1.0)
        y=center("Un error no se corrige con gritos.",f1,620,a1,(70,36,24))
        y=center("Se corrige con amor.",f1,y+20,a1,(150,50,40))
        d.line([(W/2-120,y+70),(W/2+120,y+70)],fill=(150,70,40,int(200*a2)),width=4)
        y=center("«La blanda respuesta quita la ira»",f2,y+130,a2,(70,36,24))
        center("Proverbios 15:1",f3,y+20,a2,(120,60,30))
    return im
def cam(im,name,p):
    if name=="cierre": z=1+0.04*p; cy=960
    else: z=1.12+0.05*p; cy=1150
    big=im.resize((int(W*z),int(H*z))); ox=(big.width-W)//2; oy=int(cy*z-960); oy=max(0,min(big.height-H,oy))
    return big.crop((ox,oy,ox+W,oy+H))
# ---------- subtitulos ----------
def subs(im,t):
    for k,t0,who,txt,t1 in LINES:
        if t0-0.05<=t<=t1+0.35:
            d=ImageDraw.Draw(im,"RGBA"); f=font(FBL,58); fn=font(FB,40)
            words=txt.split(); lines=[]; cur=""
            for w in words:
                tt=(cur+" "+w).strip()
                if d.textlength(tt,font=f)<W-140: cur=tt
                else: lines.append(cur); cur=w
            lines.append(cur)
            band=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(band).rectangle([0,1600,W,H],fill=(25,15,10,110)); im.alpha_composite(band.filter(ImageFilter.GaussianBlur(30))); d=ImageDraw.Draw(im,"RGBA")
            y=1700-(len(lines)-1)*36; col=(255,214,120) if who=="Jesús" else (170,230,190)
            d.text(((W-d.textlength(who,font=fn))/2,y-56),who,font=fn,fill=col,stroke_width=5,stroke_fill=(30,20,15))
            for l in lines:
                d.text(((W-d.textlength(l,font=f))/2,y),l,font=f,fill=(255,255,255),stroke_width=7,stroke_fill=(30,20,15)); y+=72
# ---------- render ----------
os.makedirs("frames",exist_ok=True)
N=int(TOTAL*FPS); XF=0.45
for n in range(N):
    t=n/FPS
    cur=[s for s in SC if s[1]<=t<s[2]] or [SC[-1]]; name,a,b=cur[0]
    im=scene(name,t-a,t)
    # zoom lento tipo camara
    im=cam(im,name,(t-a)/(b-a))
    # fundido cruzado con la escena anterior
    i=[s[0] for s in SC].index(name)
    if i>0 and t-a<XF:
        pn,pa,pb=SC[i-1]; prev=cam(scene(pn,t-pa,t),pn,1.0)
        im=Image.blend(prev,im,ss((t-a)/XF))
    if name!="cierre": subs(im,t)
    # difuminado final
    if t>TOTAL-2.2:
        k=ss((t-(TOTAL-2.2))/2.2); im=im.filter(ImageFilter.GaussianBlur(10*k)); im=Image.blend(im,Image.new("RGBA",(W,H),(255,236,210,255)),k*0.85)
    if n<6: im=Image.blend(im,Image.new("RGBA",(W,H),(0,0,0,255)),1-n/6)
    im.convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
print("frames",N)
