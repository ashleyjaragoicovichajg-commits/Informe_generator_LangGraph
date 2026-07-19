# agents/editor.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from state import InspectorState
from typing import Dict

# Cargar variables de entorno
load_dotenv()

# Inicializar el cliente compatible con OpenAI para DeepSeek
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def agente_editor(state: InspectorState) -> Dict:
    """Filtra redundancias, refina tecnicismos y diseña la estructura del informe usando DeepSeek."""
    print("\n--- [b] EJECUTANDO: Agente Editor (DeepSeek) ---")
    
    contexto = state["contexto_general_texto"]
    evidencias = state["evidencias_procesadas"]
    
    # 1. Preparar las evidencias en un formato de texto legible para el prompt
    detalles_evidencias = ""
    for idx, ev in enumerate(evidencias):
        detalles_evidencias += f"- Evidencia {idx+1} (Imagen: {ev['image_path']}): {ev['descripcion_audio']}\n"
    
    # 2. Diseñar el Prompt Técnico para DeepSeek
    prompt_sistema = (
        "Eres un Ingeniero Eléctrico Supervisor y Auditor Técnico experto. Tu trabajo es consolidar "
        "las notas de campo de una inspección, eliminar redundancias, corregir términos mal transcritos, "
        "y estructurar un informe técnico profesional y formal."
    )
    
    prompt_usuario = f"""
    A continuación tienes el contexto general de la inspección y las evidencias multimedia recolectadas.
    
    CONTEXTO GENERAL:
    {contexto}
    
    EVIDENCIAS Y ANOMALÍAS ENCONTRADAS:
    {detalles_evidencias}
    
    Por favor, genera dos elementos en tu respuesta utilizando un formato JSON estricto con las siguientes llaves:
    1. "secciones": Una lista con los títulos lógicos de las secciones del informe basados en los hallazgos (ej: ["Introducción", "Anomalías en Tableros", "Conclusiones"]).
    2. "contenido_depurado": El texto completo del informe redactado de manera formal, técnica y fluida, separando el contenido claramente para que corresponda a las secciones propuestas. No incluyas código LaTeX aquí, solo la redacción limpia.
    """

    # 3. Llamada a la API de DeepSeek
    # Tip: Usamos response_format JSON para obligar al modelo a estructurar el output
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat", # O "deepseek-reasoner" si prefieres el modelo R1 de razonamiento
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    
    # 4. Parsear la respuesta estructurada
    respuesta_json = json.loads(response.choices[0].message.content)
    
    # Construimos la estructura final asociando el orden de las imágenes
    estructura_final = {
        "secciones": respuesta_json.get("secciones", ["Introducción", "Hallazgos", "Conclusiones"]),
        "orden_imagenes": [e["image_path"] for e in evidencias]
    }
    
    contenido_final = respuesta_json.get("contenido_depurado", "Error al procesar el contenido.")
    
    return {
        "estructura_reporte": estructura_final,
        "contenido_depurado": contenido_final
    }