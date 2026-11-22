# Ilustraciones propias (sin logos reales) dibujadas con PIL, para B-roll en los Shorts.
from PIL import Image, ImageDraw, ImageFont
import math
S=2  # supermuestreo
B="/usr/share/fonts/opentype/inter/Inter-Black.otf"; SB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"
WH=(245,245,240,255); DK=(30,35,44,255); DK2=(44,51,64,255); GOLD=(241,196,15,255); GR=(150,158,170,255)
def F(p,s): return ImageFont.truetype(p,int(s*S))
def base(n=400): im=Image.new("RGBA",(n*S,n*S),(0,0,0,0)); return im,ImageDraw.Draw(im)
def done(im,n=400): return im.resize((n,n),Image.LANCZOS)
def R(*a): return [int(x*S) for x in a]
def card(acc,up=False):
    im,d=base(); d.rounded_rectangle(R(30,90,370,300),int(28*S),fill=acc)
    d.rounded_rectangle(R(30,90,370,300),int(28*S),outline=(255,255,255,70),width=int(4*S))
    d.rounded_rectangle(R(70,140,130,185),int(10*S),fill=GOLD); d.line(R(70,162,130,162),fill=(200,160,10,255),width=int(3*S))
    d.text(R(70,215),"•••• 4821",font=F(SB,34),fill=(14,17,22,255))
    for k in range(3): d.ellipse(R(300+k*-22,135,330+k*-22,165),outline=(14,17,22,180),width=int(4*S))
    if up:
        d.ellipse(R(270,230,370,330),fill=WH); d.polygon(R(320,250,350,290,330,290,330,315,310,315,310,290,290,290),fill=acc)
    return done(im)
def lock(acc):
    im,d=base(); d.arc(R(120,40,280,220),180,360,fill=WH,width=int(30*S)); d.line(R(135,130,135,180),fill=WH,width=int(30*S)); d.line(R(265,130,265,180),fill=WH,width=int(30*S))
    d.rounded_rectangle(R(80,170,320,360),int(30*S),fill=acc); d.ellipse(R(178,230,222,274),fill=(14,17,22,255)); d.rectangle(R(192,260,208,310),fill=(14,17,22,255))
    return done(im)
def cash(acc):
    im,d=base()
    for k,(dx,dy) in enumerate([(-30,40),(-10,20),(10,0)]):
        x0,y0=50+dx+30,110+dy+40; d.rounded_rectangle(R(x0,y0,x0+290,y0+160),int(16*S),fill=acc if k==2 else (36,160,90,255),outline=(14,17,22,120),width=int(3*S))
        if k==2:
            d.ellipse(R(x0+105,y0+40,x0+185,y0+120),outline=(14,17,22,255),width=int(6*S)); f=F(B,58); d.text(R(x0+128,y0+44),"$",font=f,fill=(14,17,22,255))
    return done(im)
def bureaus(acc):
    im,d=base()
    for k in range(3):
        x0=40+k*105; y0=70+(k%2)*30; d.rounded_rectangle(R(x0,y0,x0+120,y0+250),int(14*S),fill=WH if k!=1 else (225,228,232,255))
        for j in range(4): d.line(R(x0+18,y0+40+j*28,x0+102-(j%2)*25,y0+40+j*28),fill=GR,width=int(6*S))
        d.ellipse(R(x0+35,y0+170,x0+85,y0+220),fill=acc); d.line(R(x0+47,y0+196,x0+58,y0+207,x0+75,y0+184),fill=(14,17,22,255),width=int(7*S),joint="curve")
    return done(im)
def phone(acc):
    im,d=base(); d.rounded_rectangle(R(110,20,290,380),int(34*S),fill=DK2); d.rounded_rectangle(R(124,50,276,350),int(16*S),fill=(14,17,22,255))
    d.rounded_rectangle(R(135,75,240,115),int(16*S),fill=GR); d.rounded_rectangle(R(165,130,265,170),int(16*S),fill=acc); d.rounded_rectangle(R(135,185,250,225),int(16*S),fill=GR)
    d.rounded_rectangle(R(170,240,265,280),int(16*S),fill=acc); d.rounded_rectangle(R(175,32,225,40),int(4*S),fill=(14,17,22,255))
    return done(im)
def calendar(acc):
    im,d=base(); d.rounded_rectangle(R(50,70,350,350),int(26*S),fill=WH); d.rounded_rectangle(R(50,70,350,140),int(26*S),fill=acc); d.rectangle(R(50,115,350,140),fill=acc)
    for x in (120,280): d.rounded_rectangle(R(x-10,45,x+10,95),int(8*S),fill=DK2)
    for r in range(3):
        for c in range(5):
            x0,y0=75+c*55,160+r*60; d.rounded_rectangle(R(x0,y0,x0+40,y0+42),int(8*S),fill=acc if (r,c)==(1,2) else (225,228,232,255))
    return done(im)
def bank(acc):
    im,d=base(); d.polygon(R(200,40,360,130,40,130),fill=acc); d.rectangle(R(55,130,345,150),fill=acc)
    for k in range(5): x=75+k*58; d.rectangle(R(x,165,x+30,300),fill=WH)
    d.rectangle(R(45,305,355,330),fill=acc); d.rectangle(R(30,335,370,360),fill=acc)
    d.ellipse(R(180,70,220,110),fill=(14,17,22,255))
    return done(im)
def gauge(acc):
    im,d=base(); cols=[(231,76,60,255),(243,156,18,255),(241,196,15,255),(46,204,113,255)]
    for k,c in enumerate(cols): d.arc(R(40,80,360,400),180+k*45,180+(k+1)*45-2,fill=c,width=int(42*S))
    a=math.radians(180+150); cx,cy=200,240; d.line(R(cx,cy,cx+130*math.cos(a),cy+130*math.sin(a)),fill=WH,width=int(14*S)); d.ellipse(R(cx-22,cy-22,cx+22,cy+22),fill=WH)
    f=F(B,54); d.text(R(140,280),"720",font=f,fill=WH)
    return done(im)
def piggy(acc):
    im,d=base(); d.ellipse(R(60,110,330,320),fill=acc); d.ellipse(R(290,170,360,240),fill=acc); d.ellipse(R(318,192,330,204),fill=(14,17,22,255))
    d.polygon(R(110,130,140,70,175,120),fill=acc); for_legs=[(100,290),(150,300),(230,300),(270,290)]
    for x,y in for_legs: d.rounded_rectangle(R(x,y,x+35,y+60),int(10*S),fill=acc)
    d.ellipse(R(240,160,256,176),fill=(14,17,22,255)); d.rounded_rectangle(R(160,120,230,135),int(6*S),fill=(14,17,22,255))
    d.ellipse(R(170,30,230,90),fill=GOLD); d.text(R(185,30),"$",font=F(B,44),fill=(14,17,22,255))
    return done(im)
ICONS={"card":lambda a:card(a),"card_up":lambda a:card(a,True),"lock":lock,"cash":cash,"bureaus":bureaus,"phone":phone,"calendar":calendar,"bank":bank,"gauge":gauge,"piggy":piggy}
def get(name,acc): return ICONS[name](tuple(acc)+(255,))
