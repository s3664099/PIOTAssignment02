# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#Function to connect to the user's calendar so that the event
#may be stored
def connect_calendar():

    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("../Database/token.json")
    creds = store.get()

    if(not creds or creds.invalid):
        flow = client.flow_from_clientsecrets("../Database/credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)

    return build("calendar", "v3", http=creds.authorize(Http()))
    
#Function to get calendar events. Used for debugging and testing purposes
def get_events(service, noEvents):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user"s calendar.
    """

    # Call the Calendar API.
    now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time.
    later = datetime.utcnow() + timedelta(days = 3)
    later = later.isoformat() +"Z"

    print("Getting the upcoming {} events.", noEvents)
    events_result = service.events().list(calendarId = "primary", timeMin = now, timeMax = later,
        maxResults = noEvents, singleEvents = True, orderBy = "startTime").execute()
    return events_result.get("items", [])

#Function to print events. Used for debugging and testing purposes
def print_events(events):

    results = ""

    if(not events):
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime")
        results += str(start)+" "+str(end)+" "+event["summary"]
    return results

def insert(pickUp, dropOff, rego, make, model, cost, service):

    event = {
        "summary": "Vehicle Booking "+rego,
        "description": "make: "+make+" model: "+model+" cost: $"+cost,
        "start": {
            "dateTime": pickUp,
            "timeZone": "Australia/Melbourne",
        },
        "end": {
            "dateTime": dropOff,
            "timeZone": "Australia/Melbourne",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "email", "minutes": 5 },
                { "method": "popup", "minutes": 10 },
            ],
        }
    }

    event = service.events().insert(calendarId = "primary", body = event).execute()
    #print("Event created: {}".format(event.get("htmlLink")))
    
    return event["id"]
    
def remove_event(id, service):
    service.events().delete(calendarId='primary', eventId=id).execute()

if __name__ == "__main__":
    date = datetime.now()
    tomorrow = (date + timedelta(days = 1)).strftime("%Y-%m-%d")
    time_start = "{}T06:00:00+10:00".format(tomorrow)
    time_end = "{}T07:00:00+10:00".format(tomorrow)
    service = connect_calendar()
    print_events(get_events(service, 10))
    insert(time_start, time_end, "XYZ987","Holden","Commodore", service)
    print_events(get_events(service, 1))
    print(len(get_events(service, 10)))
