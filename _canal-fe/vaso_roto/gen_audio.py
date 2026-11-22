import json, urllib.request, subprocess
API="https://api.elevenlabs.io"
def post(url,body):
    req=urllib.request.Request(API+url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","xi-api-key":"proxy-injected"})
    return urllib.request.urlopen(req).read()
DANIEL="U9jmr7kY6mMqS39kfA01"   # Alex - mexicano, voz grave
JESUS="WOSzFvlJRm2hkYb3KA5w"    # Juan Campillo - calido y calmado
lines={
 "l1":(DANIEL,"¡Otra vez, Mateo! ¡Nunca tienes cuidado!",{"stability":0.28,"similarity_boost":0.8,"style":0.75,"use_speaker_boost":True}),
 "l2":(JESUS,"Daniel... ¿a quién escuchaste gritar así por primera vez?",{"stability":0.6,"similarity_boost":0.8,"style":0.2,"use_speaker_boost":True}),
 "l3":(JESUS,"De niño aprendiste que un error se paga con gritos.",{"stability":0.6,"similarity_boost":0.8,"style":0.2,"use_speaker_boost":True}),
 "l4":(JESUS,"Él no recordará el vaso roto. Recordará cómo lo hiciste sentir.",{"stability":0.6,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True}),
 "l5":(DANIEL,"Perdóname, hijo. El vaso no importa. Tú sí importas.",{"stability":0.45,"similarity_boost":0.8,"style":0.5,"use_speaker_boost":True}),
}
for k,(v,t,vs) in lines.items():
    open(k+".mp3","wb").write(post(f"/v1/text-to-speech/{v}?output_format=mp3_44100_128",{"text":t,"model_id":"eleven_multilingual_v2","voice_settings":vs}))
sfx={"glass":("glass cup falling on wooden floor and shattering, short, realistic, indoor",2.0),
     "heal":("soft warm magical shimmer, gentle chime swell, healing light",3.0),
     "whoosh":("very soft gentle airy transition whoosh",1.0),
     "room":("quiet calm living room ambience, very soft distant birds, no voices",8.0)}
for k,(t,d) in sfx.items():
    open(k+".mp3","wb").write(post("/v1/sound-generation",{"text":t,"duration_seconds":d,"prompt_influence":0.5}))
open("music.mp3","wb").write(post("/v1/music?output_format=mp3_44100_128",{"prompt":"Soft emotional solo piano, gentle and warm, slow tempo around 70 bpm, hopeful faith-inspired cinematic mood, starts tender and sad then becomes warm and hopeful, intimate, no drums, no vocals","music_length_ms":60000,"force_instrumental":True}))
for f in list(lines)+list(sfx)+["music"]:
    d=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f+".mp3"]).decode().strip(); print(f,d)
