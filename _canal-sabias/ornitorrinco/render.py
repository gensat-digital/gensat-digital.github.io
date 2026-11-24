import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(11); tl=Timeline(4)
USER="@martinaurcia6363"
def make_bg():
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        if y<1020: a=y/1020; c=(int(150-40*a),int(220-20*a),int(250-10*a))
        else: a=(y-1020)/(H-1020); c=(int(70-40*a),int(170-70*a),int(220-60*a))
        d.line([(0,y),(W,y)],fill=c)
    d.ellipse([-200,860,700,1140],fill=(120,200,100),outline=OUT,width=8); d.ellipse([500,900,1300,1150],fill=(110,190,95),outline=OUT,width=8)
    d.rectangle([0,1030,W,1080],fill=(80,175,225))
    for x in range(0,W,90): d.arc([x,1010,x+90,1060],200,340,fill=(220,245,255),width=6)
    d.ellipse([820,140,980,300],fill=(255,230,120))
    for x,y in [(150,250),(300,180),(700,300)]: d.ellipse([x,y,x+180,y+70],fill="white"); d.ellipse([x+40,y-35,x+130,y+40],fill="white")
    return im.convert("RGBA")
BG=make_bg()
BUB=[(random.uniform(0,W),random.uniform(1100,H),random.uniform(8,22),random.uniform(50,120)) for _ in range(18)]
FUR=(150,98,64); FUR_D=(118,74,48); BILL=(80,84,104)
def platypus(im,cx,cy,s,t,closed=False,blink=False,wag=0):
    d=ImageDraw.Draw(im)
    tw=math.sin(t*3)*0.1+wag
    tx=cx-300*s; d.ellipse([tx-150*s,cy-60*s+tw*60,tx+90*s,cy+70*s+tw*60],fill=FUR_D,outline=OUT,width=8)
    for k in range(4): d.line([(tx-120*s+k*45*s,cy-45*s+tw*60),(tx-100*s+k*45*s,cy+55*s+tw*60)],fill=(95,58,38),width=5)
    for fx in (-120,90):
        d.ellipse([cx+fx*s-50*s,cy+95*s,cx+fx*s+50*s,cy+140*s],fill=(70,55,50),outline=OUT,width=6)
    d.ellipse([cx-250*s,cy-130*s,cx+230*s,cy+130*s],fill=FUR,outline=OUT,width=9)
    d.ellipse([cx-150*s,cy-10*s,cx+120*s,cy+110*s],fill=(186,134,96))
    hx,hy=cx+230*s,cy-50*s
    d.ellipse([hx-120*s,hy-115*s,hx+120*s,hy+115*s],fill=FUR,outline=OUT,width=9)
    d.rounded_rectangle([hx+60*s,hy-10*s,hx+300*s,hy+80*s],int(45*s),fill=BILL,outline=OUT,width=9)
    d.ellipse([hx+240*s,hy+5*s,hx+256*s,hy+21*s],fill=OUT); d.arc([hx+90*s,hy+30*s,hx+230*s,hy+80*s],10,170,fill=(150,155,175),width=6)
    ex,ey=hx+10*s,hy-40*s
    if closed or blink: d.arc([ex-30*s,ey-14*s,ex+30*s,ey+22*s],200,340,fill=OUT,width=9)
    else:
        d.ellipse([ex-34*s,ey-40*s,ex+34*s,ey+40*s],fill="white",outline=OUT,width=6); d.ellipse([ex-16*s,ey-18*s,ex+20*s,ey+24*s],fill=(30,20,40)); d.ellipse([ex-8*s,ey-12*s,ex+4*s,ey],fill="white")
    d.ellipse([ex-60*s,ey+40*s,ex-10*s,ey+64*s],fill=(240,150,150))
def egg(d,x,y,s,crack=0,baby=0,t=0):
    if baby>0:
        by=y-60*s*baby; d.ellipse([x-55*s,by-55*s,x+55*s,by+55*s],fill=FUR,outline=OUT,width=6)
        d.rounded_rectangle([x+20*s,by-5*s,x+105*s,by+30*s],int(15*s),fill=BILL,outline=OUT,width=5)
        d.ellipse([x-8*s,by-25*s,x+12*s,by-5*s],fill=(30,20,40))
    d.ellipse([x-80*s,y-105*s,x+80*s,y+95*s],fill=(255,244,220),outline=OUT,width=8)
    for sx,sy,r in [(-30,-40,12),(25,-10,9),(-10,40,10),(35,45,7)]: d.ellipse([x+sx*s-r*s,y+sy*s-r*s,x+sx*s+r*s,y+sy*s+r*s],fill=(232,210,170))
    if crack>0:
        pts=[(x-75*s,y-20*s),(x-40*s,y-45*s),(x-10*s,y-15*s),(x+25*s,y-50*s),(x+55*s,y-20*s),(x+78*s,y-35*s)]
        n=max(2,int(len(pts)*min(1,crack))); d.line(pts[:n],fill=OUT,width=7)
def shrimp(d,x,y,s,t):
    y+=10*math.sin(t*4)
    for k in range(4): d.ellipse([x-k*28*s-30*s,y-25*s+k*6*s,x-k*28*s+30*s,y+25*s+k*6*s],fill=(255,150,120),outline=OUT,width=5)
    d.ellipse([x+12*s,y-14*s,x+24*s,y-2*s],fill=OUT); d.line([(x+20*s,y-20*s),(x+70*s,y-60*s)],fill=OUT,width=4); d.line([(x+20*s,y-15*s),(x+80*s,y-30*s)],fill=OUT,width=4)
def zap(d,a,b,t,col=(255,240,90)):
    pts=[a]; n=7
    for k in range(1,n):
        f=k/n; pts.append((a[0]+(b[0]-a[0])*f+random.uniform(-22,22),a[1]+(b[1]-a[1])*f+random.uniform(-22,22)))
    pts.append(b); d.line(pts,fill=OUT,width=16); d.line(pts,fill=col,width=8)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_hue=tl.wt("huevos",0)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t); random.seed(n//3)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v in BUB:
        y=1100+((y0-1100-t*v)%(H-1100)); d.ellipse([x-r,y-r,x+r,y+r],outline=(255,255,255,140),width=4)
    blink=((t+0.7)%3.3)<0.13; bob=10*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        platypus(im,470,860+bob,max(0.01,0.95*pop) if t<0.8 else 0.95,t,blink=blink); d=ImageDraw.Draw(im,"RGBA")
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_hue:
            a=min(1.15,back((t-t_hue)/0.4)); egg(d,900,700,1.0*a)
            label(d,"¡Pone huevos!",540,520,int(84*min(a,1)),fill=(255,214,60))
    elif i==1:
        label(d,"Mamífero",540,300,96,fill=(255,214,60)); label(d,"que nace de un huevo",540,410,64)
        platypus(im,330,890+bob,0.7,t,blink=blink); d=ImageDraw.Draw(im,"RGBA")
        egg(d,800,820,1.15,crack=(lt-0.8)/1.2,baby=ease((lt-2.0)/0.6),t=t)
    elif i==2:
        label(d,"Caza con",540,300,96); label(d,"¡ELECTRICIDAD!",540,420,110,fill=(255,230,80))
        k=ease(lt/0.8); cy=880+420*k
        platypus(im,380,cy+bob,0.75,t,closed=lt>0.9); d=ImageDraw.Draw(im,"RGBA")
        if lt>0.9: label(d,"ojos cerrados",250,cy-210,44)
        if lt>1.3:
            shrimp(d,930,1330,1.6,t)
            if int(t*10)%3!=0: zap(d,(860,1320),(380+0.75*(230+300),cy+bob-0.75*50+25),t)
    else:
        platypus(im,470,1000+bob,0.95,t,blink=blink,wag=0.4*math.sin(t*8)); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_hue,"pop",0.6),(tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.8,"boing",0.4),(tl.SC[1][0]+2.0,"ding",0.5),(tl.SC[2][0]-0.3,"whoosh",0.4),(tl.SC[2][0]+0.4,"bubbles",0.4),(tl.SC[2][0]+1.3,"twinkle",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_ornitorrinco.mp4"); print("ok",round(tl.TOTAL,1))
