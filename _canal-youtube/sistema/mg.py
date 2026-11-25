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

# ---------- piezas reutilizables extra ----------
def coin(d,x,y,r,txt="$",col=YEL):
    d.ellipse([x-r,y-r,x+r,y+r],fill=col,outline=INK,width=5); ctext(d,x,y,txt,F(FBL,r*0.9),INK)
def calendar(d,cx,cy,s,marks=(),acc=(46,204,113),title="Diciembre"):
    w,h=420*s,380*s
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],20,fill=WH,outline=INK,width=6)
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy-h/2+80*s],20,fill=acc); ctext(d,cx,cy-h/2+40*s,title,F(FB,40*s),INK)
    for r in range(4):
        for c in range(6):
            x=cx-w/2+40*s+c*68*s; y=cy-h/2+120*s+r*62*s; k=r*6+c
            col=(225,228,232); 
            if k in marks: col=marks[k] if isinstance(marks,dict) else RED
            d.rounded_rectangle([x-24*s,y-22*s,x+24*s,y+22*s],6,fill=col)
def browser(d,x0,y0,x1,y1,url,urlcol=INK):
    d.rounded_rectangle([x0,y0,x1,y1],24,fill=WH,outline=(70,78,92),width=6)
    d.rounded_rectangle([x0,y0,x1,y0+90],24,fill=(225,228,232)); d.rectangle([x0,y0+60,x1,y0+90],fill=(225,228,232))
    for k,c in enumerate([(231,76,60),(241,196,15),(46,204,113)]): d.ellipse([x0+30+k*36,y0+30,x0+54+k*36,y0+54],fill=c)
    d.rounded_rectangle([x0+150,y0+22,x1-30,y0+68],22,fill=WH); d.text((x0+175,y0+45),url,font=F(FB,36),fill=urlcol,anchor="lm")
def flag(d,x,y,s=1):
    d.line([(x,y-60*s),(x,y+60*s)],fill=WH,width=int(8*s)); d.polygon([(x,y-60*s),(x+80*s,y-38*s),(x,y-16*s)],fill=RED,outline=INK)
def bubble(d,x,y,s,txt,acc):
    d.rounded_rectangle([x-130*s,y-90*s,x+130*s,y+90*s],40,fill=CARD2,outline=acc,width=6)
    d.polygon([(x-30*s,y+88*s),(x+20*s,y+88*s),(x-50*s,y+140*s)],fill=CARD2); ctext(d,x,y,txt,F(FBL,80*s),acc)
def cta_bubbles(items):
    def f(im,lt,t,acc):
        d=ImageDraw.Draw(im,"RGBA"); n=len(items)
        for k,txt in enumerate(items):
            a=back((lt-0.3-k*0.25)/0.4)
            if a>0.02: bubble(d,540+(k-(n-1)/2)*330,1000+10*math.sin(t*3+k),min(a,1.1),txt,acc)
    return f
# ---------- Compra ahora, paga después ----------
def bnpl_hook(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); cx,cy=540,1020; phone(d,cx,cy,520,860,acc)
    d.rounded_rectangle([cx-200,cy-330,cx+200,cy-110],24,fill=CARD2); box(d,cx,cy-220,1.5,(120,140,200))
    ctext(d,cx,cy-60,"Total: $100",F(FBL,56),WH)
    g=0.5+0.5*math.sin(t*5)
    d.rounded_rectangle([cx-210,cy+40,cx+210,cy+150],55,fill=(int(46+60*g),204,113),outline=INK,width=4); ctext(d,cx,cy+95,"Paga en 4 de $25",F(FBL,42),INK)
    d.rounded_rectangle([cx-210,cy+190,cx+210,cy+290],50,outline=GR,width=4); ctext(d,cx,cy+240,"Pagar $100",F(FB,40),GR)
    if lt>1.0: hand(d,cx+130,cy+130,1 if (lt%1.3)<0.25 else 0)
def bnpl_split(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    k=ease((lt-0.2)/0.8)
    for i in range(4):
        x=lerp(540,180+i*240,k); coin(d,x,650,lerp(110,80,k),"$25" if k>0.5 else "$100")
    bal=400; n=0
    for i in range(4):
        tt=1.2+i*0.7
        if lt>tt: n+=1
        calendar_marks={}
    marks={j*6+1:(RED if j<n else (225,228,232)) for j in range(4)}
    calendar(d,320,1100,0.85,marks,acc,"Pagos")
    bal=400-25*n; ctext(d,800,960,"Tu cuenta",F(FB,44),GR); ctext(d,800,1040,f"${bal}",F(FBL,90),WH)
    if n and (lt-1.2)%0.7<0.35: ctext(d,800,1140,"-$25 automático",F(FB,40),RED)
def bnpl_fee(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    ctext(d,540,640,"Tu cuenta",F(FB,48),GR); ctext(d,540,740,"$12",F(FBL,120),WH)
    a=ease((lt-0.4)/0.6); coin(d,lerp(1000,860,a),740,70,"$25")
    if lt>1.2:
        shake=int(10*math.sin(t*40)) if lt<1.8 else 0
        stamp(d,540+shake,900,"RECHAZADO",(lt-1.2)/0.3,RED,64)
    for k,txt in enumerate(["+ Cargo por atraso","+ Cargo del banco"]):
        b=back((lt-2.2-k*0.6)/0.4)
        if b>0.02:
            y=1110+k*150; w=360*min(b,1.1)
            d.rounded_rectangle([540-w,y-55,540+w,y+55],28,fill=(60,20,20),outline=RED,width=5); ctext(d,540,y,txt,F(FB,50*min(b,1.1)),(255,210,210))
def bnpl_varios(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); total=0
    plans=[("Zapatos","$25"),("Celular","$60"),("Ropa","$30"),("TV","$75")]
    for k,(name,p) in enumerate(plans):
        a=ease((lt-0.3-k*0.6)/0.5)
        if a<=0: continue
        y=lerp(1500,620+k*150,a); total+=int(p[1:])
        d.rounded_rectangle([140,y-60,940,y+60],24,fill=CARD2,outline=(70,78,92),width=4)
        d.text((180,y),name,font=F(FB,48),fill=WH,anchor="lm"); d.text((900,y),p+"/2 sem",font=F(FBL,48),fill=RED,anchor="rm")
    if lt>2.8:
        a=ease((lt-2.8)/0.5); ctext(d,540,1330,f"Debes: ${total*4}",F(FBL,int(90*max(a,0.1))),RED)
def bnpl_ok(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    coin(d,320,800,130,"$",acc); a=back((lt-0.6)/0.4)
    if a>0.02: stamp(d,320,1000,"YA LO TIENES",min(1,(lt-0.6)/0.3),acc,44)
    calendar(d,760,880,0.75,{1:acc,7:acc,13:acc,19:acc},acc,"Anota fechas")
# ---------- Tarjeta de la tienda ----------
def tc_hook(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); x0,y0,x1,y1=150,620,930,1300
    d.rounded_rectangle([x0,y0,x1,y1],30,fill=(20,24,30),outline=(70,78,92),width=8)
    ctext(d,540,720,"Caja",F(FB,40),GR); ctext(d,540,850,"¿Abrir la tarjeta",F(FBL,60),WH); ctext(d,540,930,"y ahorrar 15%?",F(FBL,60),acc)
    for k,(txt,col) in enumerate([("SÍ",acc),("NO",GR)]):
        x=380+k*320; d.rounded_rectangle([x-120,1080,x+120,1180],50,fill=col if k==0 else None,outline=col,width=5); ctext(d,x,1130,txt,F(FBL,52),INK if k==0 else GR)
    a=ease((lt-1.0)/0.6)
    if a>0:
        x=lerp(1200,820,a); d.rounded_rectangle([x-150,1320,x+150,1500],22,fill=acc,outline=INK,width=6); d.rounded_rectangle([x-110,1370,x-50,1415],8,fill=YEL)
def tc_ahorro(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([300,620,780,1200],fill=WH); 
    for k in range(10): d.polygon([(300+k*48,1200),(324+k*48,1230),(348+k*48,1200)],fill=WH)
    d.text((340,690),"Compra",font=F(FB,44),fill=INK); d.text((740,690),"$200",font=F(FBL,48),fill=INK,anchor="ra")
    a=ease((lt-0.6)/0.5)
    if a>0: d.text((340,790),"Desc. 15%",font=F(FB,44),fill=(30,140,80)); d.text((740,790),"-$30",font=F(FBL,48),fill=(30,140,80),anchor="ra")
    d.line([(340,890),(740,890)],fill=GR,width=4)
    if a>0.9: d.text((340,930),"Pagas",font=F(FB,44),fill=INK); d.text((740,930),"$170",font=F(FBL,48),fill=INK,anchor="ra")
    for k in range(3):
        b=ease((lt-1.2-k*0.25)/0.4)
        if b>0: coin(d,880,lerp(700,1250-k*60,b),60,"$",acc)
def tc_interes(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    bars=[("Tarjeta normal",0.22*3,(120,170,230),"~22%"),("Tarjeta de tienda",0.30*3,RED,"~30%")]
    for k,(name,v,col,lab) in enumerate(bars):
        a=ease((lt-0.3-k*0.5)/0.9); x=340+k*400; h=600*v*a
        d.rounded_rectangle([x-90,1350-h,x+90,1350],20,fill=col); ctext(d,x,1400,name,F(FB,38),WH)
        if a>0.2: ctext(d,x,1350-h-60,lab,F(FBL,64),col)
    ctext(d,540,640,"Interés al año (APR)",F(FB,48),GR)
def tc_meses(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    m=min(12,int(lt*3)+1); calendar(d,540,800,0.8,{},(120,170,230),f"Mes {m} de 12")
    paid=int(34*min(1,lt/4)); ctext(d,540,1050,f"Intereses: ${paid}",F(FBL,72),RED)
    a=ease((lt-1.0)/0.8); tilt=8*a
    cx,cy=540,1300; d.line([(cx,cy-40),(cx,cy+80)],fill=GR,width=10)
    lx,ly,rx,ry=cx-260,cy-40+tilt*6,cx+260,cy-40-tilt*6; d.line([(lx,ly),(rx,ry)],fill=GR,width=10)
    for x,y,txt,col in [(lx,ly,"Ahorro $30",acc),(rx,ry,"Interés $34",RED)]:
        d.rounded_rectangle([x-120,y+10,x+120,y+80],20,fill=col); ctext(d,x,y+45,txt,F(FB,36),INK)
def tc_ok(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); x=540; y=880
    d.rounded_rectangle([x-260,y-160,x+260,y+160],30,fill=acc,outline=INK,width=8); d.rounded_rectangle([x-200,y-80,x-110,y-10],10,fill=YEL)
    stamp(d,x,y+40,"PAGADA COMPLETA",(lt-0.5)/0.3,INK,52)
    if lt>1.2: ctext(d,540,1200,"Intereses: $0",F(FBL,80),acc)
# ---------- Tienda falsa ----------
def tf_hook(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); browser(d,110,600,970,1380,"cyber-ofertas.shop")
    ctext(d,540,800,"CYBER MONDAY",F(FBL,80),INK); ctext(d,540,920,"-90% EN TODO",F(FBL,90),RED)
    for k,(x,y) in enumerate([(220,1100),(540,1180),(860,1100),(540,1300)]):
        a=back((lt-0.8-k*0.35)/0.4)
        if a>0.02: flag(d,x,y,min(a,1.1))
def tf_precio(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); cx,cy=540,1000; phone(d,cx,cy,460,760,acc)
    ctext(d,cx,cy-240,"Celular nuevo",F(FB,44),WH)
    k=ease((lt-0.5)/1.0); price=int(lerp(999,100,k)); ctext(d,cx,cy-100,f"${price}",F(FBL,110),RED if k>0.9 else WH)
    if k>0.95: flag(d,cx+250,cy-260,1.0); ctext(d,cx,cy+80,"¿Demasiado barato?",F(FB,44),(255,200,200))
def tf_url(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA")
    browser(d,110,620,970,900,"megatienda.com",(30,140,80)); ctext(d,540,800,"✓ Original".replace("✓ ",""),F(FB,46),(30,140,80))
    a=ease((lt-0.8)/0.5)
    if a>0:
        browser(d,110,980,970,1260,"rnegatienda.com",RED); ctext(d,540,1160,"Falsa",F(FB,46),RED)
        if lt>1.6:
            r=40+6*math.sin(t*8); d.ellipse([310-r*1.5,1025-r,310+r*1.5,1025+r],outline=RED,width=6)
            ctext(d,540,1340,"\"rn\" se parece a \"m\"",F(FB,46),(255,200,200))
def tf_pago(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); opts=[("Tarjeta de crédito",False),("Zelle",True),("Transferencia",True),("Tarjeta de regalo",True)]
    ctext(d,540,640,"Formas de pago",F(FB,50),GR)
    for k,(name,only) in enumerate(opts):
        a=ease((lt-0.3-k*0.35)/0.4)
        if a<=0: continue
        y=760+k*150; d.rounded_rectangle([160,y-55,920,y+55],24,fill=CARD2 if only else (25,28,34),outline=RED if only else (60,66,78),width=5)
        d.text((200,y),name,font=F(FB,46),fill=WH if only else (90,96,108),anchor="lm")
        if not only: d.line([(190,y),(890,y)],fill=(90,96,108),width=5)
    if lt>2.2: stamp(d,540,1400,"NO PUEDES RECLAMAR",(lt-2.2)/0.3,RED,52)
def tf_contacto(im,lt,t,acc):
    d=ImageDraw.Draw(im,"RGBA"); d.rounded_rectangle([160,620,920,1000],24,fill=CARD2)
    ctext(d,540,680,"Contacto",F(FB,48),GR)
    for k,lab in enumerate(["Teléfono:","Dirección:"]): d.text((210,780+k*110),lab,font=F(FB,48),fill=WH); d.text((870,780+k*110),"—",font=F(FBL,48),fill=RED,anchor="ra")
    a=ease((lt-1.6)/0.6)
    if a>0:
        x,y=540,1250; d.rounded_rectangle([x-230,y-130,x+230,y+130],26,fill=(46,204,113),outline=INK,width=6); d.rounded_rectangle([x-180,y-70,x-100,y-10],10,fill=YEL)
        sx,sy=x+170,y-110; d.polygon([(sx,sy-60),(sx+60,sy-35),(sx+50,sy+40),(sx,sy+75),(sx-50,sy+40),(sx-60,sy-35)],fill=WH,outline=INK); ctext(d,sx,sy+5,"✓".replace("✓","OK"),F(FBL,34),INK)
SCENES.update({"bnpl_hook":bnpl_hook,"bnpl_split":bnpl_split,"bnpl_fee":bnpl_fee,"bnpl_varios":bnpl_varios,"bnpl_ok":bnpl_ok,"bnpl_cta":cta_bubbles(["SÍ","NO"]),
 "tc_hook":tc_hook,"tc_ahorro":tc_ahorro,"tc_interes":tc_interes,"tc_meses":tc_meses,"tc_ok":tc_ok,"tc_cta":cta_bubbles(["Comenta"]),
 "tf_hook":tf_hook,"tf_precio":tf_precio,"tf_url":tf_url,"tf_pago":tf_pago,"tf_contacto":tf_contacto,"tf_cta":cta_bubbles(["1","2","3","4"])})
