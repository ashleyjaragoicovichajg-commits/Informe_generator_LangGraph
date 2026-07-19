# main.py
from graph import construir_grafo

def main():
    print("Iniciando Sistema de Generación de Informes Técnicos...")
    
    # 1. Definimos los inputs simulados del inspector en terreno
    inputs_iniciales = {
        "audio_general": "recursos/audio_general.ogg",
        "elementos_multimedia": [
            {"image_path": "recursos/imagen_1.jpeg", "audio_path": "recursos/audio_1.ogg"},
            {"image_path": "recursos/imagen_2.jpeg", "audio_path": "recursos/audio_2.ogg"}
        ]
    }
    
    # 2. Construimos y ejecutamos el grafo
    app = construir_grafo()
    resultado_final = app.invoke(inputs_iniciales)
    
    # 3. Output final obtenido del último agente
    print("\n--- PROCESO FINALIZADO CON ÉXITO ---")
    print("Código LaTeX Generado:")
    print(resultado_final["codigo_latex"])
    
    # Aquí podrías opcionalmente guardar el archivo .tex o enviarlo a compilar a PDF
    with open("informe_final.tex", "w", encoding="utf-8") as f:
        f.write(resultado_final["codigo_latex"])

if __name__ == "__main__":
    main()