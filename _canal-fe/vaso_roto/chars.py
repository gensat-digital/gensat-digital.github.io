# Personajes dibujados por codigo (estilo 2D plano, lineas limpias). Siempre los mismos colores y formas.
from PIL import ImageDraw
import math
OUT=(58,40,34)
SKIN=(214,164,124); SKIN_SH=(190,140,104)
def lw(H): return max(3,int(H*0.006))
def P(cx,cy,pts,sx=1): return [(cx+x*sx,cy+y) for x,y in pts]
def limb(d,a,b,w,col,H):
    d.line([a,b],fill=OUT,width=int(w+2*lw(H))); d.line([a,b],fill=col,width=int(w))
    for p in (a,b):
        r=w/2+lw(H); d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=OUT)
    for p in (a,b):
        r=w/2; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=col)
def rrect(d,box,r,col,H): d.rounded_rectangle(box,int(r),fill=col,outline=OUT,width=lw(H))
def ell(d,box,col,H,out=True): d.ellipse(box,fill=col,outline=OUT if out else None,width=lw(H) if out else 0)
def head(d,cx,cy,r,H,c,expr,mouth,blink,look,child):
    # pelo detras
    if c["hair"]=="long":
        d.rounded_rectangle([cx-r*1.12,cy-r*1.05,cx+r*1.12,cy+r*1.55],int(r*0.6),fill=c["hair_col"],outline=OUT,width=lw(H))
    ell(d,[cx-r*0.18-r,cy-r*0.15,cx-r*0.82,cy+r*0.3],SKIN,H)  # orejas
    ell(d,[cx+r*0.82,cy-r*0.15,cx+r*1.18,cy+r*0.3],SKIN,H)
    ell(d,[cx-r,cy-r,cx+r,cy+r*1.02],SKIN,H)
    hc=c["hair_col"]
    if c["hair"]=="short":
        d.chord([cx-r*1.02,cy-r*1.08,cx+r*1.02,cy+r*0.7],180,360,fill=hc,outline=OUT,width=lw(H))
        d.polygon([(cx-r*0.98,cy-r*0.15),(cx-r*0.7,cy-r*0.55),(cx-r*0.95,cy-r*0.55)],fill=hc)
    elif c["hair"]=="curly":
        for k in range(9):
            a=math.radians(190+k*20); px,py=cx+r*0.9*math.cos(a),cy-r*0.1+r*0.95*math.sin(a)
            ell(d,[px-r*0.32,py-r*0.32,px+r*0.32,py+r*0.32],hc,H)
        ell(d,[cx-r*0.75,cy-r*1.05,cx+r*0.75,cy-r*0.2],hc,H,out=False)
    elif c["hair"]=="long":
        d.chord([cx-r*1.05,cy-r*1.1,cx+r*1.05,cy+r*0.6],180,360,fill=hc,outline=OUT,width=lw(H))
        d.polygon([(cx-r*0.05,cy-r*1.0),(cx-r*0.6,cy-r*0.25),(cx-r*1.0,cy-r*0.25)],fill=hc)
        d.polygon([(cx+r*0.05,cy-r*1.0),(cx+r*0.6,cy-r*0.25),(cx+r*1.0,cy-r*0.25)],fill=hc)
    if c.get("beard"):
        d.chord([cx-r*0.92,cy-r*0.05,cx+r*0.92,cy+r*1.3],0,180,fill=hc,outline=OUT,width=lw(H))
        d.ellipse([cx-r*0.36,cy+r*0.36,cx+r*0.36,cy+r*0.78],fill=SKIN)
    # ojos
    ey=cy+r*0.05; ex=r*0.38; er=r*(0.13 if child else 0.11); lx=look*r*0.06
    for s in (-1,1):
        x=cx+s*ex
        if blink: d.line([(x-er,ey),(x+er,ey)],fill=OUT,width=lw(H))
        else:
            ell(d,[x-er*1.25,ey-er*1.25,x+er*1.25,ey+er*1.25],(255,255,255),H,out=False)
            d.ellipse([x+lx-er*0.8,ey-er*0.8,x+lx+er*0.8,ey+er*0.8],fill=(45,30,25))
            d.ellipse([x+lx-er*0.2,ey-er*0.6,x+lx+er*0.15,ey-er*0.25],fill=(255,255,255))
        # cejas
        by=ey-r*0.3; w=r*0.22
        if expr=="angry": pts=[(x-w,by-(s*-1)*r*0.08-r*0.02),(x+w,by+(s*-1)*r*0.08-r*0.02)] if s==1 else [(x-w,by-r*0.1),(x+w,by+r*0.06)]
        elif expr=="sad": pts=[(x-w,by+r*0.06),(x+w,by-r*0.08)] if s==1 else [(x-w,by-r*0.08),(x+w,by+r*0.06)]
        else: pts=[(x-w,by),(x+w,by-r*0.03)]
        if expr=="angry" and s==1: pts=[(x-w,by+r*0.06),(x+w,by-r*0.1)]
        d.line(pts,fill=c["hair_col"] if c["hair"]!="curly" else OUT,width=max(3,int(r*0.09)))
    # mejillas
    for s in (-1,1): d.ellipse([cx+s*r*0.6-r*0.14,cy+r*0.35-r*0.08,cx+s*r*0.6+r*0.14,cy+r*0.35+r*0.08],fill=(232,150,130))
    # boca
    my=cy+r*0.55
    if mouth>0.08:
        h=r*0.08+r*0.32*mouth; ww=r*(0.22+0.12*mouth)
        d.ellipse([cx-ww,my-h*0.4,cx+ww,my+h*0.6],fill=(120,45,45),outline=OUT,width=lw(H))
    else:
        sm=c.get("smile",0)
        if sm>0: d.arc([cx-r*0.28,my-r*0.25,cx+r*0.28,my+r*0.12],20,160,fill=OUT,width=lw(H))
        elif sm<0: d.arc([cx-r*0.25,my-r*0.02,cx+r*0.25,my+r*0.3],200,340,fill=OUT,width=lw(H))
        else: d.line([(cx-r*0.16,my),(cx+r*0.16,my)],fill=OUT,width=lw(H))
def person(d,c,x,yb,H,pose="stand",expr="neutral",mouth=0,blink=False,look=0,child=False,t=0,arm=0):
    """x centro, yb linea de los pies, H altura de pie."""
    r=H*(0.15 if child else 0.105)
    sh_y=yb-H+2*r+H*0.02; hip_y=yb-H*0.42; tw=H*(0.30 if child else 0.33)
    drop=0
    if pose=="sit": drop=H*0.22
    if pose=="kneel": drop=H*0.30
    if pose=="hugknees": drop=H*0.40
    sh_y+=drop; hip_y+=drop
    hc=yb-H+r+drop
    if c.get("robe"):
        # tunica hasta los pies
        bot=yb if pose!="sit" else hip_y+H*0.2
        d.polygon([(x-tw*0.5,sh_y),(x+tw*0.5,sh_y),(x+tw*0.68,bot),(x-tw*0.68,bot)],fill=c["shirt"],outline=OUT)
        d.line([(x-tw*0.5,sh_y),(x-tw*0.68,bot),(x+tw*0.68,bot),(x+tw*0.5,sh_y)],fill=OUT,width=lw(H))
        if pose=="sit":
            limb(d,(x-tw*0.25,bot),(x-tw*0.25,yb-H*0.03),H*0.07,c["shirt"],H); limb(d,(x+tw*0.25,bot),(x+tw*0.25,yb-H*0.03),H*0.07,c["shirt"],H)
        for s in (-1,1): ell(d,[x+s*tw*0.3-H*0.05,yb-H*0.025,x+s*tw*0.3+H*0.05,yb+H*0.012],(150,100,70),H)
        # manto rojizo en diagonal
        d.polygon([(x-tw*0.5,sh_y),(x-tw*0.15,sh_y),(x+tw*0.62,hip_y+H*0.08),(x+tw*0.45,hip_y+H*0.2),(x-tw*0.55,sh_y+H*0.12)],fill=c["mantle"],outline=OUT)
    else:
        if pose in ("stand","point","tremble"):
            for s in (-1,1): limb(d,(x+s*tw*0.22,hip_y),(x+s*tw*0.24,yb-H*0.03),H*0.1,c["pants"],H)
            for s in (-1,1): ell(d,[x+s*tw*0.24-H*0.06,yb-H*0.04,x+s*tw*0.24+H*0.06,yb+H*0.01],(60,45,40),H)
        elif pose=="sit":
            for s in (-1,1): limb(d,(x+s*tw*0.22,hip_y),(x+s*tw*0.26,hip_y+H*0.08),H*0.11,c["pants"],H); limb(d,(x+s*tw*0.26,hip_y+H*0.08),(x+s*tw*0.26,yb-H*0.03),H*0.1,c["pants"],H)
            for s in (-1,1): ell(d,[x+s*tw*0.26-H*0.06,yb-H*0.04,x+s*tw*0.26+H*0.06,yb+H*0.01],(60,45,40),H)
        elif pose=="kneel":
            for s in (-1,1): limb(d,(x+s*tw*0.22,hip_y),(x+s*tw*0.3,yb-H*0.05),H*0.11,c["pants"],H)
        rrect(d,[x-tw*0.5,sh_y,x+tw*0.5,hip_y+H*0.02],tw*0.25,c["shirt"],H)
        if c.get("collar"): d.polygon([(x-tw*0.14,sh_y),(x,sh_y+H*0.05),(x+tw*0.14,sh_y)],fill=c["collar"],outline=OUT)
    # brazos
    ac=c["shirt"] if not c.get("robe") else c["shirt"]
    L=H*(0.17 if child else 0.15); aw=H*(0.075 if child else 0.07)
    lsh=(x-tw*0.46,sh_y+H*0.03); rsh=(x+tw*0.46,sh_y+H*0.03)
    def arm2(sh,a1,a2):
        e=(sh[0]+L*math.cos(a1),sh[1]+L*math.sin(a1)); h=(e[0]+L*math.cos(a2),e[1]+L*math.sin(a2))
        limb(d,sh,e,aw,ac,H); limb(d,e,h,aw*0.92,SKIN,H); ell(d,[h[0]-aw*0.6,h[1]-aw*0.6,h[0]+aw*0.6,h[1]+aw*0.6],SKIN,H)
    rad=math.radians
    if pose=="point":
        arm2(lsh,rad(100),rad(80)); arm2(rsh,rad(-20+arm),rad(-25+arm))
    elif pose=="sit":
        arm2(lsh,rad(110),rad(60)); arm2(rsh,rad(70),rad(120))
    elif pose=="tremble":
        arm2(lsh,rad(70),rad(-60)); arm2(rsh,rad(110),rad(240))
    elif pose=="hugknees":
        pass
    elif pose=="kneel": pass
    elif pose=="open":
        arm2(lsh,rad(150-arm),rad(140-arm)); arm2(rsh,rad(30+arm),rad(40+arm))
    else:
        arm2(lsh,rad(100),rad(92)); arm2(rsh,rad(80),rad(88))
    if pose=="hugknees":
        # rodillas al frente y brazos abrazandolas
        for s in (-1,1): ell(d,[x+s*tw*0.25-H*0.1,sh_y+H*0.03,x+s*tw*0.25+H*0.1,sh_y+H*0.24],c["pants"],H)
        d.rounded_rectangle([x-tw*0.55,sh_y+H*0.11,x+tw*0.55,sh_y+H*0.17],int(H*0.03),fill=SKIN,outline=OUT,width=lw(H))
        for s in (-1,1): ell(d,[x+s*tw*0.25-H*0.07,yb-H*0.07,x+s*tw*0.25+H*0.07,yb],(60,45,40),H)
    head(d,x,hc,r,H,c,expr,mouth,blink,look,child)
    return {"head":(x,hc,r),"chest":(x,sh_y+H*0.1),"sh_y":sh_y,"tw":tw}
DANIEL={"hair":"short","hair_col":(30,24,22),"shirt":(42,92,62),"pants":(214,196,160),"collar":(34,76,50)}
MATEO={"hair":"curly","hair_col":(28,22,20),"shirt":(246,196,60),"pants":(64,110,190)}
JESUS={"hair":"long","hair_col":(110,72,44),"beard":True,"robe":True,"shirt":(240,228,204),"mantle":(176,74,58),"smile":1}
NINO={"hair":"short","hair_col":(30,24,22),"shirt":(120,140,150),"pants":(90,80,70)}
PADRE={"hair":"short","hair_col":(40,34,30),"shirt":(110,90,80),"pants":(70,60,55),"collar":(90,72,64)}
