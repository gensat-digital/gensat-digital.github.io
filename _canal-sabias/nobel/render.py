import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
def lerp(a,b,k): return a+(b-a)*k
random.seed(91); tl=Timeline(5)
def grad(top,bot):
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix(top,bot,y/H))
    return im.convert("RGBA")
BG=grad((60,45,90),(120,80,60)); GOLDBG=grad((40,40,80),(20,20,50))
DUST=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,5),random.uniform(0,6)) for _ in range(40)]
SKIN=(240,200,170); HAIR=(120,110,100)
def nobel(im,cx,cy,s,t,blink=False,mood="neutral"):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([cx-170*s,cy+120*s,cx+170*s,cy+460*s],int(70*s),fill=(40,40,55),outline=OUT,width=8)
    d.polygon([(cx-50*s,cy+120*s),(cx,cy+230*s),(cx+50*s,cy+120*s)],fill="white",outline=OUT); d.polygon([(cx-18*s,cy+140*s),(cx+18*s,cy+140*s),(cx,cy+200*s)],fill=(150,40,50))
    d.ellipse([cx-125*s,cy-150*s,cx+125*s,cy+120*s],fill=SKIN,outline=OUT,width=8)
    d.chord([cx-130*s,cy-165*s,cx+130*s,cy+40*s],190,350,fill=HAIR,outline=OUT,width=6)
    d.chord([cx-125*s,cy-10*s,cx+125*s,cy+200*s],0,180,fill=HAIR,outline=OUT,width=7)
    d.ellipse([cx-55*s,cy+45*s,cx+55*s,cy+95*s],fill=SKIN)
    for k in (-1,1):
        ex,ey=cx+k*48*s,cy-25*s
        if blink: d.arc([ex-22*s,ey-10*s,ex+22*s,ey+16*s],200,340,fill=OUT,width=7)
        else: d.ellipse([ex-20*s,ey-22*s,ex+20*s,ey+22*s],fill="white",outline=OUT,width=5); d.ellipse([ex-10*s,ey-10*s,ex+12*s,ey+14*s],fill=(30,20,40))
        bw=-8 if mood=="sad" else 0
        d.line([(ex-26*s,ey-36*s+bw*k*s),(ex+26*s,ey-36*s-bw*k*s)],fill=HAIR,width=int(9*s))
    d.ellipse([cx-16*s,cy+10*s,cx+16*s,cy+42*s],fill=(225,170,140))
    if mood=="smile": d.arc([cx-35*s,cy+50*s,cx+35*s,cy+90*s],20,160,fill=OUT,width=6)
    elif mood=="sad": d.arc([cx-30*s,cy+70*s,cx+30*s,cy+100*s],200,340,fill=OUT,width=6)
def dynamite(d,x,y,s,t):
    for k in range(3): d.rounded_rectangle([x-75*s+k*50*s,y-90*s,x-30*s+k*50*s,y+90*s],int(14*s),fill=(210,60,50),outline=OUT,width=5)
    d.rectangle([x-80*s,y-20*s,x+75*s,y+5*s],fill=(90,70,60))
    d.line([(x,y-90*s),(x+20*s,y-140*s),(x+5*s,y-170*s)],fill=OUT,width=5)
    for k in range(5): a=t*10+k*1.3; d.line([(x+5*s,y-170*s),(x+5*s+25*s*math.cos(a),y-170*s+25*s*math.sin(a))],fill=(255,210,60),width=5)
def coins(d,x,y,n,t):
    for k in range(n): d.ellipse([x-60+(k%4)*35,y-k*12-25,x+20+(k%4)*35,y-k*12+15],fill=(255,205,60),outline=OUT,width=4)
def newspaper(d,cx,cy,s,t):
    w,h=620*s,720*s; ang=math.sin(t*2)*0.02
    d.rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],fill=(245,240,225),outline=OUT,width=8)
    d.text((cx,cy-h/2+60*s),"LE JOURNAL · 1888",font=F(40*s),fill=OUT,anchor="mm"); d.line([(cx-w/2+30*s,cy-h/2+100*s),(cx+w/2-30*s,cy-h/2+100*s)],fill=OUT,width=4)
    d.text((cx,cy-h/2+170*s),"«El mercader",font=F(56*s),fill=(150,30,30),anchor="mm"); d.text((cx,cy-h/2+240*s),"de la muerte",font=F(56*s),fill=(150,30,30),anchor="mm"); d.text((cx,cy-h/2+310*s),"ha muerto»",font=F(56*s),fill=(150,30,30),anchor="mm")
    for k in range(6): d.line([(cx-w/2+40*s,cy-h/2+390*s+k*45*s),(cx+w/2-40*s-(k%2)*120*s,cy-h/2+390*s+k*45*s)],fill=(170,165,150),width=8)
def medal(d,x,y,s,t,label_txt):
    d.polygon([(x-40*s,y-200*s),(x-10*s,y-60*s),(x+10*s,y-60*s),(x+40*s,y-200*s)],fill=(60,100,190),outline=OUT)
    d.ellipse([x-90*s,y-90*s,x+90*s,y+90*s],fill=(255,205,60),outline=OUT,width=7); d.ellipse([x-65*s,y-65*s,x+65*s,y+65*s],outline=(220,160,30),width=6)
    lab(d,label_txt,x,y+150*s,int(42*s))
def lab(d,txt,x,y,size,fill="white"): label(d,txt,x,y,size,fill=fill)
def scroll(d,cx,cy,s,k):
    w=560*s; h=lerp(60,640,k)*s
    d.rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],fill=(250,240,210),outline=OUT,width=6)
    for yy in (cy-h/2,cy+h/2): d.rounded_rectangle([cx-w/2-30*s,yy-28*s,cx+w/2+30*s,yy+28*s],int(28*s),fill=(200,160,100),outline=OUT,width=6)
    if k>0.6:
        d.text((cx,cy-h/2+80*s),"Testamento",font=F(56*s),fill=OUT,anchor="mm"); d.text((cx,cy-h/2+150*s),"París · 27 nov 1895",font=F(36*s,"SemiBold"),fill=(120,90,60),anchor="mm")
        for j in range(4): d.line([(cx-w/2+50*s,cy-h/2+230*s+j*55*s),(cx+w/2-50*s-(j%2)*90*s,cy-h/2+230*s+j*55*s)],fill=(190,170,140),width=8)
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_test=tl.wt("testamento",0); t_prem=tl.wt("Nobel?",0); t_mill=tl.wt("millonario",1); t_per=tl.wt("periódico",1); t_merc=tl.wt("mercader",1)
t_cien=tl.wt("ciencia,",2); t_lit=tl.wt("literatura",2); t_paz=tl.wt("paz.",2); t_dic=tl.wt("diez",3)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=(GOLDBG if i>=2 else BG).copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y,r,ph in DUST: d.ellipse([x-r,y-r,x+r,y+r],fill=(255,230,170,int(120+100*math.sin(t*2+ph))))
    blink=((t+0.7)%3.3)<0.13
    if i==0:
        title_sabias(d,t,200); lab(d,"Un día como hoy · 1895",540,360,58,fill=(255,214,60))
        dynamite(d,240,1100,1.3,t)
        if t>t_test-0.3:
            k=ease((t-t_test+0.3)/0.8); scroll(d,640,1040,0.95,k)
            if t>t_test+0.4:
                pk=min(1,(t-t_test-0.4)/1.2); pts=[(470+pk*j*3,1260+8*math.sin(j*0.6)) for j in range(int(pk*100))]
                if len(pts)>1: d.line(pts,fill=(40,60,150),width=6)
        if t>t_prem-0.2: a=min(1.1,back((t-t_prem+0.2)/0.4)); medal(d,540,560+0,0.0001+0.001,t,"") if False else lab(d,"¡Los Premios Nobel!",540,470,int(70*a),fill=(255,214,60))
    elif i==1:
        lab(d,"Alfred Nobel",540,300,96,fill=(255,214,60))
        if t<t_per:
            nobel(im,540,900,1.4,t,blink,"smile"); d=ImageDraw.Draw(im,"RGBA"); dynamite(d,220,1350,1.0,t)
            if t>t_mill: coins(d,860,1500,int(min(14,(t-t_mill)*10)),t); lab(d,"¡Millonario!",820,1180,60,fill=(255,214,60))
        else:
            k=ease((t-t_per)/0.6); newspaper(d,540,1000,lerp(0.4,1.1,k),t)
            if t>t_merc: lab(d,"¡Por error!",540,1450,80,fill=(255,110,110))
            nobel(im,880,1500,0.55,t,blink,"sad"); d=ImageDraw.Draw(im,"RGBA")
    elif i==2:
        lab(d,"Quiso ser recordado",540,300,80,fill="white"); lab(d,"por algo mejor",540,400,80,fill=(255,214,60))
        nobel(im,540,1200,0.75,t,blink,"smile"); d=ImageDraw.Draw(im,"RGBA")
        for k,(tt,txt) in enumerate([(t_cien,"Ciencia"),(t_lit,"Literatura"),(t_paz,"Paz")]):
            if t>tt-0.2: a=min(1.1,back((t-tt+0.2)/0.4)); medal(d,220+k*320,780+10*math.sin(t*3+k),max(0.05,a),t,txt)
    elif i==3:
        lab(d,"Cada año…",540,300,96,fill="white")
        w,h=560,560; cx,cy=540,980
        d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],30,fill="white",outline=OUT,width=8)
        d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy-h/2+120],30,fill=(200,50,60)); d.rectangle([cx-w/2,cy-h/2+90,cx+w/2,cy-h/2+120],fill=(200,50,60))
        d.text((cx,cy-h/2+60),"DICIEMBRE",font=F(60),fill="white",anchor="mm")
        a=min(1.15,back((t-t_dic+0.2)/0.4)) if t>t_dic-0.2 else 0.6
        d.text((cx,cy+60),"10",font=F(int(260*max(0.6,a))),fill=OUT,anchor="mm")
        medal(d,540,1500,0.7,t,"")
    else:
        medal(d,540,1250,1.0,t,""); cta(d,t,tl,4)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.15,"pop",0.5),(t_test,"paper",0.6),(t_test+0.4,"pen",0.6),(t_prem,"ding",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(t_mill,"twinkle",0.4),(t_per,"paper",0.6),(t_merc,"boing",0.4),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_cien,"pop",0.5),(t_lit,"pop",0.5),(t_paz,"ding",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(t_dic,"twinkle",0.5),(tl.SC[4][0]-0.3,"whoosh",0.4),(tl.wt("suscr",4),"ding",0.5),(tl.wt("like",4),"pop",0.6),(tl.wt("comenta",4),"pop",0.6),(tl.wt("comparte",4),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_nobel.mp4"); print("ok",round(tl.TOTAL,1))
