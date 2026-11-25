import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(21); tl=Timeline(4)
USER="@temmie1i3"
def grad(top,bot):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H; d.line([(0,y),(W,y)],fill=mix(top,bot,a))
    return im.convert("RGBA")
SPACE=grad((24,16,70),(70,40,120)); WATER=grad((150,230,220),(60,160,190)); DRY=grad((255,214,150),(225,160,100))
dd=ImageDraw.Draw(SPACE); dd.ellipse([700,1250,1000,1550],fill=(80,160,255),outline=OUT,width=8); dd.ellipse([760,1300,880,1400],fill=(110,200,120)); dd.ellipse([880,1420,960,1500],fill=(110,200,120))
dd=ImageDraw.Draw(DRY)
for k in range(14):
    x=random.uniform(0,W); y=random.uniform(1150,1500); dd.line([(x,y),(x+random.uniform(-80,80),y+random.uniform(20,60)),(x+random.uniform(-80,80),y+random.uniform(60,120))],fill=(190,120,70),width=6)
STARS=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,5),random.uniform(0,6)) for _ in range(70)]
BUB=[(random.uniform(0,W),random.uniform(0,H),random.uniform(8,20),random.uniform(40,100)) for _ in range(20)]
SK=(255,214,190); SK_D=(232,176,150)
def tardi(im,cx,cy,s,t,closed=False,ball=0,helmet=False,wave=False,legs_lbl=0):
    d=ImageDraw.Draw(im)
    if ball>0.98:
        d.ellipse([cx-150*s,cy-120*s,cx+150*s,cy+120*s],fill=SK_D,outline=OUT,width=8)
        for k in range(3): d.arc([cx-150*s+k*60*s,cy-120*s,cx-30*s+k*60*s,cy+120*s],290,70,fill=(210,150,125),width=6)
        d.arc([cx-90*s,cy-30*s,cx-40*s,cy+10*s],200,340,fill=OUT,width=7); return
    sq=1-0.5*ball
    L=[(-170,0),(-60,0),(50,0),(160,0)]
    for k,(lx,_) in enumerate(L):  # patas de atras
        x=cx+lx*s*sq+30*s; y=cy+90*s*sq+8*math.sin(t*8+k)
        d.rounded_rectangle([x-30*s,y-20*s,x+30*s,y+80*s*sq],int(26*s),fill=SK_D,outline=OUT,width=6)
    d.rounded_rectangle([cx-300*s*sq,cy-130*s*sq,cx+290*s*sq,cy+130*s*sq],int(130*s*sq),fill=SK,outline=OUT,width=9)
    for k in range(1,5):
        x=cx-260*s*sq+k*110*s*sq; d.arc([x-30*s,cy-128*s*sq,x+30*s,cy+128*s*sq],280,80,fill=SK_D,width=6)
    for k,(lx,_) in enumerate(L):  # patas de adelante
        x=cx+lx*s*sq; y=cy+100*s*sq+8*math.sin(t*8+k+1)+(-40*s*math.sin(t*10)*(1 if wave and k==0 else 0))
        d.rounded_rectangle([x-32*s,y-20*s,x+32*s,y+90*s*sq],int(28*s),fill=SK,outline=OUT,width=6)
        for c in (-14,0,14): d.line([(x+c*s,y+88*s*sq),(x+c*s-6*s,y+108*s*sq)],fill=OUT,width=5)
        if legs_lbl>k:
            a=min(1.15,back((legs_lbl-k)/1.0)); label(d,str(k*2+1)+"·"+str(k*2+2),x,y+150*s,int(40*a),fill=(255,214,60))
    hx,hy=cx-250*s*sq,cy-20*s
    d.ellipse([hx-60*s,hy-40*s,hx+10*s,hy+40*s],fill=SK,outline=OUT,width=7); d.ellipse([hx-48*s,hy-16*s,hx-18*s,hy+16*s],fill=(200,120,120),outline=OUT,width=5)
    for ex in (-150,-80):
        x,y=cx+ex*s*sq,cy-50*s
        if closed: d.arc([x-18*s,y-8*s,x+18*s,y+14*s],200,340,fill=OUT,width=7)
        else: d.ellipse([x-18*s,y-20*s,x+18*s,y+20*s],fill=(30,20,40)); d.ellipse([x-8*s,y-12*s,x,y-4*s],fill="white")
    d.ellipse([cx-150*s,cy-5*s,cx-100*s,cy+20*s],fill=(255,160,160)); d.ellipse([cx-60*s,cy-5*s,cx-10*s,cy+20*s],fill=(255,160,160))
    d.arc([cx-120*s,cy,cx-50*s,cy+40*s],20,160,fill=OUT,width=6)
    if helmet:
        hl=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hl)
        hd.ellipse([cx-340*s,cy-260*s,cx+340*s,cy+260*s],fill=(200,240,255,55),outline=(230,250,255,220),width=10)
        hd.arc([cx-280*s,cy-220*s,cx-80*s,cy-40*s],200,260,fill=(255,255,255,200),width=14)
        im.alpha_composite(hl)
def lens(im,cx,cy,r):
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255); return m
def waterdrop(d,x,y,s):
    d.polygon([(x,y-s*1.2),(x-s*0.78,y+s*0.05),(x+s*0.78,y+s*0.05)],fill=OUT); d.ellipse([x-s*0.86,y-s*0.5,x+s*0.86,y+s*1.0],fill=OUT)
    d.polygon([(x,y-s*1.08),(x-s*0.68,y+s*0.05),(x+s*0.68,y+s*0.05)],fill=(90,180,255)); d.ellipse([x-s*0.76,y-s*0.42,x+s*0.76,y+s*0.9],fill=(90,180,255)); d.ellipse([x-s*0.4,y-s*0.1,x-s*0.15,y+s*0.25],fill="white")
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_esp=tl.wt("espacio",0); t_ocho=tl.wt("ocho",1); t_bol=tl.wt("bolita",2); t_agua=tl.wt("agua",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    blink=((t+0.7)%3.3)<0.13; bob=12*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        im=SPACE.copy(); d=ImageDraw.Draw(im,"RGBA")
        for x,y,r,ph in STARS: d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,230,int(140+110*math.sin(t*3+ph))))
        tardi(im,540,950+bob,max(0.01,0.9*pop) if t<0.8 else 0.9,t,closed=blink,helmet=t>t_esp-0.2); d=ImageDraw.Draw(im,"RGBA")
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_esp:
            a=min(1.1,back((t-t_esp)/0.4)); label(d,"¡Sobrevivió al espacio!",540,520,int(76*a),fill=(255,214,60))
    elif i==1:
        im=WATER.copy(); d=ImageDraw.Draw(im,"RGBA")
        for x,y0,r,v in BUB: y=(y0-t*v)%H; d.ellipse([x-r,y-r,x+r,y+r],outline=(255,255,255,150),width=4)
        label(d,"Osito de agua",540,300,100,fill=(255,214,60)); label(d,"solo se ve con microscopio",540,410,58)
        k=back((lt-0.2)/0.5); R=int(420*min(k,1.05))
        if R>10:
            inner=WATER.copy(); tardi(inner,540,1000+bob,0.95,t,closed=blink)
            im.paste(inner,(0,0),lens(im,540,1000,R)); d=ImageDraw.Draw(im,"RGBA")
            d.ellipse([540-R-14,1000-R-14,540+R+14,1000+R+14],outline=OUT,width=28); d.ellipse([540-R-6,1000-R-6,540+R+6,1000+R+6],outline=(200,210,220),width=12)
        if t>t_ocho:
            a=min(1.1,back((t-t_ocho)/0.4)); label(d,"¡8 patitas!",820,560,int(70*a),fill=(255,120,170))
    elif i==2:
        wet=ease((t-t_agua+0.2)/0.6) if t>t_agua-0.2 else 0
        im=Image.blend(DRY,WATER,wet); d=ImageDraw.Draw(im,"RGBA")
        label(d,"Se seca...",540,300,100,fill=(255,214,60)); label(d,"¡y revive con agua!",540,410,70)
        ball=ease((t-t_bol+0.6)/0.7) if t<t_agua else 1-ease((t-t_agua-0.4)/0.7)
        if ball>0.98: tardi(im,540,1050,0.95,t,ball=1)
        else: tardi(im,540,1050+bob,0.95,t,closed=ball>0.2 or blink,ball=ball)
        d=ImageDraw.Draw(im,"RGBA")
        if t_bol<t<t_agua: label(d,"años...",820,820,60)
        if t>t_agua-0.6 and wet<1: waterdrop(d,540,560+ease((t-t_agua+0.6)/0.6)*380,70)
        if wet>=1 and t<t_agua+1.6:
            for k in range(8): ang=k*0.785; r=200+80*ease(t-t_agua); sparkle(d,540+r*math.cos(ang),1050+r*math.sin(ang),18)
    else:
        im=WATER.copy(); d=ImageDraw.Draw(im,"RGBA")
        tardi(im,540,1150+bob,0.9,t,closed=blink,wave=True); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_esp,"twinkle",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.2,"bubbles",0.35),(t_ocho,"boing",0.45),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_bol,"pop",0.5),(t_agua,"bubbles",0.45),(t_agua+0.4,"ding",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_tardigrado.mp4"); print("ok",round(tl.TOTAL,1))
