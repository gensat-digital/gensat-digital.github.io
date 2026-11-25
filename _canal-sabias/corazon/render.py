import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(33); tl=Timeline(4)
def grad(top,bot):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix(top,bot,y/H))
    return im.convert("RGBA")
BG=grad((255,214,220),(250,150,170))
CELLS=[(random.uniform(0,W),random.uniform(0,H),random.uniform(18,34),random.uniform(30,90),random.uniform(0,6)) for _ in range(22)]
RED=(232,64,90); RED_D=(190,40,70)
def bpm_scale(t): ph=(t*1.2)%1; return 1+0.09*math.exp(-((ph-0.05)/0.06)**2)+0.05*math.exp(-((ph-0.25)/0.06)**2)
def heart_char(im,cx,cy,s,t,blink=False,wave=False):
    d=ImageDraw.Draw(im); k=bpm_scale(t); S=s*k
    for side in (-1,1):  # bracitos
        a=(-0.9+0.5*math.sin(t*10)) if (wave and side>0) else 0.35*side*0+0.2
        x1,y1=cx+side*230*S,cy-10*S; x2,y2=x1+side*110*s,y1+(-120*s if (wave and side>0) else 60*s)+ (25*s*math.sin(t*10) if (wave and side>0) else 0)
        d.line([(x1,y1),(x2,y2)],fill=OUT,width=int(40*s)); d.line([(x1,y1),(x2,y2)],fill=RED,width=int(28*s)); d.ellipse([x2-24*s,y2-24*s,x2+24*s,y2+24*s],fill=RED,outline=OUT,width=6)
    for side in (-1,1):
        x=cx+side*45*s; d.line([(x,cy+200*S),(x,cy+360*s)],fill=OUT,width=int(36*s)); d.line([(x,cy+200*S),(x,cy+360*s)],fill=RED_D,width=int(24*s)); d.ellipse([x-38*s,cy+340*s,x+38*s,cy+380*s],fill=(120,40,60),outline=OUT,width=6)
    heart(d,cx,cy,520*S,RED,OUT)
    d.ellipse([cx-150*S,cy-200*S,cx-70*S,cy-130*S],fill=(255,150,170))
    for side in (-1,1):
        ex,ey=cx+side*85*S,cy-40*S
        if blink: d.arc([ex-36*S,ey-14*S,ex+36*S,ey+24*S],200,340,fill=OUT,width=9)
        else:
            d.ellipse([ex-40*S,ey-46*S,ex+40*S,ey+46*S],fill="white",outline=OUT,width=6); d.ellipse([ex-22*S,ey-20*S,ex+22*S,ey+28*S],fill=(30,20,40)); d.ellipse([ex-12*S,ey-14*S,ex+2*S,ey],fill="white")
        d.ellipse([ex+side*30*S-24*S,ey+52*S-11*S,ex+side*30*S+24*S,ey+52*S+11*S],fill=(255,150,170))
    d.chord([cx-50*S,cy+40*S,cx+50*S,cy+110*S],10,170,fill=(120,30,50),outline=OUT,width=6)
def cell(d,x,y,r,rot):
    d.ellipse([x-r,y-r*0.75,x+r,y+r*0.75],fill=(220,50,70),outline=(150,30,50),width=4); d.ellipse([x-r*0.5,y-r*0.3,x+r*0.5,y+r*0.3],fill=(190,40,60))
def num_fmt(v): return f"{int(v):,}"
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_cien=tl.wt("cien",0); t_dos=tl.wt("dos",2)
PATHS=[[(540,1000),(300,800),(120,520)],[(540,1000),(800,780),(960,500)],[(540,1000),(260,1250),(100,1500)],[(540,1000),(840,1260),(990,1520)]]
def along(p,f):
    seg=f*(len(p)-1); k=min(int(seg),len(p)-2); u=seg-k; return (p[k][0]+(p[k+1][0]-p[k][0])*u,p[k][1]+(p[k+1][1]-p[k][1])*u)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v,ph in CELLS: y=(y0-t*v)%H; d.ellipse([x-r,y-r*0.75,x+r,y+r*0.75],fill=(255,255,255,70))
    blink=((t+0.7)%3.3)<0.13; pop=back((t-0.15)/0.5)
    if i==0:
        heart_char(im,540,1000,max(0.01,0.95*pop) if t<0.8 else 0.95,t,blink); d=ImageDraw.Draw(im,"RGBA")
        title_sabias(d,t)
        if t>t_cien:
            a=min(1.1,back((t-t_cien)/0.4)); label(d,num_fmt(100000*ease((t-t_cien)/1.2)),540,520,int(150*a),fill=(255,255,255),stroke=RED_D)
            label(d,"latidos al día",540,640,int(64*min(a,1)),fill=(255,214,60))
    elif i==1:
        label(d,"¡Sangre a",540,300,100); label(d,"todo el cuerpo!",540,420,100,fill=(255,214,60))
        for p in PATHS:
            d.line(p,fill=(150,30,50),width=46,joint="curve"); d.line(p,fill=(250,120,140),width=30,joint="curve")
            for k in range(4):
                f=((t*0.45+k/4)%1); x,y=along(p,f); cell(d,x,y,22,0)
        heart_char(im,540,1000,0.7,t,blink); d=ImageDraw.Draw(im,"RGBA")
        if lt>1.2: label(d,"¡en automático!",540,1450,60,fill="white")
    elif i==2:
        heart_char(im,540,1080,0.8,t,blink); d=ImageDraw.Draw(im,"RGBA")
        label(d,"En toda una vida...",540,300,80,fill=(255,214,60))
        if t>t_dos:
            k=ease((t-t_dos)/1.6); a=min(1.1,back((t-t_dos)/0.4))
            label(d,num_fmt(2500000000*k),540,470,int(118*a),fill=(255,255,255),stroke=RED_D); label(d,"¡latidos!",540,590,int(70*min(a,1)),fill=(255,214,60))
            if k>0.95:
                for j in range(8): ang=j*0.785+t; sparkle(d,540+330*math.cos(ang),1080+330*math.sin(ang),20)
    else:
        heart_char(im,540,1120,0.75,t,blink,wave=True); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
beats=[(x/1.2+0.04,"beat",0.35) for x in range(1,int(tl.SC[0][1]*1.2))]
fx=beats+[(0.15,"pop",0.5),(t_cien,"ding",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.3,"bubbles",0.3),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_dos,"twinkle",0.5),(t_dos+1.6,"ding",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_corazon.mp4"); print("ok",round(tl.TOTAL,1))
