#!/usr/bin/env python3
"""
Script de pruebas para el Sistema de Equipos Especializados de IA
"""

import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Añadir el directorio padre al path para importar el módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from specialized_team_ai_assistant import SpecializedTeamAssistant, TeamAssistantState

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
    
    print(f"Informe generado: {filename}")

# Cargar variable de entorno para la API de Groq
load_dotenv()

# Configurar la clave de API de Groq
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY', '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')

# Inicializar el modelo Groq (usando LLaMA3 70b)
llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0.5,
    verbose=True
)


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
    
    generate_md_report("CEO_Coordinator", test_queries, results)

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
    
    generate_md_report("Project_Manager", test_queries, results)

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
    
    generate_md_report("Research_Development", test_queries, results)

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
    
    generate_md_report("Marketing_Content", test_queries, results)

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
    
    generate_md_report("Technical_Documentation", test_queries, results)

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
    
    generate_md_report("Code_Review", test_queries, results)

def main():
    """Ejecutar todas las pruebas de los agentes especializados."""
    print("🚀 Pruebas del Sistema de Equipos Especializados de IA 🚀")
    
    test_ceo_coordinator()
    test_project_manager()
    test_research_development()
    test_marketing_content()
    test_technical_documentation()
    test_code_review()

if __name__ == "__main__":
    main()
