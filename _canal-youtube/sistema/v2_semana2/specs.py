import json
T="DINERO EN USA · EN ESPAÑOL"; H="@PlataClaraUSA1"; END="Información educativa, no es asesoría financiera."
def S(sc,broll=None,acc=[46,204,113]):
    d={"tag":T,"handle":H,"accent":acc,"scenes":sc}
    if broll: d["broll"]=broll
    return d
def c(say,text=None,size=76,**k):
    d={"say":say,"size":size}
    if text: d["text"]=text
    d.update(k); return d
V={
"b1":S([c("Tres trampas de Black Friday que te hacen gastar más. La primera la usan casi todas las tiendas.","trampas de Black Friday que te hacen gastar más",72,num="3",icon="card"),
 c("Uno: el precio tachado. Muchas veces lo inflan antes, para que el descuento parezca enorme.","El precio tachado puede estar inflado",76,num="1",icon="cash"),
 c("Dos: el reloj de ¡solo quedan diez minutos! Es para que compres sin pensar.","La cuenta regresiva para apurarte",76,num="2",icon="calendar"),
 c("Tres: compra cien dólares y el envío es gratis. Terminas comprando cosas que no necesitabas.","\"Envío gratis desde $100\"",76,num="3",icon="phone"),
 c("Antes de pagar, compara el precio en otra tienda y espera diez minutos.","Compara precios y espera 10 minutos",76),
 c("¿Cuál te ha atrapado? Comenta el número.","¿Cuál te ha atrapado? Comenta 1, 2 o 3",80,sub=END)],
 broll={"tachado":"cash","reloj":"calendar","envío":"phone","compara":"card"}),
"b2":S([c("Compra ahora y paga después. Suena fácil, pero esto es lo que no te dicen.","\"Compra ahora, paga después\": lo que no te dicen",70,num="4"),
 c("Te dividen la compra en cuatro pagos. Parece poco, pero se cobran solos de tu cuenta.","pagos que se cobran solos de tu cuenta",72,num="4"),
 c("Si no tienes saldo ese día, te pueden cobrar cargos por atraso, y tu banco también te puede cobrar.","Sin saldo = cargos por atraso",76,num="$"),
 c("Y lo más peligroso: es fácil abrir varios a la vez y perder la cuenta de cuánto debes.","Varios a la vez = pierdes la cuenta",76,num="!"),
 c("Úsalo solo si ya tienes el dinero, y anota cada fecha de pago.","Úsalo solo si ya tienes el dinero",80),
 c("¿Lo has usado alguna vez? Comenta sí o no.","¿Lo has usado? Comenta SÍ o NO",80,sub=END)]),
"b3":S([c("Te ofrecen quince por ciento de descuento si abres la tarjeta de la tienda. Haz esta cuenta antes de aceptar.","de descuento por abrir la tarjeta de la tienda",70,num="15%",icon="card"),
 c("En una compra de doscientos dólares, ahorras treinta.","ahorras en una compra de $200",76,num="$30",count=True,icon="cash"),
 c("Pero muchas tarjetas de tienda cobran cerca de treinta por ciento de interés.","de interés en muchas tarjetas de tienda",72,num="30%",icon="bank"),
 c("Si la pagas en doce meses, pagas unos treinta y cuatro dólares de intereses. ¡Más de lo que ahorraste!","de intereses si la pagas en 12 meses",72,num="$34",count=True,icon="calendar"),
 c("Solo vale la pena si la pagas completa ese mismo mes.","Solo si la pagas completa ese mes",80),
 c("¿Tienes alguna tarjeta de tienda? Comenta.","¿Tienes tarjeta de tienda? Comenta",80,sub=END)],
 broll={"tarjeta":"card","doscientos":"cash","interés":"bank","meses":"calendar","completa":"lock"}),
"b4":S([c("Cuatro señales de que una tienda de Cyber Monday es falsa. La tercera es la más clara.","señales de una tienda falsa en Cyber Monday",72,num="4",acc=None) if False else c("Cuatro señales de que una tienda de Cyber Monday es falsa. La tercera es la más clara.","señales de una tienda falsa en Cyber Monday",72,num="4"),
 c("Uno: precios demasiado bajos, como un celular nuevo a cien dólares.","Precios demasiado bajos",80,num="1"),
 c("Dos: la dirección de la página tiene letras raras, o un nombre parecido al de una marca famosa.","Una dirección web rara",80,num="2"),
 c("Tres: solo aceptan Zelle, transferencias o tarjetas de regalo. Así no puedes reclamar tu dinero.","Solo aceptan Zelle o tarjetas de regalo",76,num="3"),
 c("Y cuatro: no tienen teléfono ni dirección real. Paga siempre con tarjeta de crédito, que te protege.","Sin teléfono ni dirección real",80,num="4"),
 c("¿Te ha pasado? Comenta y compártelo con tu familia.","¿Te ha pasado? Comenta y comparte",80,sub=END)],acc=[231,76,60]),
}
for k,v in V.items(): json.dump(v,open(f"semana2/{k}.json","w"),ensure_ascii=False,indent=1)
print(sum(len(s["say"]) for v in V.values() for s in v["scenes"]))
