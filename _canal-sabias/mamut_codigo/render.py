# ¿Sabías Que? USA — Mamut (pedido por @RamonPerez-gk6to)
# Versión dibujada 100% por código (sin IA de imágenes), mismo guion y voz que la versión Higgsfield.
import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(11); tl=Timeline(4); USER="@RamonPerez-gk6to"
FUR=(150,92,52); FUR_D=(112,64,36); FUR_L=(186,124,74); TUSK=(250,238,205); PINK=(250,140,150)
def L(d,txt,x,y,size,**k):
    if size>=6: label(d,txt,x,y,size,**k)
def grad(top,bot,h=H):
    im=Image.new("RGB",(W,h)); d=ImageDraw.Draw(im)
    for y in range(h): d.line([(0,y),(W,y)],fill=mix(top,bot,y/h))
    return im
def thick(d,pts,w,col):
    w=max(2,int(w))
    d.line(pts,fill=OUT,width=w+14,joint="curve")
    for p in (pts[0],pts[-1]): d.ellipse([p[0]-(w+14)/2,p[1]-(w+14)/2,p[0]+(w+14)/2,p[1]+(w+14)/2],fill=OUT)
    d.line(pts,fill=col,width=w,joint="curve")
    for p in (pts[0],pts[-1]): d.ellipse([p[0]-w/2,p[1]-w/2,p[0]+w/2,p[1]+w/2],fill=col)
def blob(d,box,col,ow=8): d.ellipse([box[0]-ow,box[1]-ow,box[2]+ow,box[3]+ow],fill=OUT); d.ellipse(box,fill=col)
def curve(p0,p1,p2,n=14): return [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in [k/n for k in range(n+1)]]
def mammoth(d,cx,cy,s,t,walk=0.0,blink=False):
    """Mamut lanudo tierno mirando a la derecha. walk>0 mueve las patas."""
    P=lambda x,y:(cx+x*s,cy+y*s); ph=t*6
    def leg(x,dark,k):
        lift=walk*max(0,math.sin(ph+k))*28
        x0,y0=P(x-48,60); x1,y1=P(x+48,270); y1-=lift*s
        d.rounded_rectangle([x0-8,y0-8,x1+8,y1+8],int(40*s),fill=OUT); d.rounded_rectangle([x0,y0,x1,y1],int(36*s),fill=FUR_D if dark else FUR)
        for j in (-24,0,24): d.ellipse([*P(x+j-12,0),*P(x+j+12,0)] if False else [cx+(x+j-13)*s,y1-22*s,cx+(x+j+13)*s,y1-2*s],fill=TUSK)
    leg(-120,True,math.pi); leg(130,True,0)
    thick(d,[P(-270,-30),P(-310,40+8*math.sin(t*4))],14*s,FUR_D)
    blob(d,[*P(-290,-200),*P(230,170)],FUR)
    for k in range(9):  # flecos de pelo
        x=-270+k*58; y=140+10*math.sin(k*1.7); d.polygon([P(x,y-30),P(x+30,y+45),P(x+60,y-30)],fill=FUR)
        d.line([P(x,y-20),P(x+30,y+45),P(x+60,y-20)],fill=OUT,width=int(7*s))
    for k in range(6): d.arc([*P(-220+k*70,-130+14*(k%2)),*P(-170+k*70,-80+14*(k%2))],200,340,fill=FUR_D,width=int(8*s))
    leg(-40,False,0); leg(210,False,math.pi)
    sw=22*math.sin(t*2.4)
    far_t=curve(P(265,-110),P(270,50),P(395,15)); thick(d,far_t,22*s,mix(TUSK,(200,190,160),0.4))
    for x,y,r in [(140,-405,58),(215,-438,64),(290,-402,54)]: blob(d,[*P(x-r,y-r),*P(x+r,y+r)],FUR_D,6)  # copete
    blob(d,[*P(40,-420),*P(380,-60)],FUR)
    for x,y,r in [(150,-385,44),(215,-405,48),(280,-380,40)]: d.ellipse([*P(x-r,y-r*0.7),*P(x+r,y+r*0.7)],fill=FUR_D)
    blob(d,[*P(30,-300),*P(120,-185)],FUR_D,7); d.ellipse([*P(50,-280),*P(100,-205)],fill=(210,130,120))  # oreja pequeña
    ex,ey=P(282,-255)
    if blink: d.arc([ex-36*s,ey-16*s,ex+36*s,ey+24*s],200,340,fill=OUT,width=int(10*s))
    else:
        d.ellipse([ex-38*s,ey-46*s,ex+38*s,ey+46*s],fill="white",outline=OUT,width=int(8*s))
        d.ellipse([ex-16*s,ey-24*s,ex+28*s,ey+32*s],fill=(30,20,40)); d.ellipse([ex-6*s,ey-16*s,ex+10*s,ey]  ,fill="white")
    d.ellipse([*P(270,-185),*P(336,-150)],fill=PINK)
    d.arc([*P(195,-215),*P(262,-150)],20,140,fill=OUT,width=int(8*s))  # sonrisa
    trunk=curve(P(330,-170),P(400+sw*0.3,0),P(415+sw,130))+curve(P(415+sw,130),P(425+sw,190),P(472+sw,165),6)[1:]
    thick(d,trunk,60*s,FUR)
    for k in range(3,len(trunk)-4,3): x,y=trunk[k]; d.arc([x-22*s,y-6*s,x+22*s,y+14*s],200,340,fill=FUR_D,width=int(5*s))
    near_t=curve(P(235,-120),P(235,70),P(370,40)); thick(d,near_t,26*s,TUSK)
# ---------- fondos ----------
def night_base():
    im=grad((14,22,70),(40,95,140)).convert("RGBA"); d=ImageDraw.Draw(im)
    d.ellipse([110,130,230,250],fill=(250,246,215)); d.ellipse([150,110,270,230],fill=(20,28,78))
    for x,y,c in [(-200,1330,(225,240,250)),(500,1300,(205,228,245)),(900,1340,(225,240,250))]:
        d.polygon([(x,1420),(x+260,1150+random.randint(-40,40)),(x+520,1420)],fill=c)
    d.rectangle([0,1380,W,1480],fill=(40,110,160))
    for k in range(10): x=random.uniform(0,W); d.line([(x,1410+k*6),(x+60,1410+k*6)],fill=(120,180,215),width=4)
    d.ellipse([-260,1430,W+260,2400],fill=(236,246,252)); d.ellipse([-260,1430,W+260,2400],outline=(180,210,230),width=10)
    for x,y in [(150,1620),(860,1580),(560,1760)]: d.ellipse([x-90,y-26,x+90,y+26],fill=(205,225,240))
    return im
def aurora_layer():
    a=Image.new("RGBA",(W*2,900),(0,0,0,0)); d=ImageDraw.Draw(a)
    for col,y0,amp,ph in [((90,255,180,120),420,110,0),((150,120,255,90),330,90,2),((80,220,255,90),520,80,4)]:
        pts=[(x,y0+amp*math.sin(x/260+ph)+40*math.sin(x/90+ph)) for x in range(0,W*2+40,40)]
        for w in (150,80): d.line(pts,fill=col,width=w,joint="curve")
    return a.filter(ImageFilter.GaussianBlur(40))
STARS=[(random.uniform(0,W),random.uniform(0,1100),random.uniform(2,6),random.uniform(0,6)) for _ in range(90)]
NIGHT=night_base(); AUR=aurora_layer()
def night_bg(t):
    im=NIGHT.copy(); ox=int((t*40)%W); im.alpha_composite(AUR.crop((ox,0,ox+W,900)),(0,80)); d=ImageDraw.Draw(im)
    for x,y,r,p in STARS:
        a=int(140+110*math.sin(t*3+p)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,240,a))
    return im
def tundra_base():
    im=grad((140,205,245),(205,235,250),1100).convert("RGBA"); full=Image.new("RGBA",(W,H)); full.paste(im,(0,0)); d=ImageDraw.Draw(full)
    for x,y,r in [(200,300,90),(820,420,110)]:
        for dx,dy,rr in [(0,0,1),(r*0.9,10,0.8),(-r*0.9,15,0.75)]: d.ellipse([x+dx-r*rr,y+dy-r*0.6*rr,x+dx+r*rr,y+dy+r*0.6*rr],fill="white")
    d.rectangle([0,1000,W,1100],fill=(45,110,165))
    d.ellipse([-300,960,600,1300],fill=(150,165,140)); d.ellipse([400,990,1400,1320],fill=(135,155,130))
    d.rectangle([0,1150,W,H],fill=(150,160,90)); d.ellipse([-400,1080,W+400,1400],fill=(150,160,90))
    for k in range(70):
        x=random.uniform(0,W); y=random.uniform(1180,H); d.line([(x,y),(x+random.uniform(-8,8),y-random.uniform(20,45))],fill=(105,125,60),width=4)
    for x,y in [(120,1500),(900,1430),(700,1800),(260,1850)]: d.ellipse([x-120,y-30,x+120,y+30],fill=(238,245,250))
    for x,y,r in [(80,1330,60),(980,1620,70),(420,1700,45)]: d.ellipse([x-r,y-r*0.7,x+r,y+r*0.7],fill=(130,135,145),outline=OUT,width=6)
    for k in range(26):
        x=random.uniform(30,W-30); y=random.uniform(1250,H-40); c=random.choice([(245,140,190),(250,220,90),(190,150,240)])
        d.line([(x,y),(x,y+28)],fill=(80,120,60),width=4); d.ellipse([x-11,y-11,x+11,y+11],fill=c)
    return full
TUNDRA=tundra_base()
def desert_base():
    im=grad((255,214,150),(255,240,200),1150).convert("RGBA"); full=Image.new("RGBA",(W,H),(232,180,95)); full.paste(im,(0,0)); d=ImageDraw.Draw(full)
    d.ellipse([-200,1000,700,1350],fill=(238,190,110)); d.ellipse([450,1020,1350,1330],fill=(228,178,100))
    d.polygon([(560,1300),(W,1180),(W,1290),(640,1380)],fill=(90,180,230))
    for x,y in [(640,1260),(780,1210),(930,1170),(1030,1150)]:
        d.line([(x,y),(x+6,y-90)],fill=(130,90,50),width=10)
        for a in range(5): ang=math.radians(200+a*35); d.line([(x+6,y-90),(x+6+60*math.cos(ang),y-90+40*math.sin(ang))],fill=(60,150,70),width=14)
    d.rectangle([0,1330,W,H],fill=(232,182,98)); d.ellipse([-300,1280,W+300,1500],fill=(232,182,98))
    for y in range(1450,H,90): d.arc([random.uniform(-200,600),y,random.uniform(700,1300),y+120],200,340,fill=(210,160,80),width=6)
    return full
DESERT=desert_base()
def pyramid(d,cx,base,s,built=0.82):
    hw=420*s; h=480*s; top=base-h*built; tw=hw*(1-built)
    d.polygon([(cx-hw,base),(cx-tw,top),(cx+tw,top),(cx+hw,base)],fill=(240,210,140),outline=OUT,width=8)
    d.polygon([(cx+tw,top),(cx+hw,base),(cx+tw*0.2,base)],fill=(215,175,105))
    d.line([(cx-hw,base),(cx-tw,top),(cx+tw,top),(cx+hw,base),(cx-hw,base)],fill=OUT,width=8)
    for k in range(1,9):
        y=base-(base-top)*k/9; x=hw-(hw-tw)*k/9; d.line([(cx-x+6,y),(cx+x-6,y)],fill=(200,160,95),width=4)
    return top,tw
BLOCKS=[random.uniform(0,1) for _ in range(5)]
def desert_bg(t):
    im=DESERT.copy(); d=ImageDraw.Draw(im)
    sx,sy=830,330; r=95
    for k in range(12):
        a=t*0.6+k*math.pi/6; d.line([(sx+r*1.15*math.cos(a),sy+r*1.15*math.sin(a)),(sx+r*1.6*math.cos(a),sy+r*1.6*math.sin(a))],fill=(255,200,60),width=14)
    blob(d,[sx-r,sy-r,sx+r,sy+r],(255,214,60),7); d.ellipse([sx-40,sy-20,sx-24,sy],fill=OUT); d.ellipse([sx+24,sy-20,sx+40,sy],fill=OUT)
    d.arc([sx-34,sy-6,sx+34,sy+44],20,160,fill=OUT,width=7); d.ellipse([sx-66,sy+8,sx-40,sy+26],fill=PINK); d.ellipse([sx+40,sy+8,sx+66,sy+26],fill=PINK)
    top,tw=pyramid(d,500,1360,0.95)
    rp=[(1010,1500),(500+tw+30,top+20)]  # rampa
    d.line(rp,fill=OUT,width=58); d.line(rp,fill=(196,150,90),width=44)
    for k,b in enumerate(BLOCKS):
        u=(b+t*0.12)%1; x=rp[0][0]+(rp[1][0]-rp[0][0])*u; y=rp[0][1]+(rp[1][1]-rp[0][1])*u
        d.rectangle([x-26,y-52,x+26,y-12],fill=(245,235,210),outline=OUT,width=5)
        hx=x-50; d.ellipse([hx-9,y-70,hx+9,y-52],fill=(80,55,40)); d.line([(hx,y-52),(hx+4,y-22)],fill=(80,55,40),width=7)
        d.line([(hx+4,y-22),(hx-6,y-4)],fill=(80,55,40),width=6); d.line([(hx+4,y-22),(hx+14,y-4)],fill=(80,55,40),width=6); d.line([(hx+2,y-44),(x-26,y-32)],fill=(110,80,50),width=3)
    return im
def split_bg(t):
    """Arriba: el Ártico con el mamut. Abajo: Egipto con la pirámide. ¡Al mismo tiempo!"""
    top=night_bg(t); d=ImageDraw.Draw(top); d.ellipse([-300,880,W+300,1400],fill=(236,246,252)); d.ellipse([-300,880,W+300,1400],outline=(180,210,230),width=10); mammoth(d,400,700+12*math.sin(t*2.2),0.75,t,blink=((t+0.4)%3.1)<0.13)
    bot=DESERT.copy(); db=ImageDraw.Draw(bot); pyramid(db,560,1520,0.72,1.0)
    m=Image.new("L",(W,H),0); md=ImageDraw.Draw(m); md.polygon([(0,0),(W,0),(W,880),(0,1080)],fill=255)
    out=Image.composite(top,bot,m); od=ImageDraw.Draw(out); od.line([(0,1080),(W,880)],fill="white",width=22); od.line([(0,1080),(W,880)],fill=OUT,width=8)
    return out
SNOW=[(random.uniform(0,W),random.uniform(0,H),random.uniform(4,10),random.uniform(50,120)) for _ in range(60)]
def snow(d,t,alpha=200):
    for x,y0,r,v in SNOW:
        y=(y0+t*v)%H; xx=x+18*math.sin(t*1.3+y0); d.ellipse([xx-r,y-r,xx+r,y+r],fill=(255,255,255,alpha))
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_pir0=tl.wt("pirámides",0); t_wr=tl.wt("Wrangel",1); t_4k=tl.wt("cuatro",1)
t_gp=tl.wt("Gran",2); t_45=tl.wt("cuatro",2); t_con=tl.wt("conviv",2)
ONLY=os.environ.get("ONLY")
for n in (map(int,ONLY.split(",")) if ONLY else range(N)):
    t=n/FPS; i,lt=tl.at(t); blink=((t+0.7)%3.3)<0.13; bob=12*math.sin(t*2.2)
    if i==0:
        im=night_bg(t); d=ImageDraw.Draw(im,"RGBA"); pop=back((t-0.15)/0.5)
        mammoth(d,430,1180+bob,max(0.05,0.95*pop) if t<0.8 else 0.95,t,blink=blink); snow(d,t)
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_pir0: a=min(1.1,back((t-t_pir0)/0.4)); L(d,"¿Mamuts y pirámides?",W/2,420,int(70*a),fill=(255,214,60))
    elif i==1:
        im=TUNDRA.copy(); d=ImageDraw.Draw(im,"RGBA"); x=180+lt*28
        mammoth(d,x,1230+6*math.sin(t*12),0.85,t,walk=1,blink=blink)
        a=min(1.1,back((t-t_wr+0.2)/0.4))
        if a>0.02: L(d,"Isla de Wrangel",W/2,250,int(92*a)); L(d,"(océano Ártico)",W/2,350,int(56*a),fill=(40,110,170),stroke=(255,255,255))
        if t>t_4k:
            a=min(1.1,back((t-t_4k)/0.4)); w=640*a
            d.rounded_rectangle([W/2-w/2,470-62*a,W/2+w/2,470+62*a],44,fill=(255,255,255),outline=OUT,width=8)
            L(d,"hace ~4.000 años",W/2,470,int(62*a),fill=(255,90,150),stroke=(255,255,255))
    elif i==2:
        tc=t_con-0.35
        if t<tc:
            im=desert_bg(t); d=ImageDraw.Draw(im,"RGBA")
            a=min(1.1,back((t-t_gp+0.2)/0.4))
            if a>0.02: L(d,"La Gran Pirámide",W/2,620,int(92*a))
            if t>t_45:
                a=min(1.1,back((t-t_45)/0.4)); w=640*a
                d.rounded_rectangle([W/2-w/2,740-62*a,W/2+w/2,740+62*a],44,fill=(255,255,255),outline=OUT,width=8)
                L(d,"hace ~4.500 años",W/2,740,int(62*a),fill=(230,140,20),stroke=(255,255,255))
        else:
            im=split_bg(t); m=ease((t-tc)/0.4)
            if m<1: im=Image.blend(desert_bg(t),im,m)
            d=ImageDraw.Draw(im,"RGBA"); a=min(1.15,back((t-t_con)/0.45)); L(d,"¡Convivieron!",W/2,250,int(120*a),fill=(255,214,60))
            for k in range(6):
                ph=(t*0.9+k/6)%1; ang=k*1.05+t; r=260+ph*120
                if a>0.3: sparkle(d,W/2+r*math.cos(ang)*1.4,250+r*0.35*math.sin(ang),int(26*(1-ph))+4)
    else:
        im=night_bg(t); d=ImageDraw.Draw(im,"RGBA")
        pyramid(d,830,1330,0.42,1.0); mammoth(d,330,1150+bob,0.7,t,blink=blink); snow(d,t,150)
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
if ONLY: sys.exit()
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_pir0,"boing",0.4),
    (tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.4,"stomp",0.5),(t_4k,"ding",0.45),
    (tl.SC[2][0]-0.3,"whoosh",0.4),(t_45,"ding",0.45),(t_con-0.1,"twinkle",0.55),
    (tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_mamut_codigo.mp4"); print("ok",round(tl.TOTAL,1))
