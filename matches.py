#Imports some libraries for html parsing
import requests
from bs4 import BeautifulSoup

#Imports a datetime libary to get the current date time
from datetime import datetime

#Imports a custom function used for converting numbers to two char strings
from custom import toString

#Accounts for rescheduling of matches and team changes by deleting dota events
def clear_dota_events(service, progressBar, status):

    #Gets all the upcoming dota events on the user's calendar
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(calendarId = "primary", timeMin = now, singleEvents = True, orderBy = "startTime").execute()
    events = eventsResult.get("items", [])

    #Sets the progress bar max to the length of the events to be deleted
    progressBar["maximum"] = len(events)

    #Deletes upcoming dota events in calendar
    for event in events:
        if (event["description"][0:4] == "Dota"):
            #Updates status label with count of events deleted
            status["text"] = "Deleting match " + str(events.index(event) + 1) + " of " + str(len(events))
            service.events().delete(calendarId = "primary", eventId = event["id"]).execute()
            #Moves the progress bar graphic
            progressBar.step()

#Reads and adds all upcoming dota matches from GosuGamers website
def get_GosuGamer_matches(service, progressBar, status):
    
    #Gets the websites html to parse
    r = requests.get("http://www.gosugamers.net/dota2/gosubet")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    #Finds the table that lists the matches
    table = soup.find(text = "Dota 2 Upcoming Matches").parent.parent
    table = table.find("table", class_ = "simple matches")
    #Finds the elements within the table
    elements = table.findAll("tr")

    #Sets the progress bar max to increment in steps of four as D2MT processes matches
    progressBar["maximum"] = len(elements) * 4

    for element in elements:

        #Updates status label with count of events added
        status["text"] = "Adding match " + str(elements.index(element) + 1) + " of " + str(len(elements))
        
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

        #Gets the league that the match is being played in to add at end of summary
        heading = soup.find("div", class_ = "match-heading-overlay")
        league = heading.a.text
        summary = summary + "(" + league + ")"
        
        #Updates quater step of progress bar for smoother progress
        progressBar.step()
        
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
        
        #Updates quater step of progress bar for smoother progress
        progressBar.step()
        
        #Creates an end time for convience
        endDateTime = "2015-"
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        endTime = date[2].split(":")
        endTime[0] = int(endTime[0]) + 1
        if (endTime[0] >= 24):
            endTime[0] = endTime[0] - 24
            date[1] = toString(int(date[1]) + 1)
        endDateTime = endDateTime + toString(months.index(date[0]) + 1) + "-" + date[1] + "T" + toString(endTime[0]) + ":" + endTime[1] + ":00"

        #Updates quater step of progress bar for smoother progress
        progressBar.step()

        #Adds the match to the calendar as an event
        event = {
        'summary': summary,
        'description': "Dota",
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
        
        #Updates quater step of progress bar for smoother progress
        progressBar.step()
        
    #Updates the status label to tell the user that everything is done
    status["text"] = "Finished adding " + str(len(elements)) + " events"
