#!/usr/bin/env python3
"""
Specialized Team AI Assistant - Sistema de Equipos Profesionales de IA

Este módulo implementa un sistema de asistencia profesional basado en agentes 
especializados con capacidades de IA generativa.
"""

import logging
import os
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults

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
        self.logger = logging.getLogger(f"{self.__class__.__name__}Logger")
        self.logger.setLevel(logging.INFO)

    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        """Método base para procesamiento de consultas."""
        raise NotImplementedError("Cada agente debe implementar su método de procesamiento")

class CEOCoordinator(BaseSpecializedAgent):
    """Agente coordinador para decisiones estratégicas de alto nivel."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        strategic_prompt = ChatPromptTemplate.from_template(
            "Analiza estratégicamente la siguiente consulta desde una perspectiva de liderazgo ejecutivo: {query}"
        )
        chain = strategic_prompt | self.llm
        strategic_response = chain.invoke({"query": state.query})
        
        state.response = f"Análisis Estratégico: {strategic_response.content}"
        state.metrics['confidentiality_level'] = 0.9
        state.confidential_mode = True
        return state

class ProjectManager(BaseSpecializedAgent):
    """Agente para gestión y seguimiento de proyectos."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        project_prompt = ChatPromptTemplate.from_template(
            "Evalúa y planifica el siguiente proyecto o consulta: {query}"
        )
        chain = project_prompt | self.llm
        project_response = chain.invoke({"query": state.query})
        
        state.response = f"Plan de Proyecto: {project_response.content}"
        state.metrics['accuracy'] = 0.85
        return state

class ResearchDevelopment(BaseSpecializedAgent):
    """Agente para investigación, análisis y desarrollo de soluciones innovadoras."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        research_prompt = ChatPromptTemplate.from_template(
            "Investiga y desarrolla soluciones innovadoras para: {query}"
        )
        chain = research_prompt | self.llm
        research_response = chain.invoke({"query": state.query})
        
        state.response = f"Hallazgos de I+D: {research_response.content}"
        state.metrics['accuracy'] = 0.95
        return state

class MarketingContent(BaseSpecializedAgent):
    """Agente para creación de contenido estratégico y marketing."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        marketing_prompt = ChatPromptTemplate.from_template(
            "Desarrolla una estrategia de contenido para: {query}"
        )
        chain = marketing_prompt | self.llm
        marketing_response = chain.invoke({"query": state.query})
        
        state.response = f"Estrategia de Marketing: {marketing_response.content}"
        state.metrics['user_satisfaction'] = 0.85
        return state

class TechnicalDocumentation(BaseSpecializedAgent):
    """Agente para documentación técnica precisa y estructurada."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        doc_prompt = ChatPromptTemplate.from_template(
            "Genera documentación técnica detallada para: {query}"
        )
        chain = doc_prompt | self.llm
        doc_response = chain.invoke({"query": state.query})
        
        state.response = f"Documentación Técnica:\n{doc_response.content}"
        state.metrics['accuracy'] = 0.98
        return state

class CodeReview(BaseSpecializedAgent):
    """Agente para revisión de código, mejora de calidad y seguridad."""
    def process_query(self, state: TeamAssistantState) -> TeamAssistantState:
        code_review_prompt = ChatPromptTemplate.from_template(
            "Realiza una revisión de código crítica para: {query}. "
            "Identifica mejoras de seguridad, rendimiento y legibilidad."
        )
        chain = code_review_prompt | self.llm
        review_response = chain.invoke({"query": state.query})
        
        state.response = f"Revisión de Código:\n{review_response.content}"
        state.metrics['code_quality'] = 0.95
        state.confidential_mode = True
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
            'code_review': CodeReview(self.llm, "Code Review")
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
            'code_quality': self.agents['code_review']
        }
        
        agent = routing_strategies.get(state.category, self.agents['ceo_coordinator'])
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
