# state.py
from typing import TypedDict, List, Dict

class InspectorState(TypedDict):
    # Inputs iniciales suministrados por el usuario
    audio_general: str               # Path o bytes del audio general
    elementos_multimedia: List[Dict] # Lista de dicts: [{'image_path': '...', 'audio_path': '...'}]
    
    # Procesado por Agente Transcriptor
    contexto_general_texto: str      # Transcripción del audio de contexto [cite: 17]
    evidencias_procesadas: List[Dict] # Evidencias con su texto asociado [cite: 17]
    
    # Procesado por Agente Editor
    estructura_reporte: Dict          # Plan estratégico de secciones [cite: 23]
    contenido_depurado: str          # Texto final redactado formalmente [cite: 23]
    
    # Procesado por Agente Escritor
    codigo_latex: str                # Código LaTeX final generado [cite: 29]