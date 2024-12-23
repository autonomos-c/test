#!/usr/bin/env python3
"""
Ejemplo de uso del Sistema de Equipos Especializados de IA con integraciones
"""

import logging
import os
from specialized_team_ai_assistant import SpecializedTeamAssistant, TeamAssistantState

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_credentials():
    """Verifica si las credenciales necesarias están configuradas."""
    required_credentials = ['GROQ_API_KEY', 'GMAIL_CREDENTIALS', 'CLICKUP_API_KEY', 'GOOGLE_DRIVE_CREDENTIALS']
    missing_credentials = [cred for cred in required_credentials if not os.getenv(cred)]
    
    if missing_credentials:
        logger.warning(f"Faltan las siguientes credenciales: {', '.join(missing_credentials)}")
        print("\nPara configurar las credenciales faltantes:")
        print("1. Cree un archivo .env en el directorio raíz del proyecto si no existe.")
        print("2. Añada las siguientes líneas al archivo .env, reemplazando los valores con sus credenciales reales:")
        for cred in missing_credentials:
            print(f"   {cred}=your_{cred.lower()}_here")
        print("\nConsulte el README.md para obtener instrucciones detalladas sobre cómo obtener estas credenciales.")
        return False
    return True

def main():
    print("🚀 Ejemplo de uso del Sistema de Equipos Especializados de IA 🚀")
    
    if not check_credentials():
        return
    
    try:
        # Inicializar el asistente
        team_assistant = SpecializedTeamAssistant(config={'temperature': 0.5})
        
        # Ejemplos de consultas para diferentes agentes
        queries = [
            ("Desarrollar estrategia de expansión para nuestra startup de IA", "strategic_planning"),
            ("Planificar el desarrollo de nuestra nueva aplicación de IA", "project_management"),
            ("Investigar las últimas tendencias en IA generativa", "research_inquiry"),
            ("Crear una campaña de marketing para nuestro nuevo producto de IA", "content_creation"),
            ("Generar documentación técnica para nuestra API de procesamiento de lenguaje natural", "technical_documentation"),
            ("Revisar el código de nuestro nuevo algoritmo de machine learning", "code_quality"),
            ("Enviar un correo al equipo sobre la nueva estrategia de IA", "email_management"),
            ("Crear una tarea en ClickUp para el desarrollo del nuevo algoritmo", "task_management"),
            ("Crear un documento en Google Drive para el informe de IA generativa", "file_management")
        ]
        
        for query, category in queries:
            print(f"\n--- Consulta: {query} ---")
            state = TeamAssistantState()
            state.query = query
            state.category = category
            
            try:
                result = team_assistant.route_query(state)
                print(f"Respuesta: {result.response}")
                print(f"Métricas: {result.metrics}")
                
                # Mostrar información adicional sobre las acciones realizadas
                if category == "email_management":
                    print("Acción: Se ha utilizado la integración con Gmail para gestionar correos electrónicos.")
                    print("Ejemplo: Se ha enviado un correo electrónico utilizando la herramienta GmailSendMessage.")
                elif category == "task_management":
                    print("Acción: Se ha utilizado la integración con ClickUp para gestionar tareas del proyecto.")
                    print("Ejemplo: Se ha creado una nueva tarea en ClickUp utilizando la herramienta ClickupCreateTask.")
                elif category == "file_management":
                    print("Acción: Se ha utilizado la integración con Google Drive para gestionar documentos.")
                    print("Ejemplo: Se ha creado un nuevo documento en Google Drive utilizando la herramienta GoogleDriveCreateFile.")
                
            except Exception as e:
                logger.error(f"Error al procesar la consulta '{query}': {str(e)}")
            
            print("-" * 50)

    except ValueError as ve:
        logger.error(f"Error de credenciales: {str(ve)}")
        print("Por favor, verifique sus credenciales en el archivo .env y asegúrese de que sean válidas.")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        print("Ha ocurrido un error inesperado. Por favor, revise los logs para más detalles.")

if __name__ == "__main__":
    main()
