from apple_calendar_integration import ICloudCalendarAPI
from datetime import datetime, timedelta

class calendar:
    def __init__(self, appleCalendarConfig):
        self.usr = appleCalendarConfig["usr"]
        self.pwd = appleCalendarConfig["pwd"]
        self.pn_w = appleCalendarConfig["pn_w"]
        self.pn_d = appleCalendarConfig["pn_d"]
        self.pn_h = appleCalendarConfig["pn_h"]
        self.pn_m = appleCalendarConfig["pn_m"]
        self.api = ICloudCalendarAPI(self.usr, self.pwd)
    def makeEvent(self, assignment):
        assignment["Subject"]
        date = assignment["Date"].split("/")
        startDate = int(datetime(date[2], date[1], date[0], 11).timestamp())
        endDate = startDate + timedelta(hours=1)
        prenotif = {
            "before":False,
            "weeks": self.pn_w if self.pn_w != "-" else 0,
            "days": self.pn_d if self.pn_d != "-" else 0,
            "hours": self.pn_h if self.pn_h != "-" else 0,
            "minutes": self.pn_m if self.pn_m != "-" else 0
        }
        etag, ctag, guid = self.api.create_event(assignment["Subject"] + " - " + assignment["Title"], startDate, endDate, note=assignment, alarm=prenotif)
