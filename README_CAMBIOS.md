# Migración de Gemini a Groq en GenAI Career Assistant

## Cambios Realizados
- Reemplazado `ChatGoogleGenerativeAI` por `ChatGroq`
- Cambiado modelo de Gemini a LLaMA3 70b
- Modificadas variables de entorno de Google a Groq
- Mantenida la configuración original de temperatura y verbosidad

## Dependencias Actualizadas
```bash
pip install groq langchain-groq python-dotenv langgraph
```

## Configuración de API
- Usar token de Groq en lugar de Google API Key
- Mantener la misma lógica de carga de variables de entorno

## Consideraciones
- El modelo LLaMA3 70b puede tener un comportamiento ligeramente diferente
- Rendimiento y capacidades pueden variar respecto a Gemini
