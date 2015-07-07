#Imports the library for creating dirctories in the system
import os

#Imports library for web authorization help
import httplib2

#Imports some authorization libaries
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "Dota 2 Match Ticker"

#Gets the credentials for access to calendar then resturns an http built from them
def get_service():
    
    #Gets the home directory
    home_dir = os.path.expanduser("~")
    #Creates a variable with the credtials path
    credential_dir = os.path.join(home_dir, ".credentials")
    #Creates a directory at the credential directory if it does not exist
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "D2MT.json")

    #Creates a .json file at the credtial path to store credentials in
    store = oauth2client.file.Storage(credential_path)
    #Tries to read the credentials from the .json file
    credentials = store.get()

    #If credentials are not there or are invalid gets new credentials
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print("Storing credentials to " + credential_path)
        
    #Creates an http element from the credentials to help create the service
    http = credentials.authorize(httplib2.Http())
    #Creates a service which is used to get and add events
    service = discovery.build("calendar", "v3", http=http)

    return service
