# agents/transcriptor.py
import os
from typing import Dict
from groq import Groq
from dotenv import load_dotenv
from state import InspectorState

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _transcribir_audio(file_path: str) -> str:
    """Función helper para transcribir un archivo de audio usando Whisper en Groq."""
    if not os.path.exists(file_path):
        return f"[Error: Archivo de audio no encontrado en {file_path}]"
        
    with open(file_path, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3", # O el modelo de Whisper disponible en Groq
            response_format="text"
        )
    return str(transcription)

import base64

def _analizar_imagen_con_contexto(image_path: str, contexto_audio: str) -> str:
    """Utiliza el modelo Llama Vision de Groq para auditar la imagen junto a su transcripción."""
    if not os.path.exists(image_path):
        return f"[Error: Imagen no encontrada en {image_path}]"

    # 1. Función interna para codificar la imagen local a Base64
    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    try:
        base64_image = encode_image(image_path)
        
        # 2. Estructuración estricta del contenido para la API Multimodal de Groq
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",  # Asegúrate de usar el modelo de visión correcto
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Analiza detalladamente esta imagen de inspección técnica.\n"
                                f"Contexto proporcionado por el inspector en audio: '{contexto_audio}'.\n"
                                f"Describe de forma profesional qué anomalías o fallas de ingeniería "
                                f"puedes confirmar o complementar basándote en lo que se ve visualmente."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error al analizar imagen con Groq Vision: {str(e)}]"
    
def agente_transcriptor(state: InspectorState) -> Dict:
    """[a] Agente Transcriptor conectado a servicios de IA mediante Groq."""
    print("\n--- [a] EJECUTANDO: Agente Transcriptor (Groq) ---")
    
    audio_gen_path = state["audio_general"]
    elementos_multimedia = state["elementos_multimedia"]
    
    # 1. Transcribir el audio general de contexto
    print("Transcribiendo audio general...")
    contexto_texto = _transcribir_audio(audio_gen_path) 
    
    # 2. Procesar las evidencias de forma iterativa
    evidencias_procesadas = [] 
    for idx, elemento in enumerate(elementos_multimedia):
        img_path = elemento["image_path"] 
        aud_path = elemento["audio_path"] 
        
        print(f"Procesando evidencia {idx + 1}: Transcribiendo audio de soporte...")
        # Transcribir la descripción en audio que acompaña a la imagen
        texto_audio_incidente = _transcribir_audio(aud_path) 
        
        print(f"Procesando evidencia {idx + 1}: Analizando imagen con modelo visual...")
        # Cruzar la imagen con el texto transcrito para obtener una descripción de ingeniería impecable
        descripcion_final_evidencia = _analizar_imagen_con_contexto(img_path, texto_audio_incidente) 
        
        evidencias_procesadas.append({
            "image_path": img_path,
            "descripcion_audio": descripcion_final_evidencia  # Contiene la fusión de audio + visión
        })
        
    return {
        "contexto_general_texto": contexto_texto,
        "evidencias_procesadas": evidencias_procesadas
    }