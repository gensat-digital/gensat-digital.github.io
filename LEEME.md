# Reels diarios de GENSAT (rama `videos`)

Esta rama **no es la web**. Solo guarda los videos que se publican en Instagram y Facebook (@yeison_e_genes_v) y el generador que los hace. Nunca se mezcla con `main`.

## Cómo se hace un video
1. Escribir el guion (voz, 14–17 s) en `guiones/AAAA-MM-DD-am|pm-tema.txt`.
   Estructura fija, igual al reel que mejor funcionó ("¿Todavía sumas 1 + 1 en libreta?", 406 vistas):
   - Gancho con pregunta y algo de humor (0–3 s).
   - El problema con dos ejemplos concretos, y el resultado malo (3–8 s).
   - "Con GENSAT…" y la solución en el celular (8–13 s).
   - Cierre: "Escríbeme por WhatsApp y te muestro cómo."
2. Crear la voz con ElevenLabs (voz latina "Enrique M. Nieto"):
   `python3 generador/tts.py guiones/X.txt /tmp/X.mp3` (guarda también `/tmp/X.mp3.json` con los tiempos).
3. Escribir `guiones/X.json` copiando la forma de los ejemplos. Los tiempos se escriben como `"@palabra"`:
   la escena empieza cuando la voz dice esa palabra (se buscan en orden).
4. Renderizar: `node generador/render.js guiones/X.json /tmp/X.mp3 reels/X.mp4` (unos 45 s).
5. Revisar 4 fotogramas (`ffmpeg -ss T -i reels/X.mp4 -frames:v 1 f.png`): que ningún texto se corte ni se salga.
6. Anotar el tema en `temas.md` para no repetirlo.

## Reglas
- Logo de GENSAT idéntico (la plantilla ya lo trae, no tocarlo).
- WhatsApp +1 (385) 574-5556 · Instagram @yeison_e_genes_v · web gensat-digital.github.io. Nunca @gensat10.
- Precios en dólares (USD). Datos siempre de ejemplo, nunca de clientes reales. Nunca mencionar Nutrix.
- Nada de café (ni la palabra ni el emoji ☕).
- No repetir un tema de los últimos 14 días (ver `temas.md`).
- Si un video necesita un archivo original de Yeison (su video, su foto, su audio) y no lo tienes: detente y pídeselo. No lo busques en internet, no grabes su pantalla y no lo reemplaces con IA (Higgsfield u otra) sin preguntarle.

## Publicación (Metricool, marca "Gensat ", id 7555771, zona America/Denver)
- 2 por día: 7:30 AM y 6:30 PM, Instagram (REEL) + Facebook (REEL).
- `autoPublish: true`: se publican solos a su hora. (Con `false`, Instagram NO se publica: Metricool solo manda un aviso para terminarlo a mano. Así pasó el 21 de noviembre.)
- Vista previa: al terminar, se le envían a Yeison los 2 MP4 con SendUserFile, para que pueda pedir cambios o quitarlos antes de la hora.
- Video: `https://raw.githubusercontent.com/gensat-digital/gensat-digital.github.io/videos/reels/<archivo>.mp4`
- `instagramData.isAiGenerated: true` (la voz es generada con IA).
