# Sistema de Equipos Especializados de IA

## Descripción
Sistema de asistencia profesional basado en agentes especializados con capacidades de IA generativa, utilizando Groq LLaMA3, LangGraph y herramientas externas.

## Características Principales
- Agentes especializados para diferentes áreas (CEO, Project Manager, R&D, etc.)
- Integración con Gmail para gestión de correos electrónicos
- Integración con ClickUp para gestión de tareas y proyectos
- Integración con Google Drive para almacenamiento y gestión de archivos
- Sistema de enrutamiento inteligente de consultas
- Uso de IA generativa para procesar y responder consultas
- Flujo de trabajo adaptativo con LangGraph

## Tecnologías
- Groq LLaMA3 70b
- LangChain
- LangGraph
- DuckDuckGo Search
- Gmail API
- ClickUp API
- Google Drive API
- Python 3.7+

## Dependencias
```bash
pip install groq langchain-groq python-dotenv langgraph \
             langchain-community duckduckgo-search \
             google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Configuración
1. Cree un archivo `.env` en el directorio raíz del proyecto con las siguientes claves:
   ```
   GROQ_API_KEY=your_groq_api_key
   GMAIL_CREDENTIALS=path_to_your_gmail_credentials.json
   CLICKUP_API_KEY=your_clickup_api_key
   GOOGLE_DRIVE_CREDENTIALS=path_to_your_google_drive_credentials.json
   ```

2. Configurar las credenciales para Gmail y Google Drive:
   a. Vaya a [Google Cloud Console](https://console.cloud.google.com/)
   b. Cree un nuevo proyecto o seleccione uno existente
   c. Habilite las APIs de Gmail y Google Drive para su proyecto
   d. Cree credenciales de tipo "OAuth 2.0 Client IDs" para una aplicación de escritorio
   e. Descargue el archivo JSON de credenciales y guárdelo en un lugar seguro
   f. Actualice las rutas en el archivo `.env` para apuntar a estos archivos JSON

3. Obtener la API key de ClickUp:
   a. Inicie sesión en su cuenta de ClickUp
   b. Vaya a la configuración de su perfil
   c. En la sección "Apps", genere una nueva API key
   d. Copie esta key y péguela en el archivo `.env`

4. Instale las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución
- Para ejecutar el asistente principal:
  ```
  python specialized_team_ai_assistant.py
  ```
- Para ejecutar las pruebas:
  ```
  python test_specialized_team_ai_assistant.py
  ```
- Para ver un ejemplo de uso:
  ```
  python example_usage.py
  ```

## Notas importantes
- Asegúrese de que todas las credenciales estén correctamente configuradas antes de ejecutar el sistema.
- El sistema utiliza logging para proporcionar información sobre su funcionamiento. Revise los logs para obtener más detalles sobre la ejecución.
- Si encuentra errores relacionados con las credenciales, verifique que los archivos JSON y las API keys sean válidos y estén actualizados.

## Flujo de Trabajo
1. Categorización automática de consultas
2. Enrutamiento inteligente a agentes especializados
3. Generación de respuestas personalizadas
4. Integración con herramientas externas según sea necesario

## Capacidades de Agentes
- **CEO Coordinator**: Decisiones estratégicas de alto nivel
- **Project Manager**: Gestión y seguimiento de proyectos
- **Research & Development**: Investigación y desarrollo de soluciones innovadoras
- **Marketing Content**: Creación de contenido estratégico y marketing
- **Technical Documentation**: Documentación técnica precisa y estructurada
- **Code Review**: Revisión de código, mejora de calidad y seguridad
- **Gmail Agent**: Gestión de correos electrónicos
- **ClickUp Agent**: Gestión de tareas y proyectos
- **Google Drive Agent**: Gestión de archivos y documentos

## Salida
- Respuestas generadas por los agentes especializados
- Acciones realizadas en Gmail, ClickUp y Google Drive
- Informes de pruebas en formato markdown

## Ejemplos de Uso
- Desarrollar estrategia de expansión para una startup de IA
- Planificar el desarrollo de una nueva aplicación
- Investigar tendencias en IA generativa
- Crear una campaña de marketing para un producto de IA
- Generar documentación técnica para una API
- Revisar código de un algoritmo de machine learning
- Enviar correos electrónicos importantes
- Crear y gestionar tareas en ClickUp
- Almacenar y organizar documentos en Google Drive

## Próximas Mejoras
- Integración con más herramientas y APIs
- Mejora en la personalización de respuestas
- Implementación de un sistema de aprendizaje continuo
- Soporte para más idiomas
