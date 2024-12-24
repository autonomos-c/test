from mcp_gsuite_integration import GoogleCalendarIntegration
from mcp_gmail_integration import GmailIntegration
from langchain_community.tools import MCP
from mcp_gsuite_integration import GoogleCalendarIntegration
#!/usr/bin/env python3
"""
Specialized Team AI Assistant - Sistema de Equipos Profesionales de IA

Este módulo implementa un sistema de asistencia profesional basado en agentes 
especializados con capacidades de IA generativa. Integra herramientas externas
como Gmail, ClickUp y Google Drive para mejorar la eficiencia y funcionalidad
de los agentes especializados.

Características principales:
- Agentes especializados para diferentes áreas (CEO, Project Manager, R&D, etc.)
- Integración con Gmail para gestión de correos electrónicos
- Integración con ClickUp para gestión de tareas y proyectos
- Integración con Google Drive para almacenamiento y gestión de archivos
- Sistema de enrutamiento inteligente de consultas
- Uso de IA generativa para procesar y responder consultas

Requisitos:
- Python 3.7+
- Bibliotecas: langchain, langgraph, dotenv
- Credenciales configuradas para Gmail, ClickUp y Google Drive

Uso:
1. Configurar las variables de entorno necesarias en un archivo .env
2. Ejecutar el script: python specialized_team_ai_assistant.py
3. Ingresar consultas cuando se solicite

Nota: Asegúrese de manejar las credenciales de manera segura y no compartir
información sensible en entornos no seguros.
"""

import logging
import os
import json
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.agent_toolkits.clickup.toolkit import ClickupToolkit
from langchain_community.utilities.clickup import ClickupAPIWrapper
from langchain_community.tools import MCP

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno para las APIs
load_dotenv()

# Configurar las claves de API y credenciales
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS')
CLICKUP_API_KEY = os.getenv('CLICKUP_API_KEY')
GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv('GOOGLE_DRIVE_CREDENTIALS')

def load_json_credentials(path: str) -> Dict:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Archivo de credenciales no encontrado: {path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el archivo JSON: {path}")
        raise

if not all([GROQ_API_KEY, GMAIL_CREDENTIALS_PATH, CLICKUP_API_KEY, GOOGLE_DRIVE_CREDENTIALS_PATH]):
    logger.error("Faltan credenciales. Asegúrese de configurar todas las variables de entorno necesarias.")
    raise ValueError("Faltan credenciales. Asegúrese de configurar todas las variables de entorno necesarias.")

try:
    GMAIL_CREDENTIALS = load_json_credentials(GMAIL_CREDENTIALS_PATH)
    GOOGLE_DRIVE_CREDENTIALS = load_json_credentials(GOOGLE_DRIVE_CREDENTIALS_PATH)
except Exception as e:
    logger.error(f"Error al cargar las credenciales: {str(e)}")
    raise

# Inicializar el modelo Groq (usando LLaMA3 70b)
llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=GROQ_API_KEY,
    temperature=0.5,
    verbose=True
)

# Función para crear herramientas con retry
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_tool_with_retry(tool_class, **kwargs):
    try:
        return tool_class(**kwargs)
    except Exception as e:
        logger.error(f"Error al crear la herramienta {tool_class.__name__}: {str(e)}")
        raise

# Inicializar herramientas de mcp-gsuite
mcp_gsuite = MCP("mcp-gsuite")
gmail_tools = mcp_gsuite.get_tools_for_resource("gmail://")
google_drive_tools = mcp_gsuite.get_tools_for_resource("gdrive://")
google_calendar_tools = mcp_gsuite.get_tools_for_resource("gcalendar://")

# Initialize ClickUp API Wrapper and Toolkit
clickup_api_wrapper = ClickupAPIWrapper(access_token=CLICKUP_API_KEY)
clickup_toolkit = ClickupToolkit.from_clickup_api_wrapper(clickup_api_wrapper)
clickup_tools = clickup_toolkit.get_tools()

logger.info("Todas las herramientas han sido inicializadas correctamente.")


class TeamAssistantState:
    """Estado global del sistema de equipos especializados."""
    def __init__(self):
        self.query: str = ""
        self.category: str = ""
        self.response: str = ""
        self.metrics: Dict[str, Any] = {
            "response_time": 0,
            "accuracy": 0,
            "user_satisfaction": 0,
            "confidentiality_level": 0
        }
        self.confidential_mode: bool = False

class BaseSpecializedAgent:
    """Clase base para agentes especializados con herramientas comunes."""
    def __init__(self, llm, name: str):
        self.llm = llm
        self.name = name
        self.tools = [DuckDuckGoSearchResults()]
        self.tools.extend(gmail_tools)
        self.tools.extend(google_drive_tools)
        self.tools.extend(google_calendar_tools)
        self.tools.extend(clickup_tools)
        self.logger = logging.getLogger(f"{self.__class__.__name__}Logger")
        self.logger.setLevel(logging.INFO)

    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        """Método base para procesamiento de consultas."""
        raise NotImplementedError("Cada agente debe implementar su método de procesamiento")

    def get_tool(self, tool_name: str):
        """Obtiene una herramienta específica por nombre."""
        return next((tool for tool in self.tools if tool.name == tool_name), None)

class CEOCoordinator(BaseSpecializedAgent):
    """Agente coordinador para decisiones estratégicas de alto nivel."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        strategic_prompt = ChatPromptTemplate.from_template(
            "Analiza estratégicamente la siguiente consulta desde una perspectiva de liderazgo ejecutivo: {query}. "
            "Utiliza Gmail para comunicaciones importantes, ClickUp para asignar tareas estratégicas, "
            "Google Drive para almacenar documentos confidenciales y Google Calendar para programar reuniones importantes si es necesario."
        )
        chain = strategic_prompt | self.llm
        strategic_response = chain.invoke({"query": state.query})
        
        # Ejemplo de uso de herramientas
        if "enviar correo" in state.query.lower():
            gmail_tool = self.get_tool("gmail_send")
            if gmail_tool:
                gmail_tool.run({"to": "equipo@empresa.com", "subject": "Decisión Estratégica", "message": strategic_response.content})
        
        if "crear tarea" in state.query.lower():
            clickup_tool = self.get_tool("clickup_create_task")
            if clickup_tool:
                clickup_tool.run({"name": "Implementar estrategia", "description": strategic_response.content})
        
        if "almacenar documento" in state.query.lower():
            drive_tool = self.get_tool("gdrive_create_file")
            if drive_tool:
                drive_tool.run({"name": "Documento Estratégico.docx", "content": strategic_response.content})
        
        if "programar reunión" in state.query.lower():
            calendar_tool = self.get_tool("gcalendar_create_event")
            if calendar_tool:
                calendar_tool.run({"summary": "Reunión Estratégica", "description": strategic_response.content, "start_time": "2024-01-01T10:00:00", "end_time": "2024-01-01T11:00:00"})
        
        state.response = f"Análisis Estratégico: {strategic_response.content}"
        state.metrics['confidentiality_level'] = 0.9
        state.confidential_mode = True
        return state

class ProjectManager(BaseSpecializedAgent):
    """Agente para gestión y seguimiento de proyectos."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        project_prompt = ChatPromptTemplate.from_template(
            "Evalúa y planifica el siguiente proyecto o consulta: {query}. "
            "Utiliza ClickUp para crear y asignar tareas, Google Drive para almacenar documentos del proyecto, "
            "Gmail para comunicaciones relacionadas con el proyecto y Google Calendar para programar reuniones y plazos importantes."
        )
        chain = project_prompt | self.llm
        project_response = chain.invoke({"query": state.query})
        
        # Uso de herramientas
        clickup_tool = self.get_tool("clickup_create_task")
        if clickup_tool:
            clickup_tool.run({"name": "Nuevo Proyecto", "description": project_response.content})
        
        drive_tool = self.get_tool("gdrive_create_file")
        if drive_tool:
            file_id = drive_tool.run({"name": "Plan de Proyecto.docx", "content": project_response.content})
        
        gmail_tool = self.get_tool("gmail_create_draft")
        if gmail_tool:
            gmail_tool.run({"to": "equipo@empresa.com", "subject": "Nuevo Plan de Proyecto", "message": f"Se ha creado un nuevo plan de proyecto: {project_response.content}\nPuede acceder al documento aquí: https://drive.google.com/file/d/{file_id}"})
        
        calendar_tool = self.get_tool("gcalendar_create_event")
        if calendar_tool:
            calendar_tool.run({"summary": "Reunión de Inicio de Proyecto", "description": project_response.content, "start_time": "2024-01-02T09:00:00", "end_time": "2024-01-02T10:00:00"})
        
        state.response = f"Plan de Proyecto: {project_response.content}"
        state.metrics['accuracy'] = 0.85
        return state

class ResearchDevelopment(BaseSpecializedAgent):
    """Agente para investigación, análisis y desarrollo de soluciones innovadoras."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        research_prompt = ChatPromptTemplate.from_template(
            "Investiga y desarrolla soluciones innovadoras para: {query}. "
            "Utiliza Google Drive para almacenar documentos de investigación, "
            "ClickUp para gestionar tareas de investigación, Gmail para comunicar hallazgos importantes "
            "y Google Calendar para programar reuniones de seguimiento y presentaciones."
        )
        chain = research_prompt | self.llm
        research_response = chain.invoke({"query": state.query})
        
        # Uso de herramientas
        drive_tool = self.get_tool("gdrive_create_file")
        if drive_tool:
            file_id = drive_tool.run({"name": "Informe de Investigación.docx", "content": research_response.content})
        
        clickup_tool = self.get_tool("clickup_create_task")
        if clickup_tool:
            task_id = clickup_tool.run({"name": "Seguimiento de Investigación", "description": research_response.content})
        
        gmail_tool = self.get_tool("gmail_send")
        if gmail_tool:
            gmail_tool.run({
                "to": "equipo@empresa.com",
                "subject": "Nuevos Hallazgos de Investigación",
                "message": f"Se han realizado nuevos hallazgos en la investigación. Por favor, revisen el informe: https://drive.google.com/file/d/{file_id}\n"
                           f"Tarea de seguimiento creada en ClickUp: https://app.clickup.com/t/{task_id}"
            })
        
        calendar_tool = self.get_tool("gcalendar_create_event")
        if calendar_tool:
            calendar_tool.run({
                "summary": "Presentación de Hallazgos de Investigación",
                "description": f"Presentación de los hallazgos recientes: {research_response.content[:100]}...",
                "start_time": "2024-01-03T14:00:00",
                "end_time": "2024-01-03T15:00:00"
            })
        
        state.response = f"Hallazgos de I+D: {research_response.content}"
        state.metrics['accuracy'] = 0.95
        return state

class MarketingContent(BaseSpecializedAgent):
    """Agente para creación de contenido estratégico y marketing."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        marketing_prompt = ChatPromptTemplate.from_template(
            "Desarrolla una estrategia de contenido para: {query}. "
            "Utiliza Google Drive para almacenar materiales de marketing, "
            "ClickUp para gestionar campañas, Gmail para coordinar con el equipo de marketing "
            "y Google Calendar para programar reuniones de planificación y lanzamientos."
        )
        chain = marketing_prompt | self.llm
        marketing_response = chain.invoke({"query": state.query})
        
        # Uso de herramientas
        drive_tool = self.get_tool("gdrive_create_file")
        if drive_tool:
            file_id = drive_tool.run({"name": "Estrategia de Marketing.pptx", "content": marketing_response.content})
        
        clickup_tool = self.get_tool("clickup_create_task")
        if clickup_tool:
            task_id = clickup_tool.run({"name": "Nueva Campaña de Marketing", "description": marketing_response.content})
        
        gmail_tool = self.get_tool("gmail_create_draft")
        if gmail_tool:
            gmail_tool.run({
                "to": "marketing@empresa.com",
                "subject": "Nueva Estrategia de Contenido",
                "message": f"Se ha desarrollado una nueva estrategia de contenido. Por favor, revisen el documento: https://drive.google.com/file/d/{file_id}\n"
                           f"Tarea de campaña creada en ClickUp: https://app.clickup.com/t/{task_id}"
            })
        
        calendar_tool = self.get_tool("gcalendar_create_event")
        if calendar_tool:
            calendar_tool.run({
                "summary": "Reunión de Planificación de Campaña de Marketing",
                "description": f"Discusión de la nueva estrategia de contenido: {marketing_response.content[:100]}...",
                "start_time": "2024-01-04T10:00:00",
                "end_time": "2024-01-04T11:00:00"
            })
        
        state.response = f"Estrategia de Marketing: {marketing_response.content}"
        state.metrics['user_satisfaction'] = 0.85
        return state

class TechnicalDocumentation(BaseSpecializedAgent):
    """Agente para documentación técnica precisa y estructurada."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        doc_prompt = ChatPromptTemplate.from_template(
            "Genera documentación técnica detallada para: {query}. "
            "Utiliza Google Drive para almacenar y versionar la documentación, "
            "ClickUp para gestionar tareas de documentación, Gmail para solicitar revisiones "
            "y Google Calendar para programar reuniones de revisión y actualización de documentación."
        )
        chain = doc_prompt | self.llm
        doc_response = chain.invoke({"query": state.query})
        
        # Uso de herramientas
        drive_tool = self.get_tool("gdrive_create_file")
        if drive_tool:
            file_id = drive_tool.run({"name": "Documentación Técnica.md", "content": doc_response.content})
        
        clickup_tool = self.get_tool("clickup_create_task")
        if clickup_tool:
            task_id = clickup_tool.run({"name": "Revisión de Documentación", "description": f"Revisar nueva documentación técnica: https://drive.google.com/file/d/{file_id}"})
        
        gmail_tool = self.get_tool("gmail_send")
        if gmail_tool:
            gmail_tool.run({
                "to": "revisores@empresa.com",
                "subject": "Nueva Documentación Técnica para Revisión",
                "message": f"Por favor, revisen la nueva documentación técnica: https://drive.google.com/file/d/{file_id}\n"
                           f"Tarea de revisión creada en ClickUp: https://app.clickup.com/t/{task_id}"
            })
        
        calendar_tool = self.get_tool("gcalendar_create_event")
        if calendar_tool:
            calendar_tool.run({
                "summary": "Reunión de Revisión de Documentación Técnica",
                "description": f"Revisión de la nueva documentación técnica: {doc_response.content[:100]}...",
                "start_time": "2024-01-05T13:00:00",
                "end_time": "2024-01-05T14:00:00"
            })
        
        state.response = f"Documentación Técnica:\n{doc_response.content}"
        state.metrics['accuracy'] = 0.98
        return state

class CodeReview(BaseSpecializedAgent):
    """Agente para revisión de código, mejora de calidad y seguridad."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        code_review_prompt = ChatPromptTemplate.from_template(
            "Realiza una revisión de código crítica para: {query}. "
            "Identifica mejoras de seguridad, rendimiento y legibilidad. "
            "Utiliza ClickUp para crear tareas de mejora, Google Drive para almacenar informes de revisión, "
            "Gmail para notificar a los desarrolladores sobre los hallazgos "
            "y Google Calendar para programar reuniones de seguimiento y discusión de mejoras."
        )
        chain = code_review_prompt | self.llm
        review_response = chain.invoke({"query": state.query})
        
        # Uso de herramientas
        clickup_tool = self.get_tool("clickup_create_task")
        if clickup_tool:
            task_id = clickup_tool.run({"name": "Mejoras de Código", "description": review_response.content})
        
        drive_tool = self.get_tool("gdrive_create_file")
        if drive_tool:
            file_id = drive_tool.run({"name": "Informe de Revisión de Código.pdf", "content": review_response.content})
        
        gmail_tool = self.get_tool("gmail_send")
        if gmail_tool:
            gmail_tool.run({
                "to": "desarrolladores@empresa.com",
                "subject": "Resultados de Revisión de Código",
                "message": f"Se ha completado una revisión de código. Por favor, revisen el informe: https://drive.google.com/file/d/{file_id}\n"
                           f"Tarea de mejoras creada en ClickUp: https://app.clickup.com/t/{task_id}"
            })
        
        calendar_tool = self.get_tool("gcalendar_create_event")
        if calendar_tool:
            calendar_tool.run({
                "summary": "Reunión de Seguimiento de Revisión de Código",
                "description": f"Discusión de mejoras de código identificadas: {review_response.content[:100]}...",
                "start_time": "2024-01-06T11:00:00",
                "end_time": "2024-01-06T12:00:00"
            })
        
        state.response = f"Revisión de Código:\n{review_response.content}"
        state.metrics['code_quality'] = 0.95
        state.confidential_mode = True
        return state

class GmailAgent(BaseSpecializedAgent):
    """Agente para gestionar correos electrónicos con Gmail."""
    def __init__(self, llm, name: str):
        super().__init__(llm, name)
        self.tools.extend([GmailCreateDraft(), GmailSendMessage(), GmailSearch()])

    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        gmail_prompt = ChatPromptTemplate.from_template(
            "Gestiona la siguiente tarea de correo electrónico: {query}"
        )
        chain = gmail_prompt | self.llm
        gmail_response = chain.invoke({"query": state.query})
        
        state.response = f"Gestión de Gmail:\n{gmail_response.content}"
        return state

class ClickUpAgent(BaseSpecializedAgent):
    """Agente para gestionar tareas con ClickUp."""
    def __init__(self, llm, name: str):
        super().__init__(llm, name)
        self.tools.extend(clickup_tools)

    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        clickup_prompt = ChatPromptTemplate.from_template(
            "Gestiona la siguiente tarea en ClickUp: {query}"
        )
        chain = clickup_prompt | self.llm
        clickup_response = chain.invoke({"query": state.query})
        
        # Ejemplo de uso de herramientas ClickUp
        create_task_tool = next(tool for tool in self.tools if tool.name == "create_task")
        task_id = create_task_tool.run({"name": "Nueva tarea", "description": clickup_response.content})
        
        get_task_tool = next(tool for tool in self.tools if tool.name == "get_task")
        task_details = get_task_tool.run({"task_id": task_id})
        
        state.response = f"Gestión de ClickUp:\n{clickup_response.content}\nTarea creada: {task_details}"
        return state

class GoogleDriveAgent(BaseSpecializedAgent):
    """Agente para gestionar archivos en Google Drive."""
    def __init__(self, llm, name: str):
        super().__init__(llm, name)
        self.tools.extend([GoogleDriveCreateFile(), GoogleDriveListFiles(), GoogleDriveSearchFiles()])

    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        drive_prompt = ChatPromptTemplate.from_template(
            "Gestiona la siguiente tarea en Google Drive: {query}"
        )
        chain = drive_prompt | self.llm
        drive_response = chain.invoke({"query": state.query})
        
        state.response = f"Gestión de Google Drive:\n{drive_response.content}"
        return state

class SpecializedTeamAssistant:
    """Coordinador principal del sistema de equipos especializados."""
    def __init__(self, config: Dict[str, Any]):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=config.get('temperature', 0.5)
        )
        self.logger = self._setup_logging()
        self.agents = {
            'ceo_coordinator': CEOCoordinator(self.llm, "CEO Coordinator"),
            'project_manager': ProjectManager(self.llm, "Project Manager"),
            'research_development': ResearchDevelopment(self.llm, "R&D"),
            'marketing_content': MarketingContent(self.llm, "Marketing"),
            'technical_documentation': TechnicalDocumentation(self.llm, "Tech Docs"),
            'code_review': CodeReview(self.llm, "Code Review"),
            'gmail': GmailAgent(self.llm, "Gmail"),
            'clickup': ClickUpAgent(self.llm, "ClickUp"),
            'google_drive': GoogleDriveAgent(self.llm, "Google Drive")
        }
        self.shared_tools = {
            'gmail': [GmailCreateDraft(), GmailSendMessage(), GmailSearch()],
            'clickup': [ClickupCreateTask(), ClickupGetTask(), ClickupUpdateTask()],
            'google_drive': [GoogleDriveCreateFile(), GoogleDriveListFiles(), GoogleDriveSearchFiles()]
        }

    def _setup_logging(self):
        """Configurar sistema de logging robusto."""
        logger = logging.getLogger('SpecializedTeamAssistant')
        logger.setLevel(logging.INFO)
        return logger

    def route_query(self, state: TeamAssistantState):
        """Enrutamiento inteligente basado en categoría."""
        routing_strategies = {
            'strategic_planning': self.agents['ceo_coordinator'],
            'project_management': self.agents['project_manager'],
            'research_inquiry': self.agents['research_development'],
            'content_creation': self.agents['marketing_content'],
            'technical_documentation': self.agents['technical_documentation'],
            'code_quality': self.agents['code_review'],
            'email_management': self.agents['gmail'],
            'task_management': self.agents['clickup'],
            'file_management': self.agents['google_drive']
        }
        
        agent = routing_strategies.get(state.category, self.agents['ceo_coordinator'])
        
        # Añadir herramientas compartidas al agente seleccionado
        for tool_set in self.shared_tools.values():
            agent.tools.extend(tool_set)
        
        return agent.process_query(state)

def create_workflow():
    """Crear flujo de trabajo con LangGraph."""
    workflow = StateGraph(TeamAssistantState)
    
    workflow.add_node("route_query", SpecializedTeamAssistant(config={}).route_query)
    workflow.set_entry_point("route_query")
    workflow.add_edge("route_query", END)
    
    return workflow.compile()

def main():
    """Punto de entrada principal del sistema."""
    logging.basicConfig(level=logging.INFO)
    
    team_assistant = SpecializedTeamAssistant(config={
        'temperature': 0.5,
        'max_tokens': 4096
    })
    
    workflow = create_workflow()
    
    while True:
        query = input("Ingrese su consulta (o 'salir' para terminar): ")
        if query.lower() == 'salir':
            break
        
        state = TeamAssistantState()
        state.query = query
        
        result = workflow.invoke(state)
        print(result.response)

if __name__ == "__main__":
    main()
