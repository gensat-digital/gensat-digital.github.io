# Short con narracion ElevenLabs: cada escena dura lo que dura su voz.
import json, sys, os, subprocess, urllib.request
spec=json.load(open(sys.argv[1])); out=sys.argv[2]; voice=spec.get("voice","gbTn1bmCvNgk0QEAVyfM")
work=out+"_work"; os.makedirs(work,exist_ok=True)
def tts(text,path):
    body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True}}).encode()
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",data=body,headers={"Content-Type":"application/json","xi-api-key":"proxy-injected"})
    open(path,"wb").write(urllib.request.urlopen(req).read())
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
parts=[]
for i,sc in enumerate(spec["scenes"]):
    p=f"{work}/s{i}.mp3"
    if not os.path.exists(p): tts(sc["say"],p)
    sc["sec"]=round(dur(p)+0.35,2); parts.append(p)
spec["scenes"][-1]["sec"]+=1.2  # cola final para que no termine de golpe
# voz completa con silencios de 0.35 s entre escenas
lst=f"{work}/list.txt"; sil=f"{work}/sil.mp3"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t","0.35","-c:a","libmp3lame","-b:a","128k",sil],check=True)
open(lst,"w").write("".join(f"file '{os.path.abspath(p)}'\nfile '{os.path.abspath(sil)}'\n" for p in parts))
raw=f"{work}/voz_raw.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-af","apad=pad_dur=1.2",raw],check=True)
# normalizar en un paso aparte: loudnorm dentro de amix se comia los ultimos 3 s
voz=f"{work}/voz.wav"; subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af","loudnorm=I=-15:TP=-1.5","-ar","44100",voz],check=True)
total=dur(voz); json.dump(spec,open(f"{work}/spec.json","w"),ensure_ascii=False)
mudo=f"{work}/mudo.mp4"; subprocess.run(["python3","render_short.py",f"{work}/spec.json",mudo],check=True)
# musica suave debajo de la voz
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mudo,"-i",voz,
 "-f","lavfi","-i",f"sine=f=220:d={total}","-f","lavfi","-i",f"sine=f=277.18:d={total}","-f","lavfi","-i",f"sine=f=329.63:d={total}",
 "-filter_complex",f"[2][3][4]amix=inputs=3,volume=0.25,tremolo=f=2:d=0.3,lowpass=f=900,afade=t=in:d=1,afade=t=out:st={total-1.5}:d=1.5[m];[1][m]amix=inputs=2:duration=first:normalize=0[a]",
 "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k",out],check=True)
print("ok",out,round(total,1),"s")
