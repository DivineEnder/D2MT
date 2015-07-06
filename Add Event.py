#!/usr/bin/env python

# modified from:
# https://developers.google.com/api-client-library/python/samples/authorized_api_cmd_line_calendar.py

#Imports two standard libraries needed for the script
import time
import os

#Clears the command line screen when called
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

#Takes a package name and installs that package
def install(package):
    import pip
    pip.main(["install", package])  

#Installs the needed modules for the script to run
print("<<<INSTALLING MODULES>>>")
install("httplib2")
install("google-api-python-client")
install("BeautifulSoup4")
install("requests")

#Imports all the special modules that were installed above
import httplib2
import sys
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
from datetime import datetime

from bs4 import BeautifulSoup
import requests

#Own number to string function that places a zero in front of a single digit number
def toString(n):
    if (n < 10):
        return "0" + str(n)
    else:
        return str(n)

def main():

    #Does some google drive credtialing magic that allows the program add and read events
    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('client_secret.json', scope=scope)

    storage = Storage('credentials.dat')
    credentials = storage.get()

    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)
    
    #Would print upcoming events
    """print("Upcoming Events:")
    request = service.events().list(calendarId='primary')
    while request != None:
        response = request.execute()
        for event in response.get('items', []):
            print(event.get('summary', 'NO SUMMARY'))
        request = service.events().list_next(request, response)"""

    #Gets a list of the calendars current events to make sure not to duplicate events
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(calendarId = "primary", timeMin = now, singleEvents = True, orderBy = "startTime").execute()
    events = eventsResult.get("items", [])
    calendarStartTimes = []
    calendarEventSummaries = []
    calendarEventDescriptions = []
    calendarEventIDs = []
    for event in events:
        cStartTime = event["start"].get("dateTime")
        calendarStartTimes.append(cStartTime[0:len(cStartTime) - 6])
        calendarEventSummaries.append(event["summary"])
        calendarEventDescriptions.append(event["description"])
        calendarEventIDs.append(event["id"])

    #Clears the command line screen of all the importing stuff
    cls()

    print("Matches taken from GosuGamers website")
    #Gets the websites html to parse
    r = requests.get("http://www.gosugamers.net/dota2/gosubet")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    #Finds the table that lists the matches
    table = soup.find(text = "Dota 2 Upcoming Matches").parent.parent
    table = table.find("table", class_ = "simple matches")
    #Finds the elements within the table
    elements = table.findAll("tr")

    for element in elements:
        addEvent = True

        #Prints an extra empty line for clarity
        print()
        
        #Gets the html for the page dedicated to the match
        site = "http://www.gosugamers.net" + element.a["href"]
        r = requests.get(site)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        
        #Gets the team names from an element in the table
        teams = soup.find("div", class_ = "match-opponents")
        teams = teams.findAll("h3")
        team1 = teams[0].text
        team2 = teams[1].text
        summary = team1 + " Vs. " + team2
        print(summary)
        
        #Gets the date and time of the match
        date = soup.find("p", class_ = "datetime is-upcomming").text.replace(" ", "").replace("\n", "").split(",")
        del(date[1])
        date.append(date[1][0:5])
        date[1] = date[0][len(date[0]) - 2:len(date[0])]
        date[0] = date[0][0:len(date[0]) - 2]

        #Converts the date & time to the format needed for a google calendar event
        dateTime = "2015-"
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dateTime = dateTime + toString(months.index(date[0]) + 1) + "-"
        temp = date[2].split(":")
        time = int(temp[0]) - 9
        if (time < 0):
            time = time + 24
            date[1] = toString(int(date[1]) - 1)
        date[2] = toString(time) + ":" + temp[1]
        dateTime = dateTime + date[1] + "T" + date[2] + ":00"
        print(dateTime)

        #Creates an end time for convience
        endDateTime = "2015-"
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        endTime = date[2].split(":")
        endTime[0] = int(endTime[0]) + 1
        if (endTime[0] >= 24):
            endTime[0] = endTime[0] - 24
            date[1] = toString(int(date[1]) + 1)
        endDateTime = endDateTime + toString(months.index(date[0]) + 1) + "-" + date[1] + "T" + toString(endTime[0]) + ":" + endTime[1] + ":00"
        print(endDateTime)
        
        #Gets the league that the match is being played in to use as a description for the event
        heading = soup.find("div", class_ = "match-heading-overlay")
        league = heading.a.text
        print(league)

        for i in range(0, len(calendarStartTimes)):
            if (summary == calendarEventSummaries[i]):

                if (league == calendarEventDescriptions[i] and dateTime != calendarStartTimes[i]):
                    service.events().delete(calendarId = "primary", eventId = calendarEventIDs[i]).execute()
                    print("||||MATCH TIME HAS BEEN CHANGED||||")
                    print("Deleting previous event...")
                elif (dateTime == calendarStartTimes[i]):
                    addEvent = False

        #Adds the match to the calendar as an event if not already in there
        if (addEvent):
            event = {
            'summary': summary,
            'description': league,
            'start': {
                'dateTime': dateTime,
                'timeZone': 'America/Los_Angeles',
                },
            'end': {
                'dateTime': endDateTime,
                'timeZone': 'America/Los_Angeles',
                }
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

    print()
    print("---------------Done-------------------")
    
    #Keeps the command line open after the script has completed
    input()
        
if __name__ == '__main__':
    main()

