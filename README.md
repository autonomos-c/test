# GenAI Career Assistant

## Descripción
Asistente de IA generativa avanzado para desarrollo profesional, utilizando Groq LLaMA3 y LangGraph.

## Características Principales
- Generación de tutoriales técnicos
- Sesiones de preguntas y respuestas interactivas
- Preparación de currículum vitae
- Simulación de entrevistas
- Búsqueda de empleos
- Flujo de trabajo adaptativo con LangGraph

## Tecnologías
- Groq LLaMA3 70b
- LangChain
- LangGraph
- DuckDuckGo Search
- Python 3.12+

## Dependencias
```bash
pip install groq langchain-groq python-dotenv langgraph \
             langchain-community duckduckgo-search
```

## Configuración
1. Crear archivo `.env` con clave de API de Groq
2. Ejecutar con `python career_assistant_full.py`

## Flujo de Trabajo
1. Categorización automática de consultas
2. Enrutamiento inteligente a agentes especializados
3. Generación de respuestas personalizadas

## Capacidades de Agentes
- **Recursos de Aprendizaje**: Tutoriales y Q&A sobre IA generativa
- **Currículum**: Creación y mejora de CV
- **Entrevistas**: Preguntas de práctica y simulaciones
- **Búsqueda de Trabajo**: Asistencia en encontrar oportunidades laborales

## Salida
- Archivos markdown generados en directorio `Agent_output/`
- Tutoriales, CV, preguntas de entrevista y resultados de búsqueda

## Ejemplos de Uso
- Generar tutorial sobre LangChain
- Crear CV para puesto de IA
- Practicar preguntas de entrevista técnica
- Buscar trabajos en IA generativa

## Próximas Mejoras
- Integración con más fuentes de datos
- Personalización avanzada de respuestas
- Soporte multilenguaje
