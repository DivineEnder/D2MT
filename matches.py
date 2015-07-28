#Imports some libraries for html parsing
import requests
from bs4 import BeautifulSoup

#Imports a datetime libary to get the current date time
from datetime import datetime

#Imports a custom function used for converting numbers to two char strings
from custom import toString

#Removes duplicate matches from the user's google calendar
def clear_duplicate_events(service, progressBar, status, matches):
    
    #Gets all the upcoming dota events on the user's calendar
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(calendarId = "primary", timeMin = now, singleEvents = True, orderBy = "startTime").execute()
    events = eventsResult.get("items", [])

    #Updates status label to deleting duplicates
    status["text"] = "Deleting duplicate matches"
    #Sets the progress bar max to the length of the matches to check
    progressBar["maximum"] = len(matches)

    #Checks for duplicate matches in calendar
    for match in matches:
        for event in events:
            
            #Gets the league that the match is being played in
            eventLeague = event["summary"].split("(")[1]
            eventLeague = eventLeague[0:len(eventLeague) - 1]
            
            #Gets the teams of the calendar match
            eventTeams = event["summary"].split("(")[0]
            eventTeams = eventTeams[0:len(eventTeams) - 1]

            #Gets the event time of the calendar match (in format of website matches)
            eventTime = event["start"]["dateTime"]
            eventTime = eventTime[0:len(eventTime) - 6]
            
            #Checks for duplicate matches (same league and teams)
            if (event["summary"] == match[0] + " (" + match[1] + ")"):
                service.events().delete(calendarId = "primary", eventId = event["id"]).execute()

            #Checks for duplicate matches (same league and same time)
            elif (eventLeague == match[1] and eventTime == match[2]):
                service.events().delete(calendarId = "primary", eventId = event["id"]).execute()

        #Gets all the upcoming dota events on the user's calendar
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        eventsResult = service.events().list(calendarId = "primary", timeMin = now, singleEvents = True, orderBy = "startTime").execute()
        events = eventsResult.get("items", [])
        
        #Moves the progress bar graphic
        progressBar.step()

#Adds the list of matches to the user's google calendar
def add_events(service, matches, progressBar, status):

    #Sets the maximum of the progress bar to the number of matches to be added
    progressBar["maximum"] = len(matches)

    #Iterates through matches and adds them
    for match in matches:

        #Sets the status label to tell the user what is being added
        status["text"] = "Adding match " + str(matches.index(match) + 1) + " of " + str(len(matches))
        
        #Adds the match to the calendar as an event
        event = {
        'summary': match[0] + " (" + match[1] + ")",
        'description': "Dota",
        'start': {
            'dateTime': match[2],
            'timeZone': 'America/Los_Angeles',
            },
        'end': {
            'dateTime': match[3],
            'timeZone': 'America/Los_Angeles',
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()

        #Updates the progress bar graphics
        progressBar.step()

    #Updates the label to tell the user that it has finished
    status["text"] = "Finished adding " + str(len(matches)) + " match(es) to your google calendar"

#Reads and adds all upcoming dota matches from GosuGamers website
def get_GosuGamer_matches():
    
    #Gets the websites html to parse
    r = requests.get("http://www.gosugamers.net/dota2/gosubet")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    #Finds the table that lists the matches
    table = soup.find(text = "Dota 2 Upcoming Matches").parent.parent
    table = table.find("table", class_ = "simple matches")
    #Finds the elements within the table
    elements = table.findAll("tr")

    #Creates a list of matches to return
    matches = []

    #Iterates through the table elements for matches
    for element in elements:

        #Creates a match list [teams][league][dateTime][endDateTime]
        match = []
        
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

        #Adds the teams to the match
        match.append(summary)
        
        #Gets the league that the match is being played in to add at end of summary
        heading = soup.find("div", class_ = "match-heading-overlay")
        league = heading.a.text

        #Adds the league to the match
        match.append(league)
        
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

        #Adds the formated dateTime to the match
        match.append(dateTime)
        
        #Creates an end time for convience
        endDateTime = "2015-"
        months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        endTime = date[2].split(":")
        endTime[0] = int(endTime[0]) + 1
        if (endTime[0] >= 24):
            endTime[0] = endTime[0] - 24
            date[1] = toString(int(date[1]) + 1)
        endDateTime = endDateTime + toString(months.index(date[0]) + 1) + "-" + date[1] + "T" + toString(endTime[0]) + ":" + endTime[1] + ":00"

        #Adds the formated endDateTime to the match
        match.append(endDateTime)

        #Adds the match to the list of matches
        matches.append(match)

    #Returns a list of all the matches on the GosuGamer website
    return matches
