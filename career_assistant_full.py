#!/usr/bin/env python3
# GenAI Career Assistant Agent – Your Ultimate Guide to a Career in Generative AI!🚀

import os
import re
from typing import Dict, TypedDict
from datetime import datetime

from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages

from dotenv import load_dotenv

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

class State(TypedDict):
    query: str
    category: str
    response: str

def trim_conversation(prompt):
    """Trims conversation history to retain only the latest messages within the limit."""
    max_messages = 10  # Limit the conversation history to the latest 10 messages
    return trim_messages(
        prompt,
        max_tokens=max_messages,
        strategy="last",
        token_counter=len,
        start_on="human",
        include_system=True,
        allow_partial=False,
    )

def save_file(data, filename):
    """Saves data to a markdown file with a timestamped filename."""
    folder_name = "Agent_output"
    os.makedirs(folder_name, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{filename}_{timestamp}.md"
    
    file_path = os.path.join(folder_name, filename)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
        print(f"File '{file_path}' created successfully.")
    
    return file_path

class LearningResourceAgent:
    def __init__(self, prompt):
        self.model = ChatGroq(model="llama3-70b-8192")
        self.prompt = prompt
        self.tools = [DuckDuckGoSearchResults()]

    def TutorialAgent(self, user_input):
        agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        response = agent_executor.invoke({"input": user_input})
        
        path = save_file(str(response.get('output')).replace("```markdown", "").strip(), 'Tutorial')
        print(f"Tutorial guardado en {path}")
        return path

    def QueryBot(self, user_input):
        print("\nIniciando la sesión de preguntas y respuestas. Escribe 'exit' para terminar la sesión.\n")
        record_QA_session = []
        record_QA_session.append(f'Consulta del usuario: {user_input} \n')
        self.prompt.append(HumanMessage(content=user_input))

        while True:
            self.prompt = trim_conversation(self.prompt)
            
            response = self.model.invoke(self.prompt)
            record_QA_session.append(f'\nRespuesta del experto: {response.content} \n')
            
            self.prompt.append(AIMessage(content=response.content))
            
            print('*' * 50 + 'AGENTE' + '*' * 50)
            print("\nRESPUESTA DEL AGENTE EXPERTO:", response.content)
            
            print('*' * 50 + 'USUARIO' + '*' * 50)
            user_input = input("\nSU CONSULTA: ")
            record_QA_session.append(f'\nConsulta del usuario: {user_input} \n')
            self.prompt.append(HumanMessage(content=user_input))
            
            if user_input.lower() == "exit":
                print("Terminando la sesión de chat.")
                path = save_file(''.join(record_QA_session), 'Sesion_Preguntas_Dudas')
                print(f"Sesión de preguntas guardada en {path}")
                return path

class InterviewAgent:
    def __init__(self, prompt):
        self.model = ChatGroq(model="llama3-70b-8192")
        self.prompt = prompt
        self.tools = [DuckDuckGoSearchResults()]

    def Interview_questions(self, user_input):
        agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        response = agent_executor.invoke({"input": user_input})
        
        path = save_file(str(response.get('output')).replace("```markdown", "").strip(), 'Preguntas_Entrevista')
        print(f"Preguntas de entrevista guardadas en {path}")
        return path

    def Mock_Interview(self):
        print("\nIniciando simulación de entrevista. Escribe 'exit' para terminar.\n")
        record_interview = []
        
        while True:
            response = self.model.invoke(self.prompt)
            record_interview.append(f'\nPregunta del entrevistador: {response.content} \n')
            
            print('*' * 50 + 'ENTREVISTADOR' + '*' * 50)
            print("\nPREGUNTA:", response.content)
            
            print('*' * 50 + 'CANDIDATO' + '*' * 50)
            user_input = input("\nRESPUESTA: ")
            record_interview.append(f'\nRespuesta del candidato: {user_input} \n')
            
            if user_input.lower() == "exit":
                print("Terminando simulación de entrevista.")
                path = save_file(''.join(record_interview), 'Simulacion_Entrevista')
                print(f"Simulación de entrevista guardada en {path}")
                return path

class ResumeMaker:
    def __init__(self, prompt):
        self.model = ChatGroq(model="llama3-70b-8192")
        self.prompt = prompt
        self.tools = [DuckDuckGoSearchResults()]

    def Create_Resume(self, user_input):
        agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        response = agent_executor.invoke({"input": user_input})
        
        path = save_file(str(response.get('output')).replace("```markdown", "").strip(), 'CV')
        print(f"CV guardado en {path}")
        return path

class JobSearch:
    def __init__(self, prompt):
        self.model = ChatGroq(model="llama3-70b-8192")
        self.tools = DuckDuckGoSearchResults()
        self.prompt = prompt

    def clean_query(self, query):
        """Limpia la consulta de entrada eliminando caracteres especiales y normalizando."""
        # Eliminar caracteres especiales y convertir a minúsculas
        cleaned_query = re.sub(r'[^\w\s]', '', query.lower())
        return cleaned_query

    def find_jobs(self, user_input):
        try:
            # Limpiar la consulta de entrada
            cleaned_input = self.clean_query(user_input)
            
            # Intentar búsqueda con consulta limpia
            results = self.tools.invoke(cleaned_input)
            
            # Crear un prompt específico para búsqueda de trabajo
            job_search_prompt = ChatPromptTemplate.from_template(
                "Basado en los siguientes resultados de búsqueda, proporciona un resumen de oportunidades laborales para un experto en IA en la zona de Puerto Montt:\n\n"
                "Resultados: {result}"
            )
            
            chain = job_search_prompt | self.model
            jobs = chain.invoke({"result": results}).content
        
        except Exception as e:
            # Si la búsqueda falla, generar una respuesta predeterminada
            print(f"Error en búsqueda: {e}")
            jobs = f"""Oportunidades de Trabajo para Ingeniero de Sistemas en Puerto Montt

Debido a limitaciones técnicas, no se pudieron obtener resultados de búsqueda en línea. Sin embargo, aquí hay algunas recomendaciones generales:

1. Portales de Empleo Locales:
   - Trabajando.com
   - Portal de Empleos de la Universidad Austral
   - LinkedIn

2. Empresas Tecnológicas en la Región de Los Lagos:
   - Consultar con empresas de tecnología en Puerto Montt y Osorno
   - Parques industriales y tecnológicos de la zona

3. Estrategias de Búsqueda:
   - Contactar departamentos de recursos humanos locales
   - Networking con egresados de la Universidad Austral
   - Participar en eventos tecnológicos regionales

4. Sectores Potenciales:
   - Empresas de servicios tecnológicos
   - Sector pesquero y acuícola (requiere soluciones tecnológicas)
   - Administración pública regional
   - Startups locales

Recomendación: Personalizar CV destacando experiencia en IA y sistemas.
"""
        
        path = save_file(str(jobs).replace("```markdown", "").strip(), 'Busqueda_Trabajo')
        print(f"Trabajos guardados en {path}")
        return path

def categorize(state: State) -> State:
    """Categorizes the user query into one of four main categories."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following customer query into one of these categories:\n"
        "1: Learn Generative AI Technology\n"
        "2: Resume Making\n"
        "3: Interview Preparation\n"
        "4: Job Search\n"
        "Give the number only as an output.\n\n"
        "Examples:\n"
        "1. Query: 'What are the basics of generative AI, and how can I start learning it?' -> 1\n"
        "2. Query: 'Can you help me improve my resume for a tech position?' -> 2\n"
        "3. Query: 'What are some common questions asked in AI interviews?' -> 3\n"
        "4. Query: 'Are there any job openings for AI engineers?' -> 4\n\n"
        "Now, categorize the following customer query:\n"
        "Query: {query}"
    )

    chain = prompt | llm 
    print('Categorizing the customer query...')
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def route_query(state: State):
    """Route the query based on its category to the appropriate handler."""
    if '1' in state["category"]:
        print('Category: handle_learning_resource')
        return "handle_learning_resource"

    elif '2' in state["category"]:
        print('Category: handle_resume_making')
        return "handle_resume_making"

    elif '3' in state["category"]:
        print('Category: handle_interview_preparation')
        return "handle_interview_preparation"

    elif '4' in state["category"]:
        print('Category: job_search')
        return "job_search"

    else:
        print("Please ask your question based on my description.")
        return False

def handle_learning_resource(state: State) -> State:
    """Maneja consultas relacionadas con recursos de aprendizaje."""
    system_message = '''Eres un asistente experto en IA generativa con amplia experiencia en entrenamiento y orientación de otros en ingeniería de IA.'''
    prompt = [SystemMessage(content=system_message)]
    
    learning_agent = LearningResourceAgent(prompt)
    
    # Determinar si es tutorial o pregunta
    prompt_categorization = ChatPromptTemplate.from_template(
        "Categorize the following query:\n"
        "- Tutorial: For creating tutorials, blogs, or documentation\n"
        "- Question: For general queries about generative AI\n"
        "Query: {query}"
    )
    
    chain = prompt_categorization | llm
    sub_category = chain.invoke({"query": state["query"]}).content.lower()
    
    if 'tutorial' in sub_category:
        response_path = learning_agent.TutorialAgent(state["query"])
    else:
        response_path = learning_agent.QueryBot(state["query"])
    
    with open(response_path, 'r') as f:
        response_content = f.read()
    
    return {"response": response_content}

def handle_resume_making(state: State) -> State:
    """Maneja consultas relacionadas con la creación de currículum."""
    system_message = '''Eres un experto en creación de currículums para roles en tecnología e IA generativa.'''
    prompt = [SystemMessage(content=system_message)]
    
    resume_agent = ResumeMaker(prompt)
    response_path = resume_agent.Create_Resume(state["query"])
    
    with open(response_path, 'r') as f:
        response_content = f.read()
    
    return {"response": response_content}

def handle_interview_preparation(state: State) -> State:
    """Maneja consultas relacionadas con preparación de entrevistas."""
    system_message = '''Eres un experto en preparación de entrevistas para roles en tecnología e IA generativa.'''
    prompt = [SystemMessage(content=system_message)]
    
    interview_agent = InterviewAgent(prompt)
    
    # Determinar si es preguntas o simulación de entrevista
    prompt_categorization = ChatPromptTemplate.from_template(
        "Categorize the following query:\n"
        "- Mock: For mock interview simulation\n"
        "- Question: For interview preparation questions\n"
        "Query: {query}"
    )
    
    chain = prompt_categorization | llm
    sub_category = chain.invoke({"query": state["query"]}).content.lower()
    
    if 'mock' in sub_category:
        response_path = interview_agent.Mock_Interview()
    else:
        response_path = interview_agent.Interview_questions(state["query"])
    
    with open(response_path, 'r') as f:
        response_content = f.read()
    
    return {"response": response_content}

def job_search(state: State) -> State:
    """Maneja consultas relacionadas con búsqueda de trabajo."""
    system_message = '''Eres un experto en búsqueda de trabajo en tecnología e IA generativa.'''
    prompt = [SystemMessage(content=system_message)]
    
    job_search_agent = JobSearch(prompt)
    response_path = job_search_agent.find_jobs(state["query"])
    
    with open(response_path, 'r') as f:
        response_content = f.read()
    
    return {"response": response_content}

def run_user_query(query: str) -> Dict[str, str]:
    """Process a user query through the LangGraph workflow."""
    results = app.invoke({"query": query})
    return {
        "category": results["category"],
        "response": results["response"]
    }

def main():
    # Crear el grafo de flujo de trabajo
    workflow = StateGraph(State)

    # Añadir nodos para cada estado del flujo de trabajo
    workflow.add_node("categorize", categorize)
    workflow.add_node("handle_learning_resource", handle_learning_resource)
    workflow.add_node("handle_resume_making", handle_resume_making)
    workflow.add_node("handle_interview_preparation", handle_interview_preparation)
    workflow.add_node("job_search", job_search)

    # Definir bordes condicionales
    workflow.add_edge(START, "categorize")
    workflow.add_conditional_edges(
        "categorize",
        route_query,
        {
            "handle_learning_resource": "handle_learning_resource",
            "handle_resume_making": "handle_resume_making",
            "handle_interview_preparation": "handle_interview_preparation",
            "job_search": "job_search"
        }
    )

    # Definir bordes finales
    workflow.add_edge("handle_resume_making", END)
    workflow.add_edge("job_search", END)
    workflow.add_edge("handle_interview_preparation", END)
    workflow.add_edge("handle_learning_resource", END)

    # Compilar el grafo de flujo de trabajo
    global app
    app = workflow.compile()

    # Menú principal interactivo
    while True:
        print("\n--- Menú Principal ---")
        print("1. Hacer una consulta")
        print("2. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            query = input("Ingrese su consulta: ")
            result = run_user_query(query)
            print(f"Categoría: {result['category']}")
            print(f"Respuesta: {result['response']}")
        elif opcion == '2':
            print("Saliendo del asistente. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
