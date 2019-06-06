from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class calendar:
    def __init__(self, googleCalendarConfig):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)
        self.pn_w = int(googleCalendarConfig["pn_w"])
        self.pn_d = int(googleCalendarConfig["pn_d"])
        self.pn_h = int(googleCalendarConfig["pn_h"])
        self.pn_m = int(googleCalendarConfig["pn_m"])

    def makeEvent(self, assignment):
        # Call the Calendar API
        assignmentDate = assignment["Date"].split("/")
        event = {
            "summary": assignment["Subject"] + " - " + assignment["Title"],
            "description": assignment["Description"],
            "start": {
                "dateTime":assignmentDate[2] + "-" + assignmentDate[1] + "-" + assignmentDate[0] + "T11:00:00",
                "timeZone":"Europe/Berlin"
            },
            "end": {
                "dateTime":assignmentDate[2] + "-" + assignmentDate[1] + "-" + assignmentDate[0] + "T12:00:00",
                "timeZone":"Europe/Berlin"
            },
            "reminders":{
                "useDefault":False,
                "overrides": [
                    {"method": "popup", "minutes": self.pn_w * 7 * 24 * 60 + self.pn_d * 24 * 60 + self.pn_h * 60 + self.pn_m}
                ]
            }
        }
        self.service.events().insert(calendarId="primary", body=event).execute()
