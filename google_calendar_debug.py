import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

# Scopes para acceder a Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_credentials():
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas, solicitar al usuario que inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Cargar credenciales desde .gauth.json
            with open('.gauth.json', 'r') as f:
                gauth_data = json.load(f)
            
            # Iniciar flujo de autorización
            flow = InstalledAppFlow.from_client_config(
                gauth_data, 
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Guardar las credenciales para la próxima ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def list_calendars_and_events():
    # Obtener credenciales
    creds = get_google_calendar_credentials()
    
    # Crear servicio de Calendar
    service = build('calendar', 'v3', credentials=creds)
    
    try:
        # Listar todos los calendarios
        print("Calendarios disponibles:")
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        for calendar in calendars:
            print(f"- {calendar['summary']} (ID: {calendar['id']})")
        
        print("\nEventos en el calendario principal:")
        # Obtener eventos del próximo mes
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(days=30)
        
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now.isoformat(),
            timeMax=end_time.isoformat(),
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
        else:
            print('Upcoming events:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"{start} - {event.get('summary', 'Sin título')}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    list_calendars_and_events()
