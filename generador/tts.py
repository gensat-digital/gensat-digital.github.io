import json,sys,base64,urllib.request
text=open(sys.argv[1]).read().strip()
body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.35,"use_speaker_boost":True}}).encode()
req=urllib.request.Request("https://api.elevenlabs.io/v1/text-to-speech/gbTn1bmCvNgk0QEAVyfM/with-timestamps?output_format=mp3_44100_128",data=body,headers={"xi-api-key":"dummy","Content-Type":"application/json"})
d=json.load(urllib.request.urlopen(req))
open(sys.argv[2],'wb').write(base64.b64decode(d['audio_base64']))
a=d['alignment'];json.dump(a,open(sys.argv[2]+'.json','w'))
# print word start times
w='';st=None
for c,s in zip(a['characters'],a['character_start_times_seconds']):
  if c==' ':
    if w: print(f"{st:.2f} {w}")
    w='';st=None
  else:
    if st is None: st=s
    w+=c
print(f"{st:.2f} {w}")
