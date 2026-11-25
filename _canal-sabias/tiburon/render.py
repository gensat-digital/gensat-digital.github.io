import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
random.seed(51); tl=Timeline(4); USER="@bombonherreria"
BG=ocean_bg(); BUB=[(random.uniform(0,W),random.uniform(0,H),random.uniform(8,24),random.uniform(60,150)) for _ in range(24)]
GRAY=(130,150,175); BELLY=(235,240,245)
def shark(im,cx,cy,s,t,blink=False,mouth=0.0,new_teeth=0):
    d=ImageDraw.Draw(im); sw=math.sin(t*3)*16*s
    tx,ty=cx-330*s,cy+sw
    d.polygon([(tx+50*s,ty),(tx-80*s,ty-120*s),(tx-40*s,ty),(tx-70*s,ty+90*s)],fill=GRAY); d.line([(tx+50*s,ty),(tx-80*s,ty-120*s),(tx-40*s,ty),(tx-70*s,ty+90*s),(tx+50*s,ty)],fill=OUT,width=7)
    d.polygon([(cx-60*s,cy-120*s),(cx-130*s,cy-280*s),(cx+70*s,cy-125*s)],fill=GRAY); d.line([(cx-60*s,cy-120*s),(cx-130*s,cy-280*s),(cx+70*s,cy-125*s)],fill=OUT,width=7)
    d.ellipse([cx-350*s,cy-140*s,cx+330*s,cy+140*s],fill=OUT); d.ellipse([cx-340*s,cy-130*s,cx+320*s,cy+130*s],fill=GRAY)
    d.chord([cx-300*s,cy-20*s,cx+320*s,cy+128*s],0,180,fill=BELLY)
    for k in range(3): d.arc([cx+60*s+k*28*s,cy-50*s,cx+110*s+k*28*s,cy+40*s],300,60,fill=(90,105,130),width=6)
    d.polygon([(cx+20*s,cy+60*s),(cx-80*s,cy+200*s),(cx+90*s,cy+90*s)],fill=GRAY); d.line([(cx+20*s,cy+60*s),(cx-80*s,cy+200*s),(cx+90*s,cy+90*s)],fill=OUT,width=6)
    ex,ey=cx+215*s,cy-45*s
    if blink: d.arc([ex-26*s,ey-12*s,ex+26*s,ey+18*s],200,340,fill=OUT,width=8)
    else:
        d.ellipse([ex-30*s,ey-34*s,ex+30*s,ey+34*s],fill="white",outline=OUT,width=6); d.ellipse([ex-10*s,ey-16*s,ex+22*s,ey+22*s],fill=(30,20,40)); d.ellipse([ex-2*s,ey-10*s,ex+8*s,ey],fill="white")
    d.ellipse([ex-20*s,ey+36*s,ex+26*s,ey+54*s],fill=(240,150,170))
    mx0,mx1,my=cx+110*s,cx+300*s,cy+40*s; h=(30+60*mouth)*s
    d.chord([mx0,my-h*0.3,mx1,my+h],0,180,fill=(150,40,70),outline=OUT,width=6)
    nt=7
    for k in range(nt):
        x=mx0+15*s+k*(mx1-mx0-30*s)/(nt-1); d.polygon([(x-11*s,my+2),(x+11*s,my+2),(x,my+24*s)],fill="white",outline=OUT)
    if new_teeth>0:
        for k in range(nt):
            x=mx0+15*s+k*(mx1-mx0-30*s)/(nt-1); yy=my+h*0.9-new_teeth*20*s
            d.polygon([(x-10*s,yy),(x+10*s,yy),(x,yy-22*s)],fill=(255,250,220),outline=OUT)
def tree(d,x,y,s):
    d.rectangle([x-18*s,y-10*s,x+18*s,y+90*s],fill=(140,90,60),outline=OUT,width=5)
    for dx,dy,r in [(0,-80,70),(-55,-40,55),(55,-40,55)]: d.ellipse([x+dx*s-r*s,y+dy*s-r*s,x+dx*s+r*s,y+dy*s+r*s],fill=(90,180,90),outline=OUT,width=6)
def tooth(d,x,y,s):
    d.polygon([(x-30*s,y-30*s),(x+30*s,y-30*s),(x,y+40*s)],fill="white",outline=OUT); d.line([(x-30*s,y-30*s),(x+30*s,y-30*s),(x,y+40*s),(x-30*s,y-30*s)],fill=OUT,width=5)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_sab=tl.wt("sabías",0); t_arb=tl.wt("árboles",0); t_450=tl.wt("cuatrocientos",1); t_arb2=tl.wt("árboles",1); t_die=tl.wt("dientes",2); t_mil=tl.wt("miles",2)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v in BUB: y=(y0-t*v)%H; xx=x+12*math.sin(t*2+y0); d.ellipse([xx-r,y-r,xx+r,y+r],outline=(255,255,255,150),width=4)
    seaweed(d,70,t,520,(70,190,110),0); seaweed(d,1000,t,560,(70,190,110),2.1)
    blink=((t+0.7)%3.3)<0.13; bob=14*math.sin(t*2.2); pop=back((t-0.15)/0.5)
    if i==0:
        shark(im,470,1060+bob,max(0.01,0.9*pop) if t<0.8 else 0.9,t,blink); d=ImageDraw.Draw(im,"RGBA")
        thanks(d,t,USER,t_sab-0.3)
        if t>t_sab-0.1: title_sabias(d,t-(t_sab-0.1))
        if t>t_arb:
            a=min(1.1,back((t-t_arb)/0.4)); label(d,"¡Antes que los árboles!",540,520,int(70*a),fill=(255,214,60)); tree(d,900,760,0.9*a)
    elif i==1:
        label(d,"Más viejos que",540,300,90); label(d,"¡los árboles!",540,410,100,fill=(255,214,60))
        y=760; d.rounded_rectangle([100,y-14,980,y+14],14,fill="white",outline=OUT,width=6)
        if t>t_450-0.3:
            a=min(1.1,back((t-t_450+0.3)/0.4)); d.ellipse([140-30*a,y-30*a,140+30*a,y+30*a],fill=(255,214,60),outline=OUT,width=6)
            label(d,f"{int(450*ease((t-t_450)/1.2))}",160,620,int(110*a),fill=(255,214,60)); label(d,"millones de años",200,700,40)
        if t>t_arb2-0.3:
            a=min(1.1,back((t-t_arb2+0.3)/0.4)); tree(d,830,y-110,0.7*a); label(d,"después",830,y+70,46)
        shark(im,470,1180+bob,0.75,t,blink); d=ImageDraw.Draw(im,"RGBA")
    elif i==2:
        label(d,"¡Dientes nuevos",540,300,90,fill=(255,214,60)); label(d,"toda la vida!",540,410,90)
        shark(im,450,1080+bob,1.05,t,blink,mouth=0.8,new_teeth=((t-t_die)%1.0) if t>t_die else 0); d=ImageDraw.Draw(im,"RGBA")
        if t>t_mil:
            nk=int(min(24,(t-t_mil)*18))
            for k in range(nk):
                random.seed(k); tooth(d,random.uniform(120,960),random.uniform(500,700),random.uniform(0.8,1.3))
            a=min(1.1,back((t-t_mil)/0.4)); label(d,"¡MILES!",540,1400,int(110*a),fill=(255,214,60))
    else:
        shark(im,470,1200+bob,0.8,t,blink); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,3)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.6),(0.3,"ding",0.4),(t_sab,"whoosh",0.35),(t_arb,"boing",0.45),(tl.SC[1][0]-0.3,"whoosh",0.4),(t_450,"twinkle",0.5),(t_arb2,"pop",0.5),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_die,"boing",0.45),(t_mil,"ding",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(tl.wt("suscr",3),"ding",0.5),(tl.wt("like",3),"pop",0.6),(tl.wt("comenta",3),"pop",0.6),(tl.wt("comparte",3),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_tiburon.mp4"); print("ok",round(tl.TOTAL,1))
