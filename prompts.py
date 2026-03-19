PROMPT_EXTRACT_PARTICIPANTS = """ Analiza las siguientes notas de reunión y extrae únicamente los nombres de los participantes.

Notas:
{notes}

Instrucciones:
- Extrae solo nombres de personas (no roles, cargos ni empresas).
- Elimina duplicados.
- Corrige errores obvios de escritura si es claro el nombre.
- Si un nombre está incompleto pero es identificable, inclúyelo.
- Ignora palabras que no sean nombres propios.

Formato de salida:
- Una sola línea
- Nombres separados por coma y espacio

Ejemplo:
Ricardo Perez, Taki Mugway, Ana Garduño

No agregues explicaciones ni texto adicional.

"""

PROMPT_IDENTIFY_TOPICS = """ Analiza las siguientes notas de reunión e identifica los temas principales tratados.

Notas:
{notes}

Instrucciones:
- Extrae únicamente los temas principales discutidos en la reunión.
- Cada tema debe ser una frase corta y clara.
- Evita explicaciones o descripciones largas.
- No repitas temas similares.
- Máximo 8 temas.
- Ignora saludos, comentarios sociales o texto irrelevante.
- Si un tema aparece varias veces en las notas, inclúyelo solo una vez.

Formato de salida:
- Una sola línea
- Temas separados por punto y coma (;)

Ejemplo:
Plan de lanzamiento del producto; Problemas en el sistema de pagos; Estrategia de marketing; Seguimiento de clientes

No agregues explicaciones ni texto adicional.
"""

PROMPT_EXTRACT_ACTIONS = """Analiza las siguientes notas de reunión y extrae las acciones o tareas acordadas.

Notas:
{notes}

Instrucciones:
- Extrae únicamente acciones concretas (tareas que alguien debe realizar).
- Cada acción debe iniciar con un verbo en infinitivo (ej. "Enviar", "Revisar", "Crear").
- No incluyas discusiones, ideas o contexto, solo acciones ejecutables.
- No repitas acciones similares.

Formato de salida:
- Una sola línea
- Acciones separadas por |

Ejemplo:
Enviar reporte mensual a finanzas | Revisar errores del sistema de pagos | Crear propuesta de marketing

Si no hay acciones claras, responde con: "No se identificaron acciones específicas"

No agregues explicaciones ni texto adicional.
"""

PROMPT_GENERATE_MINUTES = """Genera una minuta de reunión clara, profesional y estructurada utilizando la siguiente información:

Participantes:
{participants_str}

Temas tratados:
{topics_str}

Acciones:
{actions_str}

Notas originales:
{notes}

Instrucciones:
- Redacta de forma clara, concisa y formal.
- Usa los participantes, temas y acciones como fuente principal.
- Usa las notas originales solo para complementar si hace falta contexto.
- No inventes información.
- No repitas información innecesariamente.
- Mantén consistencia entre secciones.

Estructura de salida:

Minuta de reunión

Participantes:
[Lista de participantes separados por coma]

Temas tratados:
[Lista de temas separados por coma]

Acuerdos:
[Lista breve de acuerdos separados por coma]

Acciones:
[Lista de acciones separadas por coma]

Formato:
- Respeta exactamente los encabezados mostrados.
- No agregues texto fuera de esta estructura.
- No dejes secciones vacías; si no hay información, escribe "No especificado".

No agregues explicaciones ni texto adicional.
"""

PROMPT_CREATE_SUMMARY = """Genera un resumen ejecutivo breve y claro de la reunión utilizando la siguiente información:

Participantes:
{participants_str}

Temas tratados:
{topics_str}

Acciones:
{actions_str}

Notas originales:
{notes}

Instrucciones:
- Máximo 5 líneas.
- Redacta en tono profesional y directo.
- Resume los puntos más importantes de la reunión.
- Destaca decisiones clave y acciones relevantes.
- Usa principalmente temas y acciones como base.
- Usa las notas solo para complementar contexto si es necesario.
- No inventes información.

Formato de salida:
- Un solo párrafo
- Sin saltos de línea
- Sin encabezados

No agregues explicaciones ni texto adicional.
"""