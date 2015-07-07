#Imports a custom made clear screen function for cmd
from custom import cls

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

#Clears the command line screen
cls()

#Imports an http library for help getting and adding events
import httplib2

#imports various Google api libraries to help get and add events
from oauth2client import tools

#Imports several custom functions in different files
from authorization import get_service
from matches import clear_dota_events
from matches import get_GosuGamer_matches

#Imports some htmp parsers to get matches and times
from bs4 import BeautifulSoup
import requests

#Imports datetime module to get current time and deal with formats
import datetime;

def main():

    print("<<<GETTING SERVICE>>>")
    #Gets a sevice that adds and gets events from google calendar
    service = get_service()
    #Clears the command line screen
    cls()
    
    print("<<<DELETING PREVIOUS DOTA 2 EVENTS>>>")
    #Deletes the previously added dota 2 events
    clear_dota_events(service)
    #Clears the command line screen
    cls()

    print("<<<ADDING GOOGLE EVENTS>>>")
    #Adds the upcoming matches taken off the GosuGamer website
    get_GosuGamer_matches(service)

    #Ticky way to keep the cmd window open after the program ends
    input()


if __name__ == "__main__":
    main()
