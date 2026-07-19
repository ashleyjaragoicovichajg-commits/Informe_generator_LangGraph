# agents/escritor.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from state import InspectorState
from typing import Dict

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de DeepSeek
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def agente_escritor(state: InspectorState) -> Dict:
    """[c] Toma el contenido del editor y lo transforma a un documento LaTeX válido."""
    print("\n--- [c] EJECUTANDO: Agente Escritor (DeepSeek LaTeX) ---")
    
    estructura = state["estructura_reporte"]
    contenido = state["contenido_depurado"]
    
    # Mapeo de imágenes disponibles por si el LLM necesita referenciarlas
    imagenes_disponibles = estructura.get("orden_imagenes", [])
    secciones_propuestas = estructura.get("secciones", [])

    prompt_sistema = (
        "Eres un compilador experto en LaTeX y maquetador de informes de ingeniería eléctrica. "
        "Tu única tarea es transformar el texto y la estructura proporcionada en un código de LaTeX "
        "completamente limpio, válido y listo para compilar. No agregues introducciones ni texto fuera del bloque de código."
    )
    
    prompt_usuario = f"""
    Genera el código LaTeX para un informe técnico basado en los siguientes datos:
    
    SECCIONES PROPUESTAS:
    {secciones_propuestas}
    
    CONTENIDO REDACTADO:
    {contenido}
    
    RUTAS DE IMÁGENES DISPONIBLES (Insértalas en las secciones correspondientes usando \\begin{{figure}}):
    {imagenes_disponibles}
    
    REQUISITOS ESTRICTOS DE LATEX:
    1. Usa la clase \\documentclass{{article}}.
    2. Incluye los paquetes esenciales: \\usepackage{{graphicx}}, \\usepackage{{geometry}}, \\usepackage{{hyperref}}.
    3. Asegúrate de ESCAPAR caracteres especiales que arruinen la compilación (como '_', '%', '&') si aparecen en el texto.
    4. Devuelve ÚNICAMENTE el código LaTeX puro, envuelto en un bloque de código markdown de tipo ```latex.
    """

    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.2
    )
    
    raw_latex = response.choices[0].message.content
    
    # Limpiar el formato markdown si el modelo lo incluye
    if "```latex" in raw_latex:
        raw_latex = raw_latex.split("```latex")[1].split("```")[0].strip()
    elif "```" in raw_latex:
        raw_latex = raw_latex.split("```")[1].split("```")[0].strip()

    return {
        "codigo_latex": raw_latex
    }