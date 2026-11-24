import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(5); tl=Timeline(4)
USER="@laslozanoleon"
def make_bg(night=False):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/1200
        c=(int(40+20*a),int(50+30*a),int(110+40*a)) if night else (int(140-30*a),int(215-15*a),int(250-10*a))
        d.line([(0,y),(W,y)],fill=c)
    if night:
        d.ellipse([780,160,940,320],fill=(255,245,200)); d.ellipse([830,140,990,300],fill=c)
    else:
        d.ellipse([800,150,960,310],fill=(255,230,120))
    g1=(70,120,80) if night else (120,200,100); g2=(60,105,70) if night else (100,180,85)
    d.ellipse([-300,1000,800,1500],fill=g1,outline=OUT,width=8); d.ellipse([400,1040,1400,1500],fill=g2,outline=OUT,width=8)
    d.rectangle([0,1300,W,H],fill=g2)
    fc=(150,110,80) if night else (200,150,100)
    for x in range(40,W,170): d.rectangle([x,1150,x+24,1300],fill=fc,outline=OUT,width=5)
    d.rectangle([0,1180,W,1200],fill=fc,outline=OUT,width=4); d.rectangle([0,1240,W,1260],fill=fc,outline=OUT,width=4)
    for x,y in [(200,1420),(860,1460),(520,1500)]:
        for k in range(5): d.ellipse([x+math.cos(k*1.26)*22-14,y+math.sin(k*1.26)*22-14,x+math.cos(k*1.26)*22+14,y+math.sin(k*1.26)*22+14],fill=(255,240,250) if not night else (200,200,220))
        d.ellipse([x-10,y-10,x+10,y+10],fill=(255,210,80))
    return im.convert("RGBA")
DAY=make_bg(False); NIGHT=make_bg(True)
STARS=[(random.uniform(0,W),random.uniform(0,900),random.uniform(2,5),random.uniform(0,6)) for _ in range(60)]
COAT=(196,128,78); MANE=(92,56,36); MUZ=(230,180,140)
def horse(im,cx,cy,s,t,pose="stand",closed=False,blink=False,locks=0):
    d=ImageDraw.Draw(im)
    if pose=="stand":
        legs=[(-150,0),(-80,0),(110,0),(180,0)]
        for k,(lx,_) in enumerate(legs):
            x=cx+lx*s; d.rounded_rectangle([x-26*s,cy+40*s,x+26*s,cy+300*s],int(22*s),fill=COAT if k in (0,3) else (176,112,66),outline=OUT,width=7)
            d.rounded_rectangle([x-30*s,cy+270*s,x+30*s,cy+310*s],int(10*s),fill=(70,50,45),outline=OUT,width=6)
        tail_y=cy-40*s
        d.polygon([(cx-240*s,tail_y),(cx-330*s,tail_y+80*s+20*s*math.sin(t*3)),(cx-300*s,tail_y+200*s),(cx-220*s,tail_y+60*s)],fill=MANE,outline=OUT)
        d.ellipse([cx-260*s,cy-120*s,cx+260*s,cy+110*s],fill=COAT,outline=OUT,width=9)
        nb=[(cx+150*s,cy-60*s),(cx+230*s,cy-300*s),(cx+330*s,cy-290*s),(cx+250*s,cy-20*s)]
        d.polygon(nb,fill=COAT,outline=OUT); d.line(nb+[nb[0]],fill=OUT,width=8)
        hx,hy=cx+300*s,cy-330*s; head_ang=0
        if locks>0:
            for k,(lx,_) in enumerate(legs):
                a=min(1.15,back(locks-k*0.12))
                if a>0.05:
                    x=cx+lx*s; y=cy+170*s; r=26*s*a
                    d.arc([x-r*0.7,y-r*1.6,x+r*0.7,y-r*0.2],180,360,fill=(255,214,60),width=int(8*s*a)+2)
                    d.rounded_rectangle([x-r,y-r*0.6,x+r,y+r],int(6*s),fill=(255,214,60),outline=OUT,width=5)
    else:  # acostado
        d.polygon([(cx-240*s,cy+20*s),(cx-340*s,cy+90*s),(cx-260*s,cy+120*s)],fill=MANE,outline=OUT)
        for lx in (-120,60):
            d.rounded_rectangle([cx+lx*s-20*s,cy+70*s,cx+lx*s+150*s,cy+120*s],int(22*s),fill=(176,112,66),outline=OUT,width=7)
        d.ellipse([cx-260*s,cy-110*s,cx+260*s,cy+120*s],fill=COAT,outline=OUT,width=9)
        nb=[(cx+150*s,cy-50*s),(cx+260*s,cy-130*s),(cx+340*s,cy-90*s),(cx+250*s,cy+10*s)]
        d.polygon(nb,fill=COAT,outline=OUT); d.line(nb+[nb[0]],fill=OUT,width=8)
        hx,hy=cx+330*s,cy-150*s
    # cabeza
    d.ellipse([hx-90*s,hy-85*s,hx+90*s,hy+85*s],fill=COAT,outline=OUT,width=8)
    d.ellipse([hx+30*s,hy-10*s,hx+190*s,hy+110*s],fill=MUZ,outline=OUT,width=8)
    d.ellipse([hx+120*s,hy+30*s,hx+140*s,hy+50*s],fill=OUT)
    d.arc([hx+70*s,hy+50*s,hx+160*s,hy+95*s],20,160,fill=OUT,width=6)
    for ex in (-40,10): d.polygon([(hx+ex*s,hy-70*s),(hx+(ex+25)*s,hy-150*s),(hx+(ex+50)*s,hy-60*s)],fill=COAT,outline=OUT)
    d.polygon([(hx-90*s,hy-60*s),(hx-30*s,hy-95*s),(hx+20*s,hy-80*s),(hx-40*s,hy-20*s),(hx-110*s,hy+60*s)],fill=MANE,outline=OUT)
    ex,ey=hx+10*s,hy-10*s
    if closed or blink: d.arc([ex-28*s,ey-12*s,ex+28*s,ey+20*s],200,340,fill=OUT,width=8)
    else:
        d.ellipse([ex-30*s,ey-36*s,ex+30*s,ey+36*s],fill="white",outline=OUT,width=6); d.ellipse([ex-14*s,ey-16*s,ex+18*s,ey+22*s],fill=(30,20,40)); d.ellipse([ex-6*s,ey-10*s,ex+4*s,ey],fill="white")
    d.ellipse([ex+20*s,ey+30*s,ex+60*s,ey+50*s],fill=(240,140,140))
    return hx,hy
def zzz(d,x,y,t):
    for k in range(3):
        ph=(t*0.6+k*0.33)%1; label(d,"Z",x+ph*80+k*10,y-ph*220,int(50+40*ph),fill=(255,255,255))
def dream(d,x,y,s,t):
    for k,(dx,dy,r) in enumerate([(-150,140,18),(-110,90,28)]): d.ellipse([x+dx-r,y+dy-r,x+dx+r,y+dy+r],fill="white",outline=OUT,width=5)
    d.ellipse([x-160*s,y-120*s,x+160*s,y+80*s],fill="white",outline=OUT,width=8)
    cx,cy=x-40*s,y-20*s; d.polygon([(cx-20*s,cy-60*s),(cx+20*s,cy-60*s),(cx+5*s,cy+70*s)],fill=(255,140,40),outline=OUT)
    for k in (-1,0,1): d.ellipse([cx+k*14*s-10*s,cy-95*s,cx+k*14*s+10*s,cy-55*s],fill=(90,190,90))
    ax,ay=x+60*s,y-15*s; d.ellipse([ax-45*s,ay-42*s,ax+45*s,ay+45*s],fill=(235,60,70),outline=OUT,width=6); d.line([(ax,ay-42*s),(ax+8*s,ay-70*s)],fill=OUT,width=6)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_pie=tl.wt("pie",0); t_tra=tl.wt("trabadas",1); t_ac=tl.wt("acostarse",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    nk=ease((lt-0.1)/0.8) if i==2 else 0
    im=DAY.copy() if i!=2 else Image.blend(DAY,NIGHT,nk)
    d=ImageDraw.Draw(im,"RGBA")
    if i==2 and nk>0.3:
        for x,y,r,ph in STARS: a=int(nk*(140+110*math.sin(t*3+ph))); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,230,a))
    blink=((t+0.7)%3.3)<0.13; bob=6*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        horse(im,420,980+bob,max(0.01,0.95*pop) if t<0.8 else 0.95,t,blink=blink); d=ImageDraw.Draw(im,"RGBA")
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_pie:
            a=min(1.1,back((t-t_pie)/0.4)); label(d,"¡Duerme de pie!",540,500,int(90*a),fill=(255,214,60))
    elif i==1:
        label(d,"Sus patas se",540,300,90); label(d,"¡TRABAN!",540,420,130,fill=(255,214,60))
        horse(im,420,980+bob,0.95,t,closed=True,locks=(t-t_tra)/0.5 if t>t_tra-0.1 else 0); d=ImageDraw.Draw(im,"RGBA")
        zzz(d,820,620,t)
    elif i==2:
        label(d,"Para soñar...",540,300,96,fill=(255,214,60)); label(d,"¡se acuesta!",540,420,110)
        if t<t_ac:
            horse(im,420,980+bob,0.95,t,closed=True); d=ImageDraw.Draw(im,"RGBA"); zzz(d,820,620,t)
        else:
            hx,hy=horse(im,420,1180,0.95,t,pose="lie",closed=True); d=ImageDraw.Draw(im,"RGBA")
            a=back((t-t_ac-0.3)/0.5)
            if a>0: dream(d,760,720,min(a,1.1),t)
            zzz(d,hx+60,hy-80,t)
    else:
        horse(im,400,1130+bob,0.85,t,blink=blink); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_pie,"boing",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(t_tra,"ding",0.5),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_ac,"boing",0.4),(t_ac+0.4,"twinkle",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_caballo.mp4"); print("ok",round(tl.TOTAL,1))
