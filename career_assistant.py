#!/usr/bin/env python3
# GenAI Career Assistant Agent – Your Ultimate Guide to a Career in Generative AI!🚀

import os
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

def main():
    # Ejemplo de uso del agente
    system_message = '''Eres un asistente experto en IA generativa con amplia experiencia en entrenamiento y orientación de otros en ingeniería de IA.'''
    prompt = [SystemMessage(content=system_message)]
    
    learning_agent = LearningResourceAgent(prompt)
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Generar Tutorial")
        print("2. Sesión de Preguntas y Respuestas")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            tema = input("Ingrese el tema para el tutorial: ")
            learning_agent.TutorialAgent(tema)
        elif opcion == '2':
            consulta_inicial = input("Ingrese su consulta inicial: ")
            learning_agent.QueryBot(consulta_inicial)
        elif opcion == '3':
            print("Saliendo del asistente. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
