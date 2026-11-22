import json
T="DINERO EN USA · EN ESPAÑOL"; H="@PlataClaraUSA1"; END="Información educativa, no es asesoría financiera."
def S(sc,acc=[46,204,113]): return {"tag":T,"handle":H,"accent":acc,"scenes":sc}
def c(say,text=None,size=76,**k):
    d={"say":say,"size":size}
    if text: d["text"]=text
    d.update(k); return d
V={
"s04":S([c("Cuatro razones por las que el banco te puede cerrar la cuenta. La primera casi nadie la sabe.","razones por las que el banco te cierra la cuenta",74,num="4"),
 c("Uno: partir tus depósitos de efectivo para no llegar a diez mil dólares. Se ve sospechoso, y hasta puede ser delito, aunque el dinero sea legal.","Partir tus depósitos de efectivo para no llegar a $10,000",70,num="1"),
 c("Dos: sobregiros que se quedan sin pagar.","Sobregiros sin pagar",80,num="2"),
 c("Tres: tu nombre o dirección no coinciden con tus documentos.","Datos que no coinciden con tus documentos",76,num="3"),
 c("Y cuatro: cuentas que pasan meses sin movimiento.","Meses sin movimiento",80,num="4"),
 c("¿Cuál te ha pasado a ti? Comenta el número.","¿Cuál te ha pasado? Comenta 1, 2, 3 o 4",80,sub=END)]),
"s05":S([c("Cinco estafas que les llegan a los latinos por WhatsApp. Si te llega la primera, no contestes.","estafas que llegan por WhatsApp",76,num="5"),
 c("Uno: hola mamá, cambié de número, necesito dinero. Llama al número de siempre antes de mandar nada.","\"Hola mamá, cambié de número\"",80,num="1"),
 c("Dos: trabajos que te pagan por dar likes. Al final te piden que tú deposites.","Te pagan por dar likes",80,num="2"),
 c("Tres: un falso aviso del IRS. El IRS no te escribe por WhatsApp.","Falso aviso del IRS",80,num="3"),
 c("Cuatro y cinco: premios que nunca jugaste, e inversiones con ganancias seguras.","Premios que no jugaste e inversiones \"seguras\"",72,num="4·5"),
 c("¿Cuál te ha llegado a ti? Comenta el número, y compártelo con tu familia.","¿Cuál te ha llegado? Comenta el número",80,sub="Compártelo con tu familia.")],acc=[231,76,60]),
"s06":S([c("Si ganas dos mil ochocientos dólares al mes, así los tienes que repartir.","al mes: así repártelos",76,num="$2,800",count=True),
 c("Mil cuatrocientos para lo necesario: renta, comida y transporte.","50 %: renta, comida y transporte",72,num="$1,400",count=True,bar=0.5),
 c("Ochocientos cuarenta para tus gustos y salidas.","30 %: tus gustos",76,num="$840",count=True,bar=0.3),
 c("Y quinientos sesenta para ahorrar o pagar deudas.","20 %: ahorro o deudas",76,num="$560",count=True,bar=0.2),
 c("Si tu renta se come más de la mitad, recorta de los gustos, no del ahorro.","¿La renta se come más de la mitad? Recorta gustos, no ahorro",72),
 c("¿Tú cuánto ahorras al mes? Comenta.","¿Cuánto ahorras tú al mes? Comenta",80,sub=END)]),
"s07":S([c("Así es como un carro de treinta mil dólares te termina costando más de cuarenta y dos mil.","es lo que pagas por un carro de $30,000",70,num="$42,239",count=True),
 c("Con un doce por ciento de interés, a setenta y dos meses...","de interés a 72 meses",76,num="12%"),
 c("pagas unos quinientos ochenta y siete dólares al mes, durante seis años.","al mes, durante 6 años",76,num="$587",count=True),
 c("Más de doce mil son solo intereses.","solo en intereses",76,num="$12,239",count=True,bar=0.29),
 c("Por eso, mejora tu crédito y compara tasas en una cooperativa antes de firmar en la agencia.","Mejora tu crédito y compara tasas antes de firmar",76),
 c("¿A qué tasa compraste tu carro? Comenta.","¿A qué tasa compraste tu carro? Comenta",80,sub=END)]),
"s08":S([c("Tres pasos para empezar tu crédito desde cero, con una tarjeta asegurada.","pasos para empezar tu crédito desde cero",74,num="3"),
 c("Uno: dejas un depósito, por ejemplo doscientos dólares, y ese es tu límite. Te lo devuelven al cerrarla o al subir de nivel.","Deja un depósito: $200 = $200 de límite",74,num="1"),
 c("Dos: confirma que reporte a los tres burós: Equifax, Experian y TransUnion.","Que reporte a Equifax, Experian y TransUnion",70,num="2"),
 c("Tres: úsala solo para algo pequeño, como el teléfono, y págala completa cada mes.","Úsala poco y págala completa cada mes",76,num="3"),
 c("En seis a doce meses, muchos bancos te dan una tarjeta normal.","meses para subir a una tarjeta normal",72,num="6–12"),
 c("¿En qué paso vas tú? Comenta.","¿En qué paso vas? Comenta 1, 2 o 3",80,sub=END)]),
"s09":S([c("Mandar dinero con envío gratis te puede salir más caro. Mira este ejemplo con trescientos dólares.","El envío \"gratis\" te puede salir más caro",82),
 c("La app A no cobra comisión y paga diecisiete veinte. La app B cobra cuatro dólares, pero paga diecisiete sesenta.","Mandas $300:",64,options=["App A: $0 de comisión, cambio 17.20","App B: $4 de comisión, cambio 17.60"],sub="Tipos de cambio de ejemplo."),
 c("Con la A, tu familia recibe cinco mil ciento sesenta pesos.","pesos con la app A",76,num="5,160",count=True),
 c("Con la B, recibe cinco mil doscientos nueve. Gana la que cobra comisión.","pesos con la app B",76,num="5,209",count=True),
 c("Compara siempre cuánto recibe tu familia al final.","Compara cuánto RECIBE tu familia, no la comisión",76),
 c("¿A qué país mandas tú? Comenta.","¿A qué país mandas dinero? Comenta",80,sub=END)]),
"s10":S([c("Quinientos dólares. Esa es tu primera meta para emergencias, y te explico por qué.","es tu primera meta de ahorro",76,num="$500",count=True),
 c("Con quinientos dólares cubres muchos imprevistos: una llanta, una consulta médica o una reparación, sin usar la tarjeta.","Cubres una llanta, una consulta o una reparación sin usar la tarjeta",68),
 c("Después, la meta es juntar de tres a seis meses de tus gastos básicos.","meses de gastos: tu meta final",76,num="3–6"),
 c("El truco: programa una transferencia automática el día que te pagan, aunque sean veinte dólares.","Ahorra automático el día que te pagan",78,sub="Aunque sean $20."),
 c("Y guárdalo en una cuenta aparte, para no gastarlo sin querer.","Guárdalo en una cuenta aparte",80),
 c("¿Cuánto llevas tú? Comenta.","¿Cuánto llevas ahorrado? Comenta",80,sub=END)]),
"s11":S([c("Mil doscientos dólares al año que tu empresa te puede regalar, y mucha gente no los cobra.","al año que tu empresa te puede regalar",72,num="+$1,200",count=True),
 c("Se llama el match del cuatro cero uno ka. Tu empresa pone dinero cuando tú ahorras para tu retiro.","El \"match\": tu empresa pone dinero cuando tú ahorras",68,num="401(k)"),
 c("Ejemplo: ganas cuarenta mil al año y pones el seis por ciento, dos mil cuatrocientos.","pones el 6 % de un sueldo de $40,000",72,num="$2,400",count=True),
 c("Si tu empresa pone el cincuenta por ciento de eso, te regala mil doscientos más.","si tu empresa pone el 50 %",76,num="+$1,200",count=True,bar=0.5),
 c("Pregunta en recursos humanos cuánto es el match de tu empresa.","Pregunta en recursos humanos cuánto es tu match",76),
 c("¿Tu trabajo lo tiene? Comenta sí o no.","¿Tu trabajo lo tiene? Comenta SÍ o NO",80,sub=END)]),
}
for k,v in V.items(): json.dump(v,open(f"semana1b/{k}.json","w"),ensure_ascii=False,indent=1)
print(sum(len(s["say"]) for v in V.values() for s in v["scenes"]))
