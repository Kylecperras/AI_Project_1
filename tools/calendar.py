from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

class GoogleCalendarTool:
    def __init__(self, credentials_file):
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/calendar"])
        self.service = build("calendar", "v3", credentials=creds)

    def list_events(self, days_ahead=7):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = self.service.events().list(
            calendarId="primary", timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return [f"{e['start'].get('dateTime', e['start'].get('date'))} - {e['summary']}" for e in events]

    def create_event(self, summary, start_time, end_time):
        event = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
        }
        created_event = self.service.events().insert(calendarId="primary", body=event).execute()
        return f"Event created: {created_event.get('htmlLink')}"

