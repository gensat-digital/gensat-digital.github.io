import json, urllib.request, subprocess
S={"pop":("cartoon bubble pop, short, cute",0.6),"ding":("bright cheerful notification ding, single bell chime",1.0),
"whoosh":("quick soft cartoon whoosh transition",0.8),"twinkle":("magical sparkle twinkle chime, short",1.2),
"boing":("cartoon boing spring sound, playful",0.8),"stomp":("cute cartoon elephant footstep thump, soft",0.7)}
def gen(name,text,d,loop=False):
    b={"text":text,"duration_seconds":d,"prompt_influence":0.6}
    if loop: b["loop"]=True
    rq=urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation",data=json.dumps(b).encode(),headers={"xi-api-key":"proxy-injected","Content-Type":"application/json"})
    open(f"audio/{name}.mp3","wb").write(urllib.request.urlopen(rq,timeout=180).read()); print(name)
for k,(t,d) in S.items(): gen(k,t,d)
gen("music_raw","cheerful playful kids documentary background music loop, ukulele, glockenspiel and soft bass, bright and curious, no vocals",22,loop=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","audio/music_raw.mp3","-ar","44100","-ac","2","audio/music.wav"],check=True)
