#!/usr/bin/env python3
"""
Script de pruebas para el Sistema de Equipos Especializados de IA
"""

import sys
import os
import logging
import pytest
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from functools import wraps

# Añadir el directorio padre al path para importar el módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from specialized_team_ai_assistant import SpecializedTeamAssistant, TeamAssistantState
from unittest.mock import patch, MagicMock

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_md_report(test_name, queries, results):
    """Genera un informe markdown para cada prueba."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"test_report_{test_name}_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Informe de Prueba: {test_name}\n\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for query, result in zip(queries, results):
            f.write(f"## Consulta: {query}\n\n")
            f.write(f"### Respuesta:\n{result.response}\n\n")
            f.write("### Métricas:\n")
            for metric, value in result.metrics.items():
                f.write(f"- {metric}: {value}\n")
            f.write("\n---\n\n")
    
    logger.info(f"Informe generado: {filename}")

# Cargar variables de entorno para las APIs
load_dotenv()

# Configurar las claves de API y credenciales
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GMAIL_CREDENTIALS = os.getenv('GMAIL_CREDENTIALS')
CLICKUP_API_KEY = os.getenv('CLICKUP_API_KEY')
GOOGLE_DRIVE_CREDENTIALS = os.getenv('GOOGLE_DRIVE_CREDENTIALS')

if not all([GROQ_API_KEY, GMAIL_CREDENTIALS, CLICKUP_API_KEY, GOOGLE_DRIVE_CREDENTIALS]):
    logger.error("Faltan credenciales. Asegúrese de configurar todas las variables de entorno necesarias.")
    raise ValueError("Faltan credenciales. Asegúrese de configurar todas las variables de entorno necesarias.")

# Inicializar el modelo Groq (usando LLaMA3 70b)
llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=GROQ_API_KEY,
    temperature=0.5,
    verbose=True
)

# Mock de herramientas externas para pruebas
mock_gmail_tool = MagicMock()
mock_clickup_tool = MagicMock()
mock_google_drive_tool = MagicMock()

def test_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Iniciando prueba: {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Prueba completada: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error en la prueba {func.__name__}: {str(e)}")
            raise
    return wrapper

@patch('specialized_team_ai_assistant.GmailSendMessage', return_value=mock_gmail_tool)
@patch('specialized_team_ai_assistant.ClickupCreateTask', return_value=mock_clickup_tool)
@patch('specialized_team_ai_assistant.GoogleDriveCreateFile', return_value=mock_google_drive_tool)
@test_decorator
def test_ceo_coordinator():
    """Prueba del agente coordinador CEO."""
    print("\n--- Prueba de Coordinador CEO ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Desarrollar estrategia de expansión para una startup de IA",
        "Analizar riesgos en un nuevo proyecto tecnológico"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'strategic_planning'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Métricas de Confidencialidad: {result.metrics['confidentiality_level']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['confidentiality_level'] > 0.8, "El nivel de confidencialidad debe ser alto"
    
    generate_md_report("CEO_Coordinator", test_queries, results)

@test_decorator
def test_project_manager():
    """Prueba del agente de gestión de proyectos."""
    print("\n--- Prueba de Gestor de Proyectos ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Planificar desarrollo de una aplicación de IA para recursos humanos",
        "Definir metodología de gestión para un proyecto de transformación digital"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'project_management'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Precisión: {result.metrics['accuracy']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['accuracy'] > 0.7, "La precisión debe ser alta"
    
    generate_md_report("Project_Manager", test_queries, results)

@test_decorator
def test_research_development():
    """Prueba del agente de investigación y desarrollo."""
    print("\n--- Prueba de Investigación y Desarrollo ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Investigar nuevas tendencias en inteligencia artificial generativa",
        "Desarrollar solución innovadora para optimización de procesos empresariales"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'research_inquiry'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Precisión de Investigación: {result.metrics['accuracy']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['accuracy'] > 0.8, "La precisión de investigación debe ser muy alta"
    
    generate_md_report("Research_Development", test_queries, results)

@test_decorator
def test_marketing_content():
    """Prueba del agente de marketing y contenido."""
    print("\n--- Prueba de Marketing y Contenido ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Crear estrategia de contenido para campaña de lanzamiento de producto de IA",
        "Desarrollar narrativa de marketing para startup tecnológica"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'content_creation'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Satisfacción del Usuario: {result.metrics['user_satisfaction']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['user_satisfaction'] > 0.7, "La satisfacción del usuario debe ser alta"
    
    generate_md_report("Marketing_Content", test_queries, results)

@test_decorator
def test_technical_documentation():
    """Prueba del agente de documentación técnica."""
    print("\n--- Prueba de Documentación Técnica ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Generar documentación técnica para una API de procesamiento de lenguaje natural",
        "Crear guía de implementación para sistema de IA generativa"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'technical_documentation'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Precisión de Documentación: {result.metrics['accuracy']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['accuracy'] > 0.9, "La precisión de la documentación debe ser muy alta"
    
    generate_md_report("Technical_Documentation", test_queries, results)

@test_decorator
def test_code_review():
    """Prueba del agente de revisión de código."""
    print("\n--- Prueba de Revisión de Código ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Revisar código de implementación de modelo de machine learning",
        "Identificar mejoras de seguridad en un sistema de autenticación"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'code_quality'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print(f"Calidad de Código: {result.metrics['code_quality']}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
        assert result.metrics['code_quality'] > 0.8, "La calidad del código debe ser alta"
    
    generate_md_report("Code_Review", test_queries, results)

@test_decorator
def test_gmail_integration():
    """Prueba de la integración con Gmail."""
    print("\n--- Prueba de Integración con Gmail ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Enviar un correo electrónico al equipo sobre la nueva estrategia de IA",
        "Buscar correos relacionados con el proyecto de machine learning"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'email_management'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
    
    generate_md_report("Gmail_Integration", test_queries, results)
    
    # Verificar que se llamó a las funciones de Gmail
    assert mock_gmail_tool.run.called, "No se llamó a la herramienta de Gmail"

@test_decorator
def test_clickup_integration():
    """Prueba de la integración con ClickUp."""
    print("\n--- Prueba de Integración con ClickUp ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Crear una tarea en ClickUp para el desarrollo del nuevo algoritmo de IA",
        "Actualizar el estado de la tarea de implementación de machine learning"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'task_management'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
    
    generate_md_report("ClickUp_Integration", test_queries, results)
    
    # Verificar que se llamó a las funciones de ClickUp
    assert mock_clickup_tool.run.called, "No se llamó a la herramienta de ClickUp"

@test_decorator
def test_google_drive_integration():
    """Prueba de la integración con Google Drive."""
    print("\n--- Prueba de Integración con Google Drive ---")
    team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
    
    test_queries = [
        "Crear un documento en Google Drive para el informe de IA generativa",
        "Buscar archivos relacionados con el proyecto de machine learning en Google Drive"
    ]
    
    results = []
    for query in test_queries:
        state = TeamAssistantState()
        state.query = query
        state.category = 'file_management'
        
        result = team_assistant.route_query(state)
        results.append(result)
        print(f"Consulta: {query}")
        print(f"Respuesta: {result.response}")
        print("-" * 50)
        
        assert result.response, "La respuesta no debe estar vacía"
    
    generate_md_report("Google_Drive_Integration", test_queries, results)
    
    # Verificar que se llamó a las funciones de Google Drive
    assert mock_google_drive_tool.run.called, "No se llamó a la herramienta de Google Drive"

@test_decorator
def test_invalid_credentials():
    """Prueba del manejo de credenciales inválidas."""
    print("\n--- Prueba de Credenciales Inválidas ---")
    
    # Guardar las credenciales originales
    original_gmail_creds = os.environ.get('GMAIL_CREDENTIALS')
    
    try:
        # Establecer credenciales inválidas
        os.environ['GMAIL_CREDENTIALS'] = 'invalid_credentials.json'
        
        with pytest.raises(ValueError):
            SpecializedTeamAssistant(config={'temperature': 0.5})
        
        logger.info("Prueba de credenciales inválidas pasada exitosamente")
    finally:
        # Restaurar las credenciales originales
        os.environ['GMAIL_CREDENTIALS'] = original_gmail_creds

def main():
    """Ejecutar todas las pruebas de los agentes especializados."""
    print("🚀 Pruebas del Sistema de Equipos Especializados de IA 🚀")
    
    test_ceo_coordinator()
    test_project_manager()
    test_research_development()
    test_marketing_content()
    test_technical_documentation()
    test_code_review()
    test_gmail_integration()
    test_clickup_integration()
    test_google_drive_integration()
    test_invalid_credentials()

if __name__ == "__main__":
    main()
