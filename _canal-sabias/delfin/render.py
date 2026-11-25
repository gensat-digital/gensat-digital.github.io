import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(41); tl=Timeline(4); USER="@MateoAdona-q1n"
BG=ocean_bg(); BUB=[(random.uniform(0,W),random.uniform(0,H),random.uniform(8,24),random.uniform(60,150)) for _ in range(24)]
BLUE=(110,165,215); BELLY=(215,232,245)
def dolphin(im,cx,cy,s,t,eye="open",tilt=0):
    d=ImageDraw.Draw(im); sw=math.sin(t*3)*18*s
    # cola
    tx,ty=cx-330*s,cy+10*s+sw
    d.polygon([(tx+40*s,ty),(tx-90*s,ty-80*s),(tx-60*s,ty),(tx-90*s,ty+80*s)],fill=BLUE,outline=OUT); d.line([(tx+40*s,ty),(tx-90*s,ty-80*s),(tx-60*s,ty),(tx-90*s,ty+80*s),(tx+40*s,ty)],fill=OUT,width=7)
    # aleta dorsal
    d.polygon([(cx-40*s,cy-110*s),(cx-120*s,cy-230*s),(cx+60*s,cy-115*s)],fill=BLUE,outline=OUT); d.line([(cx-40*s,cy-110*s),(cx-120*s,cy-230*s),(cx+60*s,cy-115*s)],fill=OUT,width=7)
    # cuerpo
    d.ellipse([cx-340*s,cy-130*s+sw*0.3,cx+260*s,cy+130*s],fill=OUT); d.ellipse([cx-330*s,cy-120*s+sw*0.3,cx+250*s,cy+120*s],fill=BLUE)
    d.chord([cx-300*s,cy-40*s,cx+240*s,cy+118*s],0,180,fill=BELLY)
    # cabeza y hocico
    d.ellipse([cx+120*s,cy-120*s,cx+340*s,cy+100*s],fill=OUT); d.ellipse([cx+128*s,cy-112*s,cx+332*s,cy+92*s],fill=BLUE)
    d.rounded_rectangle([cx+280*s,cy+10*s,cx+430*s,cy+70*s],int(30*s),fill=BLUE,outline=OUT,width=7)
    d.chord([cx+200*s,cy+20*s,cx+420*s,cy+92*s],0,180,fill=BELLY)
    d.arc([cx+250*s,cy+20*s,cx+400*s,cy+70*s],20,150,fill=OUT,width=6)
    d.ellipse([cx+160*s,cy-100*s,cx+190*s,cy-86*s],fill=OUT)  # espiraculo
    ex,ey=cx+235*s,cy-35*s
    if eye=="closed": d.arc([ex-28*s,ey-12*s,ex+28*s,ey+20*s],200,340,fill=OUT,width=8)
    else:
        d.ellipse([ex-30*s,ey-34*s,ex+30*s,ey+34*s],fill="white",outline=OUT,width=6); d.ellipse([ex-12*s,ey-16*s,ex+20*s,ey+22*s],fill=(30,20,40)); d.ellipse([ex-4*s,ey-10*s,ex+6*s,ey],fill="white")
    d.ellipse([ex-10*s,ey+38*s,ex+40*s,ey+58*s],fill=(240,150,170))
    # aleta pectoral
    d.polygon([(cx+60*s,cy+50*s),(cx-20*s,cy+170*s),(cx+120*s,cy+80*s)],fill=BLUE,outline=OUT); d.line([(cx+60*s,cy+50*s),(cx-20*s,cy+170*s),(cx+120*s,cy+80*s)],fill=OUT,width=6)
def brain(d,cx,cy,s,sleep_left,t):
    for half,(x0,x1) in enumerate([(cx-170*s,cx),(cx,cx+170*s)]):
        asleep=(half==0)==sleep_left
        col=(170,150,190) if asleep else (255,160,190)
        for k in range(4):
            bx=x0+(x1-x0)*(k%2+0.5)/2; by=cy-60*s+(k//2)*90*s
            d.ellipse([bx-70*s,by-55*s,bx+70*s,by+55*s],fill=col,outline=OUT,width=6)
        if asleep:
            for k in range(3):
                ph=(t*0.7+k*0.33)%1; label(d,"z",(x0+x1)/2+ph*40-20,cy-150*s-ph*60,int(56+36*ph),fill="white")
        else: label(d,"¡alerta!",(x0+x1)/2,cy+150*s,56,fill=(255,214,60))
    d.line([(cx,cy-140*s),(cx,cy+110*s)],fill=OUT,width=8)
def note(d,x,y,s,col=(255,214,60)):
    d.ellipse([x-22*s,y-16*s,x+22*s,y+16*s],fill=col,outline=OUT,width=5); d.line([(x+18*s,y),(x+18*s,y-80*s)],fill=OUT,width=7); d.polygon([(x+18*s,y-80*s),(x+50*s,y-60*s),(x+18*s,y-55*s)],fill=OUT)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_med=tl.wt("medio",0); t_ojo=tl.wt("ojo",1); t_sil=tl.wt("silbido",2); t_nom=tl.wt("nombre",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v in BUB: y=(y0-t*v)%H; xx=x+12*math.sin(t*2+y0); d.ellipse([xx-r,y-r,xx+r,y+r],outline=(255,255,255,150),width=4)
    seaweed(d,70,t,520,(70,190,110),0); seaweed(d,1000,t,560,(70,190,110),2.1)
    blink=((t+0.7)%3.3)<0.13; bob=14*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        dolphin(im,470,1050+bob,max(0.01,0.95*pop) if t<0.8 else 0.95,t,eye="closed" if blink else "open"); d=ImageDraw.Draw(im,"RGBA")
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_med:
            a=min(1.1,back((t-t_med)/0.4)); label(d,"¡Medio cerebro despierto!",540,520,int(66*a),fill=(255,214,60))
    elif i==1:
        label(d,"Una mitad duerme,",540,300,80); label(d,"¡la otra vigila!",540,410,90,fill=(255,214,60))
        sleep_left=(lt%3.0)<1.5
        dolphin(im,470,1230+bob,0.8,t,eye="open" if not sleep_left else ("closed" if blink else "open")); d=ImageDraw.Draw(im,"RGBA")
        brain(d,540,880,1.5,sleep_left,t)
        if t>t_ojo:
            a=min(1.1,back((t-t_ojo)/0.4)); label(d,"¡un ojo abierto!",760,1480,int(54*a),fill="white")
    elif i==2:
        label(d,"Cada uno tiene",540,300,84); label(d,"¡su propio silbido!",540,410,88,fill=(255,214,60))
        dolphin(im,430,1080+bob,0.85,t,eye="closed" if blink else "open"); d=ImageDraw.Draw(im,"RGBA")
        if t>t_sil-0.3:
            for k in range(3):
                ph=((t-t_sil)*0.8+k*0.33)%1; r=80+ph*260
                d.arc([800-r,1080-r,800+r,1080+r],-50,50,fill=(255,255,255,int(255*(1-ph))),width=10)
            for k in range(3): note(d,830+k*80,900-k*60+15*math.sin(t*4+k),0.9)
        if t>t_nom:
            a=min(1.1,back((t-t_nom)/0.4)); w=360*a
            d.rounded_rectangle([540-w/2,600-60*a,540+w/2,600+60*a],40,fill="white",outline=OUT,width=8); label(d,"= su nombre",540,600,int(56*a),fill=(255,90,150))
    else:
        dolphin(im,470,1200+bob,0.8,t,eye="closed" if blink else "open"); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_med,"boing",0.45),(tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.3,"bubbles",0.3),(t_ojo,"ding",0.45),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_sil,"whistle",0.55),(t_nom,"twinkle",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_delfin.mp4"); print("ok",round(tl.TOTAL,1))
