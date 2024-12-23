import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta

# Cargar credenciales desde .gauth.json
with open('.gauth.json', 'r') as f:
    gauth_data = json.load(f)

# Cargar credenciales desde .accounts.json
with open('.accounts.json', 'r') as f:
    accounts_data = json.load(f)

# Configurar credenciales
creds = Credentials(
    token=None,  # Necesitarás obtener un token de acceso
    token_uri=gauth_data['installed']['token_uri'],
    client_id=gauth_data['installed']['client_id'],
    client_secret=gauth_data['installed']['client_secret'],
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)

# Crear servicio de Calendar
service = build('calendar', 'v3', credentials=creds)

# Obtener eventos del próximo mes
now = datetime.utcnow()
end_time = now + timedelta(days=30)

try:
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=now.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
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
            print(f"{start} - {event['summary']}")

except Exception as e:
    print(f"An error occurred: {e}")
