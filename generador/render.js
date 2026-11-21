// uso: node render.js spec.json voz.mp3 salida.mp4
const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');
const [specF,voz,out]=process.argv.slice(2);
const spec=JSON.parse(fs.readFileSync(specF));const al=JSON.parse(fs.readFileSync(voz+'.json'));
// palabras con tiempos
const W=[];let w='',s=null,e=0;
al.characters.forEach((c,i)=>{if(c===' '){if(w)W.push({w,s,e});w='';s=null}else{if(s===null)s=al.character_start_times_seconds[i];w+=c;e=al.character_end_times_seconds[i]}});if(w)W.push({w,s,e});
// frases: cortar en puntuación o cada 5 palabras
const P=[];let cur=[];W.forEach((x,i)=>{cur.push(x);if(/[.,?!…]$/.test(x.w)||cur.length>=5||i==W.length-1){P.push({s:cur[0].s,e:cur[cur.length-1].e,words:cur});cur=[]}});
spec.phrases=P;
// tiempos "@palabra": inicio de la primera palabra que empieza así (sin signos)
const norm=x=>x.toLowerCase().normalize('NFD').replace(/[^a-z0-9ñ$]/g,'');
let cur0=0;const res=o=>{for(const k in o){const v=o[k];if(typeof v==='string'&&v[0]==='@'){const f=W.find(x=>x.s>=cur0-.01&&norm(x.w).startsWith(norm(v.slice(1))));if(!f)throw new Error('no encuentro '+v);o[k]=cur0=f.s}else if(v&&typeof v==='object')res(v)}};
res(spec);if(!spec.dur)spec.dur=Math.ceil((W[W.length-1].e+1.8)*10)/10;
const FPS=30,N=Math.round(spec.dur*FPS),dir=out+'.frames';fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.addInitScript(s=>{window.SPEC=s},spec);
await p.goto('file://'+__dirname+'/plantilla.html');await p.evaluate(()=>document.fonts.ready);
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/FPS);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();
// música suave de fondo (acordes sintetizados) + voz
execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${dir}/%04d.jpg -i ${voz} -f lavfi -t ${spec.dur} -i "aevalsrc='0.05*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*2*t))+0.04*sin(2*PI*277.2*t)+0.035*sin(2*PI*329.6*t)+0.06*sin(2*PI*55*t)*exp(-6*mod(t,0.5))':s=44100" -filter_complex "[2:a]volume=0.55,afade=t=in:d=0.5,afade=t=out:st=${spec.dur-1.5}:d=1.5[m];[1:a]volume=1.6[v];[v][m]amix=inputs=2:duration=longest:normalize=0[a]" -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium -r ${FPS} -c:a aac -b:a 160k -t ${spec.dur} -movflags +faststart ${out}`);
fs.rmSync(dir,{recursive:true,force:true});console.log('ok',out);
})();
