# graph.py
from langgraph.graph import StateGraph, END
from state import InspectorState
from agents.transcriptor import agente_transcriptor
from agents.editor import agente_editor
from agents.escritor import agente_escritor

def construir_grafo():
    # Inicializamos el flujo basado en nuestro State personalizado
    workflow = StateGraph(InspectorState)
    
    # 1. Añadir los Nodos al Grafo [cite: 4]
    workflow.add_node("transcriptor", agente_transcriptor)
    workflow.add_node("editor", agente_editor)
    workflow.add_node("escritor", agente_escritor)
    
    # 2. Definir las Conexiones (Flujo Lineal en este caso) [cite: 30]
    workflow.set_entry_point("transcriptor")
    workflow.add_edge("transcriptor", "editor")
    workflow.add_edge("editor", "escritor")
    workflow.add_edge("escritor", END)
    
    # Compilar el grafo listo para ser usado
    return workflow.compile()