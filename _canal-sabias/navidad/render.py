import sys; sys.path.insert(0,"/home/user/canal-sabias")
from sabias_lib import *
def lerp(a,b,k): return a+(b-a)*k
random.seed(81); tl=Timeline(5)
def make_bg():
    im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix((30,45,90),(70,60,120),y/H))
    d.ellipse([-300,1500,W+300,2300],fill=(240,245,255),outline=OUT,width=8)
    for x,h in [(90,260),(980,300),(200,180)]:
        d.polygon([(x,1560-h),(x-90,1580),(x+90,1580)],fill=(50,120,80),outline=OUT)
        d.polygon([(x,1560-h),(x-50,1560-h*0.45),(x+50,1560-h*0.45)],fill=(240,245,255))
    return im.convert("RGBA")
BG=make_bg()
SNOW=[(random.uniform(0,W),random.uniform(0,H),random.uniform(4,10),random.uniform(40,110),random.uniform(0,6)) for _ in range(60)]
def flame(d,x,y,s,t,on):
    if not on: return
    f=1+0.12*math.sin(t*14+x)
    d.ellipse([x-26*s,y-60*s*f,x+26*s,y+6*s],fill=(255,170,40))
    d.ellipse([x-13*s,y-38*s*f,x+13*s,y+2*s],fill=(255,240,160))
def candle(d,x,y,s,t,col,on,big=False):
    h=(130 if big else 80)*s; w=(36 if big else 22)*s
    d.rounded_rectangle([x-w,y-h,x+w,y],int(8*s),fill=col,outline=OUT,width=5)
    d.line([(x,y-h),(x,y-h-14*s)],fill=OUT,width=4); flame(d,x,y-h-12*s,s*(1.2 if big else 0.8),t,on)
def glow(im,x,y,r,a):
    g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).ellipse([x-r,y-r,x+r,y+r],fill=(255,190,90,a)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(50)))
def wheel(im,cx,cy,R,t,lit,sundays=(6,13,20)):
    d=ImageDraw.Draw(im)
    d.ellipse([cx-R-18,cy-R*0.45-18,cx+R+18,cy+R*0.45+18],fill=(110,70,45),outline=OUT,width=8)
    d.ellipse([cx-R+30,cy-R*0.45+20,cx+R-30,cy+R*0.45-20],fill=(30,45,90),outline=OUT,width=6)
    for k in range(8): a=k*math.pi/4; d.line([(cx,cy),(cx+(R-30)*math.cos(a),cy+(R*0.45-20)*math.sin(a))],fill=(110,70,45),width=12)
    d.ellipse([cx-40,cy-22,cx+40,cy+22],fill=(110,70,45),outline=OUT,width=5)
    pts=[]
    for k in range(24):
        a=-math.pi/2+k*2*math.pi/24; pts.append((k,a,cx+R*math.cos(a),cy+R*0.45*math.sin(a)))
    for k,a,x,y in sorted(pts,key=lambda p:p[3]):
        big=k in sundays or k==23
        candle(d,x,y,1.0,t,(255,255,255) if big else (220,50,60),k<lit,big)
def wreath(im,cx,cy,s,t,lit):
    d=ImageDraw.Draw(im)
    d.ellipse([cx-300*s,cy-120*s,cx+300*s,cy+120*s],fill=(40,110,70),outline=OUT,width=8)
    for k in range(26):
        a=k*2*math.pi/26; x=cx+280*s*math.cos(a); y=cy+105*s*math.sin(a)
        d.ellipse([x-34*s,y-22*s,x+34*s,y+22*s],fill=(60,140,80))
        if k%3==0: d.ellipse([x-12*s,y-12*s,x+12*s,y+12*s],fill=(220,40,50))
    d.ellipse([cx-200*s,cy-55*s,cx+200*s,cy+55*s],fill=(30,45,90))
    for k,(dx,dy) in enumerate([(-220,10),(-75,-60),(75,-60),(220,10)]):
        candle(d,cx+dx*s,cy+dy*s,1.4*s,t,[(140,80,170),(140,80,170),(240,150,190),(140,80,170)][k],k<lit,True)
def cal(d,cx,cy,s,t,hl):
    w,h=560*s,520*s; d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],24,fill="white",outline=OUT,width=8)
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy-h/2+90*s],24,fill=(220,50,60)); d.rectangle([cx-w/2,cy-h/2+60*s,cx+w/2,cy-h/2+90*s],fill=(220,50,60))
    d.text((cx,cy-h/2+45*s),"Noviembre",font=F(46*s),fill="white",anchor="mm")
    days=["L","M","M","J","V","S","D"]
    for c,dn in enumerate(days): d.text((cx-w/2+50*s+c*76*s,cy-h/2+130*s),dn,font=F(32*s,"SemiBold"),fill=(120,120,140),anchor="mm")
    nums=[23,24,25,26,27,28,29]
    for c,nm in enumerate(nums):
        x=cx-w/2+50*s+c*76*s; y=cy-h/2+220*s
        if nm==29 and hl>0:
            r=40*s*min(1.15,back(hl)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,214,60),outline=OUT,width=5)
        d.text((x,y),str(nm),font=F(40*s),fill=OUT,anchor="mm")
    if hl>0: d.text((cx,cy+h/2-90*s),"1.ª vela de Adviento",font=F(40*s),fill=(220,50,60),anchor="mm")
os.makedirs("frames",exist_ok=True); N=int(tl.TOTAL*FPS)
t_rueda=tl.wt("rueda",0); t_24=tl.wt("veinticuatro",0); t_dia=tl.wt("día,",2); t_dom=tl.wt("domingo.",2); t_cor=tl.wt("corona",3); t_este=tl.wt("domingo!",3)
for n in range(N):
    t=n/FPS; i,lt=tl.at(t)
    im=BG.copy(); d=ImageDraw.Draw(im,"RGBA")
    for x,y0,r,v,ph in SNOW: y=(y0+t*v)%H; xx=x+20*math.sin(t+ph); d.ellipse([xx-r,y-r,xx+r,y+r],fill=(255,255,255,200))
    if i==0:
        title_sabias(d,t)
        if t>t_rueda-0.2:
            a=ease((t-t_rueda+0.2)/0.6); lit=int(24*ease((t-t_24)/1.6)) if t>t_24 else 0
            glow(im,540,1050,380*a,int(90*a*lit/24)); wheel(im,540,1050,330*max(0.35,a),t,lit); d=ImageDraw.Draw(im,"RGBA")
            if t>t_24: a2=min(1.1,back((t-t_24)/0.4)); label(d,"24 velas",540,560,int(110*a2),fill=(255,214,60))
    elif i==1:
        label(d,"Alemania, 1839",540,300,90,fill=(255,214,60))
        for k in range(3):
            x=300+k*240; y=1080+10*math.sin(t*3+k); a=back((lt-0.3-k*0.25)/0.4)
            if a<=0.02: continue
            s=min(a,1.1); d.ellipse([x-60*s,y-60*s,x+60*s,y+60*s],fill=(240,195,160),outline=OUT,width=6)
            d.chord([x-62*s,y-64*s,x+62*s,y+10*s],180,360,fill=[(60,40,30),(150,100,50),(40,30,25)][k],outline=OUT,width=5)
            for ex in (-20,20): d.ellipse([x+ex*s-8*s,y+5*s-8*s,x+ex*s+8*s,y+5*s+8*s],fill=OUT)
            d.rounded_rectangle([x-70*s,y+60*s,x+70*s,y+220*s],int(30*s),fill=[(200,60,60),(60,120,200),(80,160,90)][k],outline=OUT,width=6)
            bx,by=x+40*s,y-170*s; d.rounded_rectangle([bx-80*s,by-55*s,bx+80*s,by+55*s],30,fill="white",outline=OUT,width=5); label(d,"¿Ya?",bx,by,int(48*s),fill=(220,50,60))
        label(d,"¿Cuánto falta?",540,600,84)
    elif i==2:
        label(d,"1 pequeña cada día",540,300,72,fill=(255,120,120)); label(d,"1 grande cada domingo",540,400,72,fill="white")
        lit=int(lerp(0,21,ease(lt/(tl.SC[2][1]-tl.SC[2][0])))); glow(im,540,1050,380,int(60*lit/24))
        wheel(im,540,1050,330,t,lit); d=ImageDraw.Draw(im,"RGBA")
        label(d,f"Día {max(1,lit)}",540,1450,70,fill=(255,214,60))
    elif i==3:
        label(d,"La corona",540,290,100,fill=(255,214,60)); label(d,"de Adviento",540,400,100,fill=(120,220,140))
        if t<t_este-0.2:
            lit=0; glow(im,540,1000,300,30); wreath(im,540,1000,1.2,t,lit); d=ImageDraw.Draw(im,"RGBA")
        else:
            k=ease((t-t_este+0.2)/0.6); cal(d,540,820,1.0,t,(t-t_este)/0.4)
            glow(im,280,1330,200,int(120*k)); wreath(im,540,1330,0.85,t,1); d=ImageDraw.Draw(im,"RGBA")
    else:
        glow(im,540,1250,260,60); wreath(im,540,1250,0.9,t,1); d=ImageDraw.Draw(im,"RGBA")
        cta(d,t,tl,4)
    subs(d,t,tl)
    finish(im,t,i,lt).convert("RGB").save(f"frames/{n:05d}.jpg",quality=92)
fx=[(0.1,"bells",0.5),(t_rueda,"pop",0.5),(t_24,"twinkle",0.5),(tl.SC[1][0]-0.3,"whoosh",0.4),(tl.SC[1][0]+0.4,"boing",0.4),(tl.SC[2][0]-0.3,"whoosh",0.4),(t_dia,"match",0.5),(t_dom,"match",0.5),(tl.SC[3][0]-0.3,"whoosh",0.4),(t_este,"match",0.6),(t_este+0.3,"bells",0.5),(tl.SC[4][0]-0.3,"whoosh",0.4),(tl.wt("suscr",4),"ding",0.5),(tl.wt("like",4),"pop",0.6),(tl.wt("comenta",4),"pop",0.6),(tl.wt("comparte",4),"ding",0.5)]
build_audio_video(tl,fx,"sabias_que_navidad.mp4"); print("ok",round(tl.TOTAL,1))
