#Used to log errors to a text file
import sys
sys.stderr = open("errlog.txt", "w")
#Program does not run without this

#Installs required modules
import os
os.system("install_dependencies.py")

#Imports several custom functions in different files
from authorization import get_service
from matches import clear_duplicate_events
from matches import get_GosuGamer_matches
from matches import add_events
from customwidget import FitListbox

#Imports some GUI libraries
import tkinter as tk
from tkinter import ttk
#Imports a threading library
import threading

#Creates an application class which can be called to run D2MT
class Application:

    #Creates an init function which generates all the widgets
    def __init__(self, master):

        #Creates a frame inside of the window
        frame = tk.Frame(master)
        frame.grid()

        #Gets a sevice that adds and gets events from google calendar
        self.service = get_service()

        #Creates a combobox of the different websites to get matches from
        self.selectedWebsite = tk.StringVar()
        self.websites = ttk.Combobox(frame, textvariable = self.selectedWebsite, values = ("GosuGamers"), state = "readonly")
        self.websites.current(0)
        self.websites.grid(column = 0, row = 1, padx = 5)

        #Creates a button to add the matches to your google calendar
        self.addMatches = tk.Button(frame, text = "Add Matches", fg = "yellow", bg = "black", command = self.create_thread)
        self.addMatches.grid(column = 0, row = 0, pady = 3, padx = 10)

        #Creates a quit button to quit the app
        self.quit = tk.Button(frame, text = "Quit", fg = "white", bg = "black", command = root.destroy)
        self.quit.grid(column = 2, row = 0, pady = 2, padx = 10)

        #Creates a progress bar for creating events
        self.progressBar = ttk.Progressbar(frame, orient = "horizontal", length = 200, mode = "determinate", maximum = 100)
        self.progressBar.grid(column = 1, row = 0, pady = 2, padx = 4)

        #Creates a status label to tell the user what the app is doing
        self.status = tk.Label(frame, text = "", fg = "black")
        self.status.grid(column = 1, row = 1, pady = 2, padx = 2)

        #Gets a list of matches from the GosuGamers website
        self.matches = get_GosuGamer_matches()

        #Creates a listbox full of preloaded matches
        self.listbox = FitListbox(frame, selectmode = tk.EXTENDED, height = len(self.matches))
        self.listbox.grid(column = 0, row = 2, padx = 4, pady = 4)
        for self.match in self.matches:
            self.listbox.insert(tk.END, self.match[0])
        self.listbox.autowidth()

    #Creates a thread to add events alongside the render loop
    def create_thread(self):
        threading.Thread(target = self.add_events).start()
        
    #Adds the matches to the user's google calendar
    def add_events(self):
        #Deletes the previously added dota 2 events
        #clear_dota_events(self.service, self.progressBar ,self.status)
        
        self.selectedMatches = []
        for i in range(0, len(self.matches)):
            if i in self.listbox.curselection():
                self.selectedMatches.append(self.matches[i])

        clear_duplicate_events(self.service, self.progressBar, self.status, self.selectedMatches)
        
        #Adds the upcoming matches taken off the GosuGamer website
        add_events(self.service, self.selectedMatches, self.progressBar, self.status)

#Creates a tkinter winodw loop
root = tk.Tk()

#Extra window sizing stuff (non-functional)
#windowWidth = 500
#windowHeight = 500
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()
#root.geometry(str(windowWidth) + "x" + str(windowWidth) + "+" + str(int(screen_width/2 - windowWidth/2)) + "+" + str(int(screen_height/2 - windowHeight/2)))

#Creates an instance of the D2MT app
app = Application(root)
#Starts the root tkinter loop
root.mainloop()
