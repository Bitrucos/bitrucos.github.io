# Guion 19 alargado (19/11/2026) -> lines.json (subtítulos) + lines.txt (voz)
import json, re
S = [
"Las tres cuestan casi lo mismo: unos veinte dólares por mes. ChatGPT Plus, Claude Pro y Google AI Pro.",
"Y casi todo el mundo elige de la misma manera: paga la primera que conoció, o paga dos por si acaso. En los dos casos, muchas veces está pagando por algo que ya tenía gratis.",
"En los próximos ocho minutos vas a ver qué te da gratis cada una, qué hace mejor, cuánto cuesta y cuál elegir según para qué la usas. Y al final te dejo una prueba de diez minutos para decidir sin pagar nada.",
"Los precios y los planes los revisé en noviembre de 2026, en dólares, como los publica cada empresa en Estados Unidos. En tu país pueden cambiar.",
"Primero, lo gratis. Porque ahí se decide casi todo.",
"ChatGPT gratis te deja chatear con texto sin límite en el uso de todos los días. Lo que sí tiene tope es todo lo demás: subir archivos, crear imágenes, la investigación profunda y la memoria. Sirve para preguntar, escribir y aprender. El día que quieras analizar muchos documentos, ahí lo vas a sentir.",
"Claude gratis funciona distinto. Tiene un límite de uso que se renueva cada cinco horas y otro semanal. Incluye búsqueda en internet, memoria, creación de archivos y hasta cinco proyectos. Pero si le pegas textos largos, el límite llega rápido. Es la versión gratis donde más se nota que es gratis.",
"Gemini gratis usa, desde octubre, el modelo más liviano de Google. Te deja crear y editar imágenes, y trae investigación profunda incluida. Y tiene una ventaja que las otras dos no tienen: si usas Gmail, Drive y Documentos de Google, ya está ahí. No instalas nada.",
"Resumen de lo gratis: ChatGPT es la más generosa para conversar. Gemini, la más cómoda si vives en Google. Claude, la que se acaba más rápido.",
"Ahora, qué hace mejor cada una. Empiezo por ChatGPT. ChatGPT es la navaja suiza. Hace un poco de todo y lo hace bien: texto, imágenes, modo de voz, búsqueda en internet, análisis de archivos. Si nunca usaste IA y quieres una sola, es la que menos te va a frustrar al empezar, porque casi cualquier cosa que le pidas la intenta.",
"Un uso concreto: le sacas una foto a una factura o a un menú en otro idioma y le preguntas qué dice y qué te conviene.",
"Sus planes: Go, a ocho dólares por mes, sube los límites de imágenes, archivos y análisis de datos. Ojo con un detalle: OpenAI avisa que el plan Go puede incluir anuncios.",
"Plus, a veinte dólares, suma los modelos que razonan más, como GPT-6 Sol, agrega funciones como ChatGPT Work y Sites, y no tiene anuncios. Arriba hay planes Pro de cien, doscientos y quinientos dólares, pensados para gente que lo usa todo el día para trabajar.",
"El límite que más vas a notar: el modelo gratis no es el mismo que el pago. La versión gratis y Go usan GPT-6 Luna, que es rápido, pero razona menos que el modelo Sol.",
"Segunda: Claude. Claude es la que elegiría si escribes mucho o trabajas con documentos largos. Contratos, informes, una tesis, un manual de cuarenta páginas.",
"Por ejemplo, le subes tu contrato de alquiler y le preguntas: «¿Qué cláusulas me pueden costar dinero si me voy antes?». Te las marca una por una, con la parte del contrato donde está cada una.",
"Sus proyectos te dejan guardar tus archivos y tus instrucciones en un solo lugar, y cada chat nuevo arranca sabiendo de qué se trata. Si tienes un negocio chico, armas un proyecto con tu lista de precios y tres mensajes que ya escribiste. Desde ahí, cada respuesta a un cliente sale con tus precios y con tu forma de escribir.",
"Planes: Pro cuesta veinte dólares por mes, o diecisiete si pagas el año entero, que son doscientos dólares de una vez. Max cuesta cien dólares y te da cinco veces el uso de Pro. Y arriba de todo está Ultra, a doscientos dólares, con diez veces el uso semanal de Pro.",
"El límite: aunque pagues, el uso se mide en ventanas de cinco horas y con un tope semanal. Si te pasas una tarde entera mandándole documentos, puede frenarte hasta que se renueve. Si eso te pasa seguido, el problema no es la herramienta: es el plan.",
"Tercera: Gemini. Gemini es la que más sentido tiene si tu vida pasa por Google. Te resume un hilo largo de Gmail, busca un archivo en tu Drive o arma un borrador en Documentos, sin copiar y pegar nada.",
"Le puedes pedir, por ejemplo: «Busca en mi correo los mensajes de la aerolínea y dime a qué hora sale mi vuelo».",
"Y acá viene el dato que casi nadie mira. El plan Google AI Pro, de diecinueve con noventa y nueve por mes, incluye cinco terabytes de almacenamiento. Si ya pagas almacenamiento en Google para tus fotos, a lo mejor estás a un paso de tener la IA casi incluida.",
"Si quieres algo más barato, Google AI Plus cuesta cuatro con noventa y nueve: duplica el uso del plan gratis y trae cuatrocientos gigas de espacio. Pero ojo: desde el trece de noviembre, Plus ya no incluye el modelo Pro de Google. Para tenerlo, hay que pasar a AI Pro.",
"El límite: la versión gratis usa el modelo más liviano, y Plus tampoco tiene el Pro. En tareas difíciles se nota. Razonar un problema largo o revisar un documento técnico les cuesta más que al plan AI Pro.",
"Antes de elegir, dos errores que hacen pagar de más.",
"Uno: pagar por el nombre del modelo. Cada pocos meses sale uno nuevo con un nombre más grande. Si la versión gratis ya resuelve lo que haces, el modelo nuevo no te cambia la semana.",
"Dos: pagar el año entero el primer día. El plan anual es más barato por mes, pero si a los dos meses dejas de usarla, perdiste la diferencia. Y si pagas en dólares con tarjeta, fíjate si en tu país hay impuestos o recargos: el precio final puede ser más alto.",
"Ahora sí: cuál te conviene. Sin rodeos. Si la usas de vez en cuando, para preguntar algo o escribir un mensaje: no pagues. Empieza con ChatGPT gratis, que te deja chatear con texto sin límite.",
"Si vives en Gmail y Drive, o ya pagas almacenamiento en Google: Gemini. Prueba primero la gratis. Si solo te falta uso o espacio, Google AI Plus, a cuatro con noventa y nueve. Si necesitas que razone mejor, AI Pro, a diecinueve con noventa y nueve.",
"Si escribes mucho o trabajas con documentos largos: Claude Pro, veinte dólares. Es la que más tiempo te devuelve en ese tipo de trabajo. Si quieres una sola herramienta para todo, con imágenes y voz incluidas: ChatGPT Plus, veinte dólares.",
"Y si estás por pagar dos: casi nunca hace falta. Paga una y usa la versión gratis de otra como segunda opinión.",
"Te prometí una prueba para decidir sin gastar. Es esta. Abre las tres en su versión gratis, en tres pestañas, y dales exactamente los mismos tres pedidos.",
"Uno: un mensaje difícil de tu vida real. Por ejemplo: «Escríbele a mi jefe que no llego con el informe del viernes y propón una nueva fecha, en tono amable y sin poner excusas».",
"Dos: un documento tuyo. Sube un PDF del trabajo o del estudio y pídele: «Resúmelo en cinco puntos y dime qué parte no está clara».",
"Tres: un plan. «Organiza mi semana: trabajo de nueve a seis, gimnasio tres veces y media hora de inglés por día».",
"Después, hazte una sola pregunta con cada respuesta: ¿la usarías sin corregir nada? La que gane dos de tres es tu herramienta. No la que gana en internet: la que gana con tus tareas.",
"Y un consejo antes de pagar: paga primero un solo mes. Si a fin de mes la extrañas cada vez que se te acaban los mensajes, ahí sí piensa en el plan anual.",
"Cuéntame en los comentarios cuál usas hoy y para qué. En la descripción tienes mi guía gratis con diez trucos de IA. Y suscríbete a Bitrucos: cada martes y cada viernes, un video como este.",
]
SAY = [
 (r"ChatGPT Work y Sites", "Chat ge pe te Uork y Saits"),
 (r"GPT-6", "ge pe te seis"),
 (r"Google AI Pro", "Google ei ai Pro"), (r"Google AI Plus", "Google ei ai Plas"), (r"\bAI Pro\b", "ei ai Pro"),
 (r"\bPlus\b", "Plas"), (r"\bGo\b", "Gou"), (r"\bClaude\b", "Clod"), (r"\bGemini\b", "Yémini"),
 (r"\bGmail\b", "Yimeil"), (r"\bDrive\b", "Draiv"), (r"\bOpenAI\b", "Óupen ei ái"), (r"usaste IA", "usaste inteligencia artificial"), (r"tener la IA", "tener la inteligencia artificial"), (r"\bPDF\b", "pe de efe"),
 (r"\bIA\b", "i a"), (r"2026", "dos mil veintiséis"), (r"[«»]", ""),
]
def say(s):
    for a, b in SAY: s = re.sub(a, b, s)
    return s
def segs(s, mx=64):
    out, cur = [], ''
    for w in s.split(' '):
        if cur and len(cur) + 1 + len(w) > mx: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
        if cur.endswith(('.', ':', '?', '»', '».')) and len(cur) > 28: out.append(cur); cur = ''
    if cur: out.append(cur)
    i = 1
    while i < len(out):
        if len(out[i]) < 18 and len(out[i-1]) + 1 + len(out[i]) <= 80: out[i-1] += ' ' + out.pop(i)
        else: i += 1
    return out
lines = [{"scene": i + 1, "segs": segs(s)} for i, s in enumerate(S)]
if __name__ == '__main__':
    json.dump(lines, open('lines.json', 'w'), ensure_ascii=False, indent=0)
    open('lines.txt', 'w').write('\n'.join(say(s) for s in S) + '\n')
    print('escenas', len(S), 'palabras', sum(len(s.split()) for s in S))
