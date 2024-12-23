import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

class GoogleCalendarIntegration:
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]

    def __init__(self, gauth_path='.gauth.json', token_path='token.json'):
        self.gauth_path = gauth_path
        self.token_path = token_path
        self.credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def _get_credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
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

    def list_calendars(self):
        """Listar todos los calendarios disponibles"""
        calendars_result = self.service.calendarList().list().execute()
        return calendars_result.get('items', [])

    def get_upcoming_events(self, days=30, calendar_id='primary'):
        """Obtener eventos próximos en un calendario"""
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(days=days)
        
        events_result = self.service.events().list(
            calendarId=calendar_id, 
            timeMin=now.isoformat(),
            timeMax=end_time.isoformat(),
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

    def create_event(self, summary, start_time, end_time, description=None, attendees=None, calendar_id='primary'):
        """Crear un nuevo evento en el calendario"""
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }
        
        if description:
            event['description'] = description
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
        
        event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return event

def main():
    # Ejemplo de uso
    calendar_integration = GoogleCalendarIntegration()
    
    # Listar calendarios
    print("Calendarios disponibles:")
    for calendar in calendar_integration.list_calendars():
        print(f"- {calendar['summary']} (ID: {calendar['id']})")
    
    # Obtener eventos próximos
    print("\nEventos próximos:")
    events = calendar_integration.get_upcoming_events()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} - {event.get('summary', 'Sin título')}")
    
    # Ejemplo de creación de evento
    try:
        new_event = calendar_integration.create_event(
            summary="Reunión de Equipo",
            start_time=datetime.now(timezone.utc) + timedelta(days=7),
            end_time=datetime.now(timezone.utc) + timedelta(days=7, hours=1),
            description="Reunión semanal de seguimiento de proyectos",
            attendees=["equipo@empresa.com"]
        )
        print("\nEvento creado:")
        print(f"ID: {new_event['id']}")
        print(f"Enlace: {new_event.get('htmlLink', 'No disponible')}")
    except Exception as e:
        print(f"Error al crear evento: {e}")

if __name__ == '__main__':
    main()
