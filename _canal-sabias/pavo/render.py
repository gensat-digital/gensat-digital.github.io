import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
def lerp(a,b,k): return a+(b-a)*k
random.seed(61); tl=Timeline(4); USER="@MariaGarcia-jw5jq"; USER2="@constanzadeleon9235"
def make_bg(night=False):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/1300; c=mix((40,40,90),(90,70,130),a) if night else mix((255,210,150),(250,170,110),min(1,a))
        d.line([(0,y),(W,y)],fill=c)
    if night: d.ellipse([780,170,930,320],fill=(255,245,200))
    else: d.ellipse([780,170,950,340],fill=(255,235,150))
    g=(70,100,60) if night else (150,170,80)
    d.ellipse([-300,1180,800,1600],fill=g,outline=OUT,width=8); d.ellipse([400,1220,1400,1600],fill=mix(g,(0,0,0),0.1),outline=OUT,width=8)
    d.rectangle([0,1450,W,H],fill=mix(g,(0,0,0),0.1))
    for x,y,c in [(160,1560,(230,120,60)),(880,1600,(240,170,60)),(520,1680,(200,90,50))]:
        d.polygon([(x,y-30),(x+30,y),(x,y+30),(x-30,y)],fill=c,outline=OUT)
    return im.convert("RGBA")
DAY=make_bg(); NIGHT=make_bg(True)
LEAVES=[(random.uniform(0,W),random.uniform(0,H),random.uniform(0,6),random.choice([(230,120,60),(240,170,60),(200,90,50)])) for _ in range(18)]
BODY=(120,80,55); BODY_D=(95,62,42)
FEATH=[(200,90,50),(240,160,60),(150,95,60),(230,120,60),(255,200,90)]
def turkey(im,cx,cy,s,t,blink=False,snood=(220,50,50),flap=0,mouth="smile"):
    d=ImageDraw.Draw(im)
    for k in range(9):  # cola en abanico
        a=math.radians(200+k*17.5); r=330*s
        p=[(cx,cy-20*s),(cx+r*math.cos(a-0.1),cy-20*s+r*math.sin(a-0.1)),(cx+r*1.05*math.cos(a),cy-20*s+r*1.05*math.sin(a)),(cx+r*math.cos(a+0.1),cy-20*s+r*math.sin(a+0.1))]
        d.polygon(p,fill=FEATH[k%5],outline=OUT); d.line(p+[p[0]],fill=OUT,width=6)
        d.ellipse([cx+r*0.85*math.cos(a)-14*s,cy-20*s+r*0.85*math.sin(a)-14*s,cx+r*0.85*math.cos(a)+14*s,cy-20*s+r*0.85*math.sin(a)+14*s],fill=(255,240,200))
    for side in (-1,1):  # alas
        ang=flap*side
        d.ellipse([cx+side*150*s-90*s,cy+20*s-60*s-ang*80*s,cx+side*150*s+90*s,cy+20*s+90*s-ang*80*s],fill=BODY_D,outline=OUT,width=7)
    for side in (-1,1):
        x=cx+side*55*s; d.line([(x,cy+170*s),(x,cy+260*s)],fill=(230,150,60),width=int(16*s))
        for dx in (-25,0,25): d.line([(x,cy+260*s),(x+dx*s,cy+285*s)],fill=(230,150,60),width=int(10*s))
    d.ellipse([cx-170*s,cy-120*s,cx+170*s,cy+200*s],fill=BODY,outline=OUT,width=8)
    d.ellipse([cx-90*s,cy-20*s,cx+90*s,cy+170*s],fill=(160,110,75))
    hx,hy=cx,cy-190*s
    d.ellipse([hx-90*s,hy-95*s,hx+90*s,hy+85*s],fill=(150,180,210),outline=OUT,width=7)
    for side in (-1,1):
        ex,ey=hx+side*38*s,hy-20*s
        if blink: d.arc([ex-22*s,ey-10*s,ex+22*s,ey+16*s],200,340,fill=OUT,width=7)
        else:
            d.ellipse([ex-25*s,ey-28*s,ex+25*s,ey+28*s],fill="white",outline=OUT,width=5); d.ellipse([ex-12*s,ey-12*s,ex+14*s,ey+18*s],fill=(30,20,40)); d.ellipse([ex-6*s,ey-8*s,ex+2*s,ey],fill="white")
    d.polygon([(hx-22*s,hy+15*s),(hx+22*s,hy+15*s),(hx,hy+55*s)],fill=(250,190,60),outline=OUT)
    sw=10*math.sin(t*3)*s
    d.rounded_rectangle([hx+12*s+sw*0.2,hy+5*s,hx+40*s+sw*0.2,hy+110*s],int(14*s),fill=snood,outline=OUT,width=5)
    d.ellipse([hx-35*s,hy+60*s,hx+5*s,hy+130*s],fill=snood,outline=OUT,width=5)
def tree(d,x,y,s):
    d.rectangle([x-30*s,y,x+30*s,y+330*s],fill=(110,75,50),outline=OUT,width=6)
    d.line([(x,y+80*s),(x+170*s,y+40*s)],fill=(110,75,50),width=int(26*s)); d.line([(x,y+80*s),(x+170*s,y+40*s)],fill=OUT,width=3)
    for dx,dy,r in [(0,-60,140),(-110,10,100),(110,-10,110)]: d.ellipse([x+dx*s-r*s,y+dy*s-r*s,x+dx*s+r*s,y+dy*s+r*s],fill=(70,110,70),outline=OUT,width=6)
def speed(d,x,y,t):
    for k in range(4): yy=y-60+k*40; d.line([(x-260-k*40,yy),(x-120-k*20,yy)],fill=(255,255,255,200),width=8)
def thanks2(d,t,u1,u2,t_end):
    a=back(t/0.45); out=ease((t-t_end)/0.4)
    if a<=0.02 or out>=1: return
    y=210-out*320; sc=min(a,1.1); f1=F(78*sc); f2=F(46*sc,"SemiBold")
    w=max(d.textlength(u1,font=f2),d.textlength(u2,font=f2))+130
    d.rounded_rectangle([W/2-w/2,y-80*sc,W/2+w/2,y+150*sc],50,fill="white",outline=OUT,width=10)
    d.text((W/2,y-15*sc),"¡Gracias!",font=f1,fill=(255,90,150),anchor="mm")
    d.text((W/2,y+50*sc),u1,font=f2,fill=(70,110,220),anchor="mm"); d.text((W/2,y+105*sc),u2,font=f2,fill=(70,110,220),anchor="mm")
    for k,(hx,hy) in enumerate([(W/2-w/2-10,y-70),(W/2+w/2+10,y-60),(W/2+w/2-30,y+160)]): heart(d,hx,hy+6*math.sin(t*5+k),46*sc)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_vol=tl.wt("volar",0); t_mil=tl.wt("millas",1); t_arb=tl.wt("árboles",1)
t_r=tl.wt("roja,",2); t_a=tl.wt("azul",2); t_b=tl.wt("blanca",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    night=ease((t-t_arb+0.6)/0.6) if i==1 else 0
    im=Image.blend(DAY,NIGHT,night) if night>0 else DAY.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,ph,c in LEAVES:
        y=(y0+t*60)%H; xx=x+40*math.sin(t+ph); d.ellipse([xx-14,y-8,xx+14,y+8],fill=c+(200,))
    blink=((t+0.7)%3.3)<0.13; bob=10*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        fly=ease((t-t_vol)/0.8) if t>t_vol else 0
        turkey(im,540+200*fly,1100-380*fly+bob,max(0.01,0.95*pop) if t<0.8 else 0.95-0.3*fly,t,blink,flap=math.sin(t*16)*0.6 if fly>0 else 0); d=ImageDraw.Draw(im,"RGBA")
        if fly>0.3: speed(d,540+200*fly,1100-380*fly,t)
        thanks2(d,t,USER,USER2,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_vol: a=min(1.1,back((t-t_vol)/0.4)); label(d,"¡Los pavos vuelan!",540,520,int(84*a),fill=(255,214,60))
    elif i==1:
        label(d,"Vuelan hasta",540,300,84); label(d,"55 mph",540,420,130,fill=(255,214,60))
        if t<t_arb:
            x=lerp_x=100+((lt*420)%1100); turkey(im,x,900+30*math.sin(t*3),0.55,t,blink,flap=math.sin(t*16)*0.6); d=ImageDraw.Draw(im,"RGBA"); speed(d,x,900,t)
        else:
            tree(d,420,820,1.2); k=ease((t-t_arb)/0.6); turkey(im,lerp(1000,620,k),lerp(700,760,k),0.42,t,blink=night>0.6,flap=0 if k>=1 else math.sin(t*16)*0.6); d=ImageDraw.Draw(im,"RGBA")
            if night>0.6: label(d,"zZ",760,560,64,fill="white")
    elif i==2:
        label(d,"¡Cambia de color!",540,320,96,fill=(255,214,60))
        col=(220,50,50); lab="roja"
        if t>t_a: col=(70,120,230); lab="azul"
        if t>t_b: col=(240,240,245); lab="blanca"
        turkey(im,540,1080+bob,1.1,t,blink,snood=col); d=ImageDraw.Draw(im,"RGBA")
        k=min(1.1,back((t-max(t_r,t_a if t>t_a else 0,t_b if t>t_b else 0))/0.35))
        d.rounded_rectangle([700,640,1000,760],40,fill=col,outline=OUT,width=8); label(d,lab,850,700,int(56*max(0.3,min(k,1))),fill=OUT if lab=="blanca" else "white")
        d.line([(700,740),(600,860)],fill=OUT,width=6)
    else:
        turkey(im,540,1180+bob,0.8,t,blink,flap=0.3*math.sin(t*6)); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.4,"gobble",0.6),(t_sab,"whoosh",0.35),(t_vol,"whoosh",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(t_mil,"ding",0.5),(t_arb,"boing",0.4),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_r,"pop",0.5),(t_a,"pop",0.5),(t_b,"pop",0.5),(tl.SC[2][1]-1.0,"gobble",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_pavo.mp4"); print("ok",round(tl.TOTAL,1))
