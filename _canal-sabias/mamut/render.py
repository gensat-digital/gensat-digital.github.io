# ¿Sabías Que? USA — Mamut (pedido por @RamonPerez-gk6to)
# Prueba con fondos ilustrados por IA (Higgsfield, Nano Banana 2) + sistema del canal (voz, subtítulos, marca, cierre).
import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(7); tl=Timeline(4); USER="@RamonPerez-gk6to"
IMG="/home/user/gensat-digital.github.io/_canal-sabias/mamut/higgsfield/"
def load(n):  # escala a 1.12x del lienzo para poder hacer zoom y paneo sin bordes
    im=Image.open(IMG+n).convert("RGB"); s=max(W/im.width,H/im.height)*1.12
    return im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
AUR,WRA,PIR,JUN=load("mamut_prueba1.png"),load("escena1_wrangel.png"),load("escena2_piramide.png"),load("escena3_juntos.png")
def L(d,txt,x,y,size,**k):
    if size>=6: label(d,txt,x,y,size,**k)
JUN_CTA=Image.eval(JUN.filter(ImageFilter.GaussianBlur(10)),lambda v:int(v*0.55))
def kb(big,k,zoom=(1.0,1.08),pan=(0.5,0.5,0.5,0.5)):
    """Ken Burns: k de 0 a 1 recorre el zoom y el paneo."""
    k=max(0,min(1,k)); z=(zoom[0]+(zoom[1]-zoom[0])*k)*1.04
    cw=min(big.width,W*1.12/z); chh=min(big.height,H*1.12/z)
    cx=(pan[0]+(pan[2]-pan[0])*k); cy=(pan[1]+(pan[3]-pan[1])*k)
    x0=(big.width-cw)*cx; y0=(big.height-chh)*cy
    return big.resize((W,H),Image.BILINEAR,box=(x0,y0,x0+cw,y0+chh))
# degradados para que se lean títulos y subtítulos sobre la ilustración
SH=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(SH)
for y in range(H):
    a=0
    if y<560: a=int(120*(1-y/560)**1.4)
    if y>1380: a=int(150*((y-1380)/540)**1.2)
    if a: sd.line([(0,y),(W,y)],fill=(20,15,45,a))
SNOW=[(random.uniform(0,W),random.uniform(0,H),random.uniform(4,10),random.uniform(50,120)) for _ in range(70)]
def snow(d,t,alpha=200):
    for x,y0,r,v in SNOW:
        y=(y0+t*v)%H; xx=x+18*math.sin(t*1.3+y0)
        d.ellipse([xx-r,y-r,xx+r,y+r],fill=(255,255,255,alpha))
def scene_bg(i,t,lt):
    a,b=tl.SC[i]; L=b-a+tl.GAP+(tl.TOTAL-b if i==3 else 0); k=lt/L if i else t/(tl.SC[0][1]+tl.GAP)
    if i==0: return kb(AUR,k,(1.0,1.10),(0.5,0.25,0.5,0.45))
    if i==1: return kb(WRA,k,(1.08,1.0),(0.2,0.5,0.6,0.5))
    if i==2:
        base=kb(PIR,k,(1.0,1.08),(0.5,0.6,0.5,0.4)); tc=tl.wt("conviv",2)-0.35
        if t>tc:
            m=ease((t-tc)/0.45); base=Image.blend(base,kb(JUN,(t-tc)/2.5,(1.04,1.0),(0.5,0.5,0.5,0.5)),m)
        return base
    return kb(JUN_CTA,k,(1.0,1.05))
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_pir0=tl.wt("pirámides",0); t_wr=tl.wt("Wrangel",1); t_4k=tl.wt("cuatro",1)
t_gp=tl.wt("Gran",2); t_45=tl.wt("cuatro",2); t_con=tl.wt("conviv",2)
XF=0.35  # fundido entre escenas
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=scene_bg(i,t,lt)
    if i>0 and lt<XF:  # fundido desde la escena anterior
        pt=tl.SC[i][0]-0.001; pi,plt=tl.at(pt); im=Image.blend(scene_bg(pi,pt,plt),im,ease(lt/XF))
    im=Image.alpha_composite(im.convert("RGBA"),SH); d=ImageDraw.Draw(im,"RGBA")
    if i in (0,1): snow(d,t,150 if i==1 else 200)
    if i==0:
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_pir0:
            a=min(1.1,back((t-t_pir0)/0.4)); L(d,"¿Mamuts y pirámides?",W/2,420,int(70*a),fill=(255,214,60))
    elif i==1:
        a=min(1.1,back((t-t_wr+0.2)/0.4))
        if a>0.02: L(d,"Isla de Wrangel",W/2,250,int(92*a)); L(d,"(océano Ártico)",W/2,350,int(56*a),fill=(160,230,255))
        if t>t_4k:
            a=min(1.1,back((t-t_4k)/0.4)); w=640*a
            d.rounded_rectangle([W/2-w/2,470-62*a,W/2+w/2,470+62*a],44,fill=(255,255,255),outline=OUT,width=8)
            L(d,"hace ~4.000 años",W/2,470,int(62*a),fill=(255,90,150),stroke=(255,255,255))
    elif i==2:
        if t<t_con-0.35:
            a=min(1.1,back((t-t_gp+0.2)/0.4))
            if a>0.02: L(d,"La Gran Pirámide",W/2,250,int(92*a))
            if t>t_45:
                a=min(1.1,back((t-t_45)/0.4)); w=640*a
                d.rounded_rectangle([W/2-w/2,380-62*a,W/2+w/2,380+62*a],44,fill=(255,255,255),outline=OUT,width=8)
                L(d,"hace ~4.500 años",W/2,380,int(62*a),fill=(230,140,20),stroke=(255,255,255))
        else:
            a=min(1.15,back((t-t_con)/0.45)); L(d,"¡Convivieron!",W/2,250,int(120*a),fill=(255,214,60))
            for k in range(6):
                ph=(t*0.9+k/6)%1; ang=k*1.05+t; r=260+ph*120
                sparkle(d,W/2+r*math.cos(ang)*1.4,250+r*0.35*math.sin(ang),int(26*(1-ph))+4) if a>0.3 else None
    else:
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_pir0,"boing",0.4),
    (tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.4,"stomp",0.5),(t_4k,"ding",0.45),
    (tl.SC[2][0]-0.3,"whoosh",0.4),(t_45,"ding",0.45),(t_con-0.1,"twinkle",0.55),
    (tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_mamut.mp4"); print("ok",round(tl.TOTAL,1))
