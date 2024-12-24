import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone

class GmailIntegration:
    SCOPES = [
        'https://mail.google.com/',  # Scope for full Gmail access
        'https://www.googleapis.com/auth/gmail.modify'
    ]

    def __init__(self, gauth_path='.gauth.json', token_path='gmail_token.json'):
        self.gauth_path = gauth_path
        self.token_path = token_path
        self.credentials = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def _get_credentials(self):
        """Obtener credenciales de Gmail"""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Verificar si existe el archivo de credenciales
                if not os.path.exists(self.gauth_path):
                    print("Archivo de credenciales no encontrado.")
                    print("Por favor, configure las credenciales de Google en .gauth.json")
                    print("Pasos:")
                    print("1. Vaya a https://console.cloud.google.com/")
                    print("2. Cree un nuevo proyecto o seleccione uno existente")
                    print("3. Habilite la API de Gmail")
                    print("4. Cree credenciales de OAuth 2.0 para una aplicación de escritorio")
                    print("5. Descargue el archivo de credenciales y guárdelo como .gauth.json")
                    raise FileNotFoundError(f"No se encontró el archivo de credenciales {self.gauth_path}")
                
                with open(self.gauth_path, 'r') as f:
                    gauth_data = json.load(f)
                
                flow = InstalledAppFlow.from_client_config(
                    gauth_data, 
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def list_labels(self):
        """Listar etiquetas en Gmail"""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            return results.get('labels', [])
        except Exception as e:
            print(f"Error al listar etiquetas: {e}")
            return []

    def search_emails(self, query='', max_results=10):
        """Buscar correos electrónicos"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_details = []
            
            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                try:
                    payload = txt['payload']
                    headers = payload['headers']
                    
                    # Extraer información del correo
                    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'Sin asunto')
                    sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Remitente desconocido')
                    date = next((header['value'] for header in headers if header['name'] == 'Date'), 'Fecha desconocida')
                    
                    email_details.append({
                        'id': msg['id'],
                        'subject': subject,
                        'from': sender,
                        'date': date
                    })
                except Exception as e:
                    print(f"Error procesando correo {msg['id']}: {e}")
            
            return email_details
        except Exception as e:
            print(f"Error al buscar correos: {e}")
            return []

    def create_draft(self, to, subject, message_body):
        """Crear un borrador de correo"""
        try:
            message = {
                'message': {
                    'raw': self._create_message(to, subject, message_body)
                }
            }
            
            draft = self.service.users().drafts().create(
                userId='me', 
                body=message
            ).execute()
            
            return draft
        except Exception as e:
            print(f"Error al crear borrador: {e}")
            return None

    def _create_message(self, to, subject, body):
        """Crear mensaje codificado en base64"""
        import base64
        from email.mime.text import MIMEText
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        return base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    def send_email(self, to, subject, message_body):
        """Enviar correo electrónico"""
        try:
            message = {
                'raw': self._create_message(to, subject, message_body)
            }
            
            sent_message = self.service.users().messages().send(
                userId='me', 
                body=message
            ).execute()
            
            return sent_message
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return None

def main():
    """Ejemplo de uso de la integración de Gmail"""
    try:
        gmail_integration = GmailIntegration()
        
        # Listar etiquetas
        print("Etiquetas de Gmail:")
        labels = gmail_integration.list_labels()
        for label in labels:
            print(f"- {label['name']}")
        
        # Buscar correos electrónicos
        print("\nBuscando correos recientes:")
        emails = gmail_integration.search_emails(query='', max_results=5)
        for email in emails:
            print(f"ID: {email['id']}")
            print(f"De: {email['from']}")
            print(f"Asunto: {email['subject']}")
            print(f"Fecha: {email['date']}\n")
        
        # Crear borrador
        draft = gmail_integration.create_draft(
            to="equipo@empresa.com", 
            subject="Prueba de Integración de Gmail", 
            message_body="Este es un borrador de correo creado por el Sistema de Equipos Especializados de IA."
        )
        if draft:
            print("\nBorrador creado:")
            print(f"ID del borrador: {draft['id']}")
    except Exception as e:
        print(f"Error general en la integración de Gmail: {e}")

if __name__ == '__main__':
    main()
