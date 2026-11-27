import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
def lerp(a,b,k): return a+(b-a)*k
random.seed(71); tl=Timeline(4)
def grad(top,bot):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix(top,bot,y/H))
    return im.convert("RGBA")
SHOP=grad((60,40,110),(30,25,70)); OLD=grad((230,210,170),(200,170,130)); CITY=grad((120,180,230),(200,225,245))
def building(d,x,w,h,col,base=1450):
    d.rectangle([x,base-h,x+w,base],fill=col,outline=OUT,width=6)
    for r in range(int(h//90)):
        for c in range(int(w//70)): d.rectangle([x+20+c*70,base-h+25+r*90,x+50+c*70,base-h+65+r*90],fill=(255,240,180))
def street(d):
    d.rectangle([0,1450,W,H],fill=(80,85,95)); 
    for x in range(0,W,160): d.rectangle([x+30,1600,x+110,1620],fill=(255,230,120))
def car(d,x,y,s,col):
    d.rounded_rectangle([x-110*s,y-40*s,x+110*s,y+30*s],int(20*s),fill=col,outline=OUT,width=6)
    d.rounded_rectangle([x-60*s,y-85*s,x+60*s,y-35*s],int(16*s),fill=col,outline=OUT,width=6); d.rectangle([x-45*s,y-75*s,x+45*s,y-45*s],fill=(200,230,250))
    for dx in (-60,60): d.ellipse([x+dx*s-26*s,y+5*s,x+dx*s+26*s,y+57*s],fill=OUT)
def police(d,x,y,s,t):
    d.rounded_rectangle([x-130*s,y-45*s,x+130*s,y+35*s],int(22*s),fill="white",outline=OUT,width=7)
    d.rectangle([x-130*s,y-10*s,x+130*s,y+10*s],fill=(40,60,140))
    d.rounded_rectangle([x-70*s,y-95*s,x+70*s,y-40*s],int(16*s),fill="white",outline=OUT,width=6); d.rectangle([x-55*s,y-85*s,x+55*s,y-50*s],fill=(200,230,250))
    on=int(t*6)%2; d.rounded_rectangle([x-40*s,y-120*s,x,y-95*s],8,fill=(230,50,50) if on else (120,30,30)); d.rounded_rectangle([x,y-120*s,x+40*s,y-95*s],8,fill=(50,90,230) if not on else (30,40,110))
    for dx in (-75,75): d.ellipse([x+dx*s-28*s,y+10*s,x+dx*s+28*s,y+66*s],fill=OUT)
def bag(d,x,y,s,col,txt=""):
    d.arc([x-35*s,y-95*s,x+35*s,y-25*s],180,360,fill=OUT,width=int(9*s))
    d.rounded_rectangle([x-75*s,y-60*s,x+75*s,y+90*s],int(14*s),fill=col,outline=OUT,width=6)
    if txt: label(d,txt,x,y+15*s,int(40*s),fill="white")
def ledger(d,x,y,s,k,t):
    w,h=520*s,560*s; d.rounded_rectangle([x-w/2,y-h/2,x+w/2,y+h/2],20,fill=(255,252,240),outline=OUT,width=8)
    d.text((x,y-h/2+55*s),"Cuentas de la tienda",font=F(40*s),fill=OUT,anchor="mm")
    rows=[("Enero","-$8,000"),("Junio","-$3,000"),("Nov.","-$1,000")]
    for r,(m,v) in enumerate(rows):
        yy=y-h/2+140*s+r*80*s; d.text((x-w/2+40*s,yy),m,font=F(40*s,"SemiBold"),fill=OUT,anchor="lm"); d.text((x+w/2-40*s,yy),v,font=F(44*s),fill=(220,50,50),anchor="rm")
    yy=y-h/2+400*s; d.line([(x-w/2+30*s,yy-40*s),(x+w/2-30*s,yy-40*s)],fill=OUT,width=4)
    val=int(lerp(-1000,12000,ease(k))); col=(30,30,30) if val>=0 else (220,50,50)
    d.text((x-w/2+40*s,yy+20*s),"Black Friday",font=F(40*s,"SemiBold"),fill=OUT,anchor="lm"); d.text((x+w/2-40*s,yy+20*s),(f"+${val:,}" if val>=0 else f"-${-val:,}"),font=F(48*s),fill=col,anchor="rm")
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_pol=tl.wt("policía",0); t_fil=tl.wt("Filadelfia",1); t_caos=tl.wt("caos",1); t_rojos=tl.wt("rojos",2); t_neg=tl.wt("negros,",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    blink=((t+0.7)%3.3)<0.13
    if i==0:
        im=SHOP.copy(); d=ImageDraw.Draw(im,"RGBA")
        for k,(x,col,txt) in enumerate([(300,(230,60,80),"-50%"),(540,(250,190,60),"SALE"),(780,(80,180,120),"-70%")]):
            a=back((t-0.2-k*0.2)/0.4)
            if a>0.02: bag(d,x,900+10*math.sin(t*3+k),min(a,1.1)*1.3,col,txt)
        title_sabias(d,t)
        if t>t_pol:
            a=min(1.1,back((t-t_pol)/0.4)); police(d,540,1330,1.7*a,t); label(d,"¡Lo inventó la policía!",540,560,int(76*min(a,1)),fill=(255,214,60))
        else: label(d,"BLACK FRIDAY",540,560,110,fill="white")
    elif i==1:
        im=OLD.copy(); d=ImageDraw.Draw(im,"RGBA")
        building(d,40,260,620,(170,120,90)); building(d,330,220,760,(150,110,95)); building(d,580,240,560,(180,140,100)); building(d,840,220,700,(160,115,90))
        street(d)
        for k in range(6):
            x=((k*230+lt*(60 if t<t_caos else 15))%1300)-120; car(d,x,1560,0.85,[(200,70,60),(70,120,190),(230,180,60)][k%3])
        label(d,"Filadelfia, años 60",540,310,80,fill=OUT,stroke=(255,250,230))
        if t>t_caos:
            a=min(1.1,back((t-t_caos)/0.4))
            for k in range(14):
                random.seed(k); x=random.uniform(80,1000); y=random.uniform(1380,1460)
                d.ellipse([x-22,y-60,x+22,y-16],fill=(60,50,50)); d.rounded_rectangle([x-26,y-18,x+26,y+50],12,fill=[(200,70,60),(70,120,190),(90,160,90)][k%3])
            label(d,"¡CAOS!",540,460,int(120*a),fill=(220,50,50),stroke=OUT)
    elif i==2:
        im=SHOP.copy(); d=ImageDraw.Draw(im,"RGBA")
        label(d,"De rojo",540,300,96,fill=(255,110,110)); label(d,"a ganancias",540,420,96,fill=(120,230,150))
        k=(t-t_neg)/1.2 if t>t_neg else 0
        ledger(d,540,1030,1.2,k,t)
        if k>1: label(d,"¡Ganancias!",540,1450,90,fill=(120,230,150))
    else:
        im=SHOP.copy(); d=ImageDraw.Draw(im,"RGBA")
        for k,(x,col) in enumerate([(380,(230,60,80)),(700,(80,180,120))]): bag(d,x,1250+10*math.sin(t*3+k),1.3,col)
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.5),(0.35,"pop",0.5),(0.55,"pop",0.5),(t_pol,"siren",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(t_caos,"boing",0.45),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_neg+1.1,"cash",0.6),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_blackfriday.mp4"); print("ok",round(tl.TOTAL,1))
