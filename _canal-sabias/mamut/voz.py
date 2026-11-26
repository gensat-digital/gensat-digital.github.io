import json, base64, subprocess, urllib.request, re
LINES=["¡Gracias por pedirlo! Aquí te lo tengo: ¿sabías que todavía había mamuts cuando ya existían las pirámides de Egipto?",
"Los últimos mamuts vivieron en la isla de Wrangel, en el Ártico, hasta hace unos cuatro mil años.",
"La Gran Pirámide se construyó hace unos cuatro mil quinientos años, ¡así que convivieron!",
"¡Suscríbete para más videos de ¿Sabías Que?, dale like, comenta qué animal quieres para mañana y comparte este video!"]
for i,txt in enumerate(LINES):
    body=json.dumps({"text":txt,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.32,"similarity_boost":0.8,"style":0.55,"use_speaker_boost":True}}).encode()
    rq=urllib.request.Request("https://api.elevenlabs.io/v1/text-to-speech/gbTn1bmCvNgk0QEAVyfM/with-timestamps?output_format=mp3_44100_128",data=body,headers={"xi-api-key":"proxy-injected","Content-Type":"application/json"})
    r=json.load(urllib.request.urlopen(rq,timeout=120))
    open(f"audio/s{i}.mp3","wb").write(base64.b64decode(r["audio_base64"]))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"audio/s{i}.mp3","-ar","44100","-ac","1",f"audio/s{i}.wav"],check=True)
    al=r["alignment"]; ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
    words=[]; cur=""; s=None; e=None
    for c,a,b in zip(ch,st,en):
        if c.isspace():
            if cur: words.append({"text":cur,"start":s,"end":e}); cur=""
        else:
            if not cur: s=a
            cur+=c; e=b
    if cur: words.append({"text":cur,"start":s,"end":e})
    json.dump({"words":words},open(f"audio/s{i}.json","w"),ensure_ascii=False)
    print(i,len(words),words[-1]["end"])
