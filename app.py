from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import TypedDict, List
import openai   # Transcripción Whisper
from tkinter import Tk, filedialog
import os

from settings import *
from prompts import *
from config import OPENAI_API_KEY

llm = ChatOpenAI(
    model = IA_MODEL,
    temperature = TEMPERATURE_IA
)


class State( TypedDict ):
    notes : str                 # Texto Original
    participants : List[str]    # Participantes identificados
    topics : List[str]          # Temas principales
    action_items : List[str]   # Acciones y responsables
    minutes : str               # Minuta formal
    summary : str               # Resumen ejecutivo


participants_prompt = PromptTemplate.from_template(
    PROMPT_EXTRACT_PARTICIPANTS
)

topics_prompt = PromptTemplate.from_template(
    PROMPT_IDENTIFY_TOPICS
)

actions_prompt = PromptTemplate.from_template(
    PROMPT_EXTRACT_ACTIONS
)

minutes_prompt = PromptTemplate.from_template(
    PROMPT_GENERATE_MINUTES
)

summary_prompt = PromptTemplate.from_template(
    PROMPT_CREATE_SUMMARY
)

def extract_participants( state ) -> State:
    prompt = participants_prompt.format(
        notes = state["notes"]
    )

    response = llm.invoke( prompt )
    participants = [p.strip() for p in response.content.split( ',' ) if p.strip()]

    print(f"Participantes extraidos: {len(participants)} personas")

    return {
        'participants': participants 
        }

def identify_topics( state ) -> State:  
    prompt = topics_prompt.format(
        notes = state["notes"]
    )

    response = llm.invoke( prompt )
    topics = [t.strip() for t in response.content.split( ";" ) if t.strip()]

    print(f"Temas obtenidos: {len(topics)}")

    return {
        'topics': topics
        }

def extract_actions( state )-> State:
    prompt = actions_prompt.format(
        notes = state["notes"]
    )
    response = llm.invoke( prompt )

    if "No se identificaron" in response.content:
        actions = []
    else:
        actions = [a.strip() for a in response.content.split( "|" ) if a.strip()]

    print(f"Acciones obtenidas: {len(actions)}")
    
    return {
        'action_items': actions
        }

def generate_minutes( state )-> State:
    participants_str = ", ".join(state["participants"])
    topics_str = "\n ".join(state["topics"])
    actions_str = "\n ".join(state["action_items"]) if state["action_items"] else "No se identificaron"

    prompt = minutes_prompt.format(
        participants_str = participants_str,
        topics_str = topics_str,
        actions_str = actions_str,
        notes = state["notes"]
    )

    response = llm.invoke( prompt )

    return {
        "minutes": response.content
        }

def create_summary( state )-> State:
    participants_str = ", ".join(state["participants"])
    topics_str = "\n ".join(state["topics"])
    actions_str = "n ".join(state["action_items"]) if state["action_items"] else "No se identificaron"
    
    prompt = summary_prompt.format(
        participants_str = participants_str,
        topics_str = topics_str,
        actions_str = actions_str,
        notes = state["notes"]
    )

    response = llm.invoke( prompt )

    return {
        "summary": response.content
        }

def create_workflow():
    workflow = StateGraph( State )
    workflow.add_node( "Participants", extract_participants)
    workflow.add_node( "Topics", identify_topics )
    workflow.add_node( "Actions", extract_actions )
    workflow.add_node( "Minutes", generate_minutes )
    workflow.add_node( "Summary", create_summary )

    workflow.add_edge(
        START,
        "Participants"
    )
    workflow.add_edge(
        "Participants",
        "Topics"
    )
    workflow.add_edge(
        "Topics",
        "Actions"
    )
    workflow.add_edge(
        "Actions",
        "Minutes"
    )
    workflow.add_edge(
        "Minutes",
        "Summary"
    )
    workflow.add_edge(
        "Summary",
        END
    )

    return workflow.compile()



def transcribe_media( file_path: str) -> str:

    try: 
        client = openai.OpenAI()

        with open( file_path, "rb" ) as audio_file:
            transcript = client.audio.transcriptions.create(
                model = WHISPER_MODEL,
                file = audio_file,
                language = "es",
                prompt = "Esta es una reunión de trabajo en español con múltiples participantes",
                response_format = "text"
            )

        return transcript
    
    except Exception as e:
        print(f"Error en la transcripcion: {e}")
        return f"Error: {str(e)}"
    
def process_meeting_notes( notes: str, app ):
    """Procesa una nota de reunión individual"""
    initial_state = {
        'notes': notes,
        'participants': [],
        'topics': [],
        'action_items': [],
        'minutes': '',
        'summary': '',
    }

    print("\n" + "=" * 60)
    print("Procesando nota de reunión...")
    print("=" * 60)

    result = app.invoke( initial_state )
    return result

def display_results( result: State, meeting_num: int):
    """Muestra los resultados de forma estrucurada"""
    print(f"\n RESULTADOS - REUNIÓN #{meeting_num}")
    print("-" * 60)

    print(f"\n Participantes ({len(result['participants'])}):")
    for p in result['participants']:
        print(f"    -{p}")
    
    print(f"\n Temas tratados ({len(result['topics'])}):")
    for t in result['topics']:
        print(f"    -{t}")

    print(f"\n Acciones acordadas ({len(result['action_items'])}):")
    if result['action_items']:
        for a in result['action_items']:
            print(f"    -{a}")
    else:
        print(" - No se definieron acciones específicas")

    print(f"\n Minuta formal:")
    print("-" * 40)
    print(result['minutes'])
    print("-" * 40)

    print(f"\n Resumen ejecutivo: ")
    print("-" * 40)
    print(f"    {result['summary']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    app = create_workflow()

    # Interfaz gráfica: Selector de archivos
    Tk().withdraw()
    file = filedialog.askopenfile(
        title = "Selecciona un video o una transcripción",
        filetypes = [
            ("Video/Audio", "*.mp4 *.mov *.m4a *.mp3 *.wav *.mkv *.webm"),
            ("Texto", "*.txt *.md")
        ]
    )

    if not file:
        print( "No se seleccionó archivo." )
        raise SystemExit(0)
    
    file_path = file.name
    
    ext = os.path.splitext( file_path )[1].lower()
    media_exts = {".mp4", ".mov", ".m4a", ".mp3", ".wav", ".mkv", ".webm"}

    if ext in media_exts:
        notes = transcribe_media( file_path )
    else: 
        notes = file.read()
        '''with open( file_path, "r", encoding = "utf-8", errors = "ignore") as f:
            notes = f.read()'''

    result = process_meeting_notes( notes, app )
    display_results( result, 1 )


    



