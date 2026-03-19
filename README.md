# 🧠 Sistema de Procesamiento de Reuniones con IA y LangGraph

Este proyecto implementa un sistema inteligente para procesar reuniones a partir de audio, video o texto utilizando modelos de lenguaje (LLMs) y LangGraph.

El sistema es capaz de:
- Transcribir reuniones (audio/video → texto)
- Extraer participantes
- Identificar temas principales
- Detectar acciones o tareas
- Generar una minuta formal
- Crear un resumen ejecutivo

---

## 🚀 Tecnologías utilizadas

- Python 3.12
- LangGraph
- LangChain
- OpenAI (GPT + Whisper)
- Tkinter (selector de archivos)
- dotenv

---

## 📂 Estructura del proyecto

├── app.py # Punto de entrada principal
├── prompts.py # Prompts estructurados
├── settings.py # Configuración de modelos
├── .env # Variables de entorno
├── README.md

---

## ⚙️ Instalación

1. Clona el repositorio:
2. Crea un entorno virtual
  python -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows
3. Instala las dependencias
   pip install -r requirements.txt
4. Configura tu archivo .env:
   OPENAI_API_KEY=tu_api_key_aqui

---
▶️ Uso
Ejecuta la aplicación:
python app.py
Se abrirá un selector de archivos donde puedes elegir:
🎥 Video (.mp4, .mov, etc.)
🎧 Audio (.mp3, .wav, etc.)
📄 Texto (.txt, .md)

---
🔄 Flujo del sistema
El sistema utiliza LangGraph para ejecutar un pipeline estructurado:
Notas → Participantes → Temas → Acciones → Minuta → Resumen

---
🧩 Estado del sistema (State)
class State(TypedDict):
    notes: str
    participants: List[str]
    topics: List[str]
    action_items: List[str]
    minutes: str
    summary: str

---
🧠 Funcionalidades principales

🎙️ Transcripción automática
Convierte audio/video a texto usando Whisper.

👥 Extracción de participantes
Identifica nombres dentro de las notas.

🧠 Identificación de temas
Detecta los temas principales discutidos.

✅ Extracción de acciones
Encuentra tareas concretas acordadas.

📝 Generación de minuta
Crea una minuta profesional estructurada.

📊 Resumen ejecutivo
Genera un resumen claro y conciso.

---
📌 Ejemplo de salida
Participantes:
- Juan Pérez
- Ana López

Temas:
- Estrategia de marketing
- Problemas técnicos

Acciones:
- Revisar sistema de pagos
- Enviar reporte mensual

Minuta:
[Texto estructurado...]

Resumen:
[Resumen ejecutivo...]



