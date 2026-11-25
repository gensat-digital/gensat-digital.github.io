# Motion graphics para Plata Clara: escenas que ENSEÑAN con objetos animados (estilo adulto, limpio).
import math
from PIL import Image, ImageDraw, ImageFont
FB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; FBL="/usr/share/fonts/opentype/inter/Inter-Black.otf"; FM="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
_F={}
def F(p,s):
    k=(p,int(s))
    if k not in _F: _F[k]=ImageFont.truetype(p,max(8,int(s)))
    return _F[k]
W,H=1080,1920
INK=(14,17,22); CARD=(30,35,44); CARD2=(44,51,64); WH=(245,245,240); GR=(150,158,170); RED=(231,76,60); YEL=(241,196,15)
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x): x=max(0,min(1,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def lerp(a,b,k): return a+(b-a)*k
def ctext(d,x,y,txt,f,col): d.text((x,y),txt,font=f,fill=col,anchor="mm")
def phone(d,cx,cy,w,h,acc):
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],int(w*0.12),fill=(10,12,16),outline=(70,78,92),width=6)
    d.rounded_rectangle([cx-w/2+16,cy-h/2+16,cx+w/2-16,cy+h/2-16],int(w*0.09),fill=CARD)
    d.rounded_rectangle([cx-50,cy-h/2+28,cx+50,cy-h/2+42],7,fill=(10,12,16))
def tag(d,cx,cy,s,txt,col=WH,txtcol=INK,ang=0):
    w,h=300*s,170*s
    pts=[(cx-w/2,cy-h/2),(cx+w/2-50*s,cy-h/2),(cx+w/2,cy),(cx+w/2-50*s,cy+h/2),(cx-w/2,cy+h/2)]
    d.polygon(pts,fill=col,outline=(70,78,92)); d.ellipse([cx+w/2-75*s,cy-12*s,cx+w/2-51*s,cy+12*s],fill=INK)
    ctext(d,cx-25*s,cy,txt,F(FBL,72*s),txtcol)
def strike(d,x0,y,x1,k,col=RED,w=10):
    if k>0: d.line([(x0,y),(lerp(x0,x1,k),y)],fill=col,width=w)
def stamp(d,cx,cy,txt,k,col=RED,size=60):
    if k<=0: return
    s=lerp(1.6,1.0,ease(k)); f=F(FBL,size*s); tw=d.textlength(txt,font=f)
    d.rounded_rectangle([cx-tw/2-24,cy-size*s*0.7,cx+tw/2+24,cy+size*s*0.7],14,outline=col,width=8)
    ctext(d,cx,cy,txt,f,col)
def cart(d,cx,cy,s,acc):
    d.line([(cx-200*s,cy-130*s),(cx-150*s,cy-130*s),(cx-100*s,cy+60*s),(cx+150*s,cy+60*s),(cx+190*s,cy-80*s),(cx-130*s,cy-80*s)],fill=WH,width=int(14*s),joint="curve")
    for x in (cx-70*s,cx+120*s): d.ellipse([x-22*s,cy+90*s,x+22*s,cy+134*s],outline=WH,width=int(10*s))
def box(d,x,y,s,col):
    d.rounded_rectangle([x-45*s,y-40*s,x+45*s,y+40*s],8,fill=col,outline=INK,width=4); d.line([(x,y-40*s),(x,y+40*s)],fill=INK,width=4)
def bar(d,x0,y0,x1,h,k,col,bg=CARD2):
    d.rounded_rectangle([x0,y0,x1,y0+h],h//2,fill=bg)
    if k>0.01: d.rounded_rectangle([x0,y0,x0+max(h,(x1-x0)*min(1,k)),y0+h],h//2,fill=col)
def hand(d,x,y,press=0):
    y+=press*12
    d.rounded_rectangle([x-18,y-70,x+18,y+20],18,fill=(232,196,160),outline=INK,width=4)
    d.rounded_rectangle([x-40,y,x+50,y+90],30,fill=(232,196,160),outline=INK,width=4)
    if press>0.5: d.ellipse([x-50,y-120,x+50,y-20],outline=WH,width=4)
# ---------- escenas de "3 trampas de Black Friday" ----------
def bf_hook(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); cx,cy=540,980
    sw=math.sin(t*2.4)*4
    d.line([(cx-120,cy-260),(cx,cy-330),(cx+120,cy-260)],fill=GR,width=6)
    d.rounded_rectangle([cx-280,cy-260+sw,cx+280,cy+180+sw],30,fill=(20,20,24),outline=(70,78,92),width=6)
    ctext(d,cx,cy-120+sw,"BLACK",F(FBL,110),WH); ctext(d,cx,cy+10+sw,"FRIDAY",F(FBL,110),acc)
    ctext(d,cx,cy+120+sw,"HASTA -70%",F(FB,52),YEL)
    for k,(x,y) in enumerate([(220,700),(860,760),(830,1260)]):
        a=back((lt-1.0-k*0.35)/0.4)
        if a>0.02:
            r=70*min(a,1.15); d.regular_polygon((x,y,r),3,rotation=0,fill=RED,outline=INK); ctext(d,x,y+12,"!",F(FBL,r*0.9),WH)
def bf_tachado(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    k1=ease((lt-0.2)/0.6); k2=ease((lt-1.6)/0.8); k3=ease((lt-3.2)/0.5)
    ctext(d,300,620,"Octubre",F(FB,48),GR); ctext(d,780,620,"Black Friday",F(FB,48),GR)
    tag(d,300,820,0.95*max(0.01,k1),"$79")
    if k2>0:
        price=int(lerp(79,129,k2)); tag(d,780,820,0.95,f"${price}")
        if k3>0:
            strike(d,660,820,880,k3,RED,12)
            a=back((lt-3.4)/0.4)
            if a>0.02: tag(d,780,1060,0.8*min(a,1.1),"$99",col=acc)
    if lt>4.6:
        a=ease((lt-4.6)/0.5); d.rounded_rectangle([140,1230,940,1380],30,fill=(60,20,20,int(230*a)),outline=RED,width=6)
        ctext(d,540,1305,"Pagas $20 MÁS que en octubre",F(FB,48),(255,220,220))
def bf_reloj(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); cx,cy=540,1000
    phone(d,cx,cy,520,860,acc)
    d.rounded_rectangle([cx-200,cy-330,cx+200,cy-90],24,fill=CARD2); box(d,cx,cy-210,1.6,(200,150,90))
    ctext(d,cx,cy-40,"Audífonos Pro",F(FB,46),WH); ctext(d,cx,cy+20,"$89",F(FBL,64),acc)
    secs=max(0,599-int(lt*7)); blink=(int(t*4)%2==0)
    d.rounded_rectangle([cx-200,cy+80,cx+200,cy+180],20,fill=(RED if blink else (150,40,30)))
    ctext(d,cx,cy+130,f"⏱ {secs//60:02d}:{secs%60:02d}".replace("⏱ ",""),F(FBL,64),WH)
    ctext(d,cx,cy+225,"¡Solo quedan 3!",F(FB,40),(255,200,200))
    press=1 if (lt%1.2)<0.25 and lt>1.5 else 0
    d.rounded_rectangle([cx-200,cy+270,cx+200,cy+360],45,fill=acc); ctext(d,cx,cy+315,"COMPRAR YA",F(FBL,44),INK)
    if lt>1.2: hand(d,cx+120,cy+340,press)
def bf_envio(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); cx=540
    cart(d,cx,1080,1.5,acc)
    items=[(20,0.3,(80,140,220)),(25,1.0,(200,90,120)),(18,1.7,(230,170,60))]
    total=82; 
    for k,(p,t0,col) in enumerate(items):
        a=ease((lt-t0)/0.6)
        if a>0: box(d,cx-120+k*120,lerp(560,1000,a),1.0,col)
        if lt>t0+0.6: total+=p
    goal=100; bar(d,140,640,940,46,total/goal,acc if total>=goal else YEL)
    ctext(d,540,590,"Envío gratis desde $100",F(FB,46),WH)
    ctext(d,540,740,f"Tu carrito: ${total}",F(FBL,64),WH if total<goal else acc)
    if lt>2.8:
        a=ease((lt-2.8)/0.5); d.rounded_rectangle([140,1330,940,1470],30,fill=(60,20,20,int(230*a)),outline=RED,width=6)
        ctext(d,540,1400,"Gastaste $63 para ahorrar $8",F(FB,48),(255,220,220))
def bf_compara(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    for k,(x,store,price) in enumerate([(300,"Tienda A","$99"),(780,"Tienda B","$84")]):
        a=ease((lt-0.2-k*0.4)/0.5)
        if a<=0: continue
        y=lerp(1200,1000,a); phone(d,x,y,380,640,acc)
        ctext(d,x,y-200,store,F(FB,44),GR); box(d,x,y-60,1.2,(200,150,90)); ctext(d,x,y+90,price,F(FBL,80),WH)
    if lt>1.6:
        a=back((lt-1.6)/0.4); r=70*min(a,1.15)
        d.ellipse([780-r,720-r,780+r,720+r],fill=acc,outline=INK,width=6); d.line([(780-r*0.45,720),(780-r*0.1,720+r*0.35),(780+r*0.5,720-r*0.35)],fill=INK,width=int(r*0.2),joint="curve")
    if lt>2.4:
        a=ease((lt-2.4)/0.5); cx,cy=540,1440; R=70
        d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=WH,width=8); ang=-math.pi/2+(lt*2)%6.28
        d.line([(cx,cy),(cx+R*0.7*math.cos(ang),cy+R*0.7*math.sin(ang))],fill=WH,width=8); ctext(d,cx+250,cy,"espera 10 min",F(FB,44),WH)
def bf_cta(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    for k,n in enumerate(["1","2","3"]):
        a=back((lt-0.3-k*0.25)/0.4)
        if a<=0.02: continue
        x=260+k*280; y=1000+10*math.sin(t*3+k); s=min(a,1.1)
        d.rounded_rectangle([x-110*s,y-90*s,x+110*s,y+90*s],40,fill=CARD2,outline=acc,width=6)
        d.polygon([(x-30*s,y+88*s),(x+20*s,y+88*s),(x-50*s,y+140*s)],fill=CARD2)
        ctext(d,x,y,n,F(FBL,100*s),acc)
SCENES={"bf_hook":bf_hook,"bf_tachado":bf_tachado,"bf_reloj":bf_reloj,"bf_envio":bf_envio,"bf_compara":bf_compara,"bf_cta":bf_cta}
