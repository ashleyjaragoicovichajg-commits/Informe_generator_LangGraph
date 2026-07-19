informe_inspector/
│
├── state.py               # Definición del estado compartido del grafo
├── graph.py               # Orquestación y construcción del Grafo (LangGraph)
├── main.py                # Punto de entrada de la aplicación
│
└── agents/                # Módulo independiente para los agentes
    ├── __init__.py
    ├── transcriptor.py    # Nodo del Agente Transcriptor [a]
    ├── editor.py          # Nodo del Agente Editor [b]
    └── escritor.py        # Nodo del Agente Escritor [c]