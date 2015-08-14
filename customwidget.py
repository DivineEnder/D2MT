#Imports gui python tools
import tkinter as tk
import _thread

#Creates a custom widget formed from several listboxes which resembles a table
class Table(tk.Frame):

    def __init__(self, master, columnHeaders, columnData, betweenRowHeaders, searchable):
        #Initializes a frame that the table is going to be displayed in
        tk.Frame.__init__(self, master)

        #Gets the column data and labels for the columns
        self.columnHeaders = columnHeaders
        self.columnData = columnData

        #Creates a list of between row labels ([Team 1] vs [Team 2])
        self.betweenRowHeaders = betweenRowHeaders

        #Creates a list of the current data that is displayed
        self.curData = self.columnData

        #Displays the column headers above respective columns (buttons for sorting purposes)
        self.headers = []
        for i in range(0, len(self.columnHeaders)):
            #Displays the columns with row headers if provided with some
            self.column = i
            if (self.betweenRowHeaders != []):
                self.column = i * 2
            self.headers.append(tk.Button(self, text = self.columnHeaders[i] + " -"))
            #Using bind instead of built in command because bind sends event which a widget can be pulled from
            self.headers[i].bind("<Button-1>", self.sort)
            self.headers[i].grid(row = 0, column = self.column, padx = 3, pady = 1)

        #Creates listboxes as columns for the table
        self.listboxes = []

        #Creates a list of between column listboxes for the visual effect
        self.betweenListboxes = []
        for i in range(0, len(self.columnData)):
            #Displays the columns with row headers if provided with some
            self.column = i
            if (self.betweenRowHeaders != []):
                self.column = i * 2
            
            #Sets the width of the listboxes to the length of the max data/label
            self.width = 0
            if (len(self.headers[i]["text"]) > len(max(self.columnData[i], key = len))):
                self.width = len(self.headers[i]["text"]) + 3
            else:
                self.width = len(max(self.columnData[i], key = len)) + 1
                
            #Creates the listbox and adds it to the list
            self.listboxes.append(tk.Listbox(self, selectmode = tk.EXTENDED, activestyle = tk.NONE, exportselection = 0, height = 15, width = self.width))

            #Adds all the data sent to the widget to the listboxes
            for self.element in self.columnData[i]:
                self.listboxes[i].insert(tk.END, self.element)

            #Causes row select on click of element
            self.listboxes[i].bind("<<ListboxSelect>>", self.select_row)

            #Displays listboxes in column
            self.listboxes[i].grid(row = 1, column = self.column)

            #Displays the headers in between the columned listboxes
            if (self.betweenRowHeaders != [] and i != len(self.columnData) - 1):
                #Creates a listbox so that the formating aligns
                self.betweenListboxes.append(tk.Listbox(self, bd = 0, bg = "SYSTEMBUTTONFACE", relief = tk.FLAT, height = 15, width = len(self.betweenRowHeaders[i]) + 1))
                for j in range(0, len(self.curData[0])):
                    self.betweenListboxes[i].insert(tk.END, self.betweenRowHeaders[i])
                #Disables listbox functionality so that it functions as a correctly formatted label
                self.betweenListboxes[i].config(state = tk.DISABLED)

                #Displays the headers in column
                self.betweenListboxes[i].grid(row = 1, column = self.column + 1)

        #WORK IN PROGRESS
        #Creates a scroll bar for the table if there are more than 15 items
        if (len(columnData) > 15):
            self.scrollbar = tk.Scrollbar(self)
            self.scrollbar.grid(row = 1, column = len(self.columnData) * 2, sticky = "NS")
            self.scrollbar.config(command = self.scroll_all)

        self.searchable = searchable
        #Checks to see whether a search entry is included in the table widget
        if (searchable):
            #Creates variables to hold what is currently in the entry widget and what was last in the entry widget
            self.key = ""
            self.lastKey = self.key

            #Creates a frame to the right of the table to place the search box in
            searchFrame = tk.Frame(self)

            #Creates a label for the search box
            tk.Label(searchFrame, text = "Search for:").pack()

            #Cretaes the entry widget
            self.sortEntry = tk.Entry(searchFrame)
            self.sortEntry.pack()

            #Displays the frame to the right of the table spanning two rows
            searchFrame.grid(row = 0, rowspan = 2, column = len(self.listboxes) * 2)

        #Creates a new thread that constantly updates various displays
        _thread.start_new_thread(self.update, ())

    #Makes selection more tablelike (row select instead of single listbox element)
    def select_row(self, event):
        #Gets the selection of the listbox that was clicked
        self.selection = event.widget.curselection()

        #Sets the other column listboxes to have the same selection
        for j in range(0, len(self.listboxes)):
            self.listboxes[j].selection_clear(0, len(self.curData[0]))
            for k in range(0, len(self.selection)):
                self.listboxes[j].selection_set(self.selection[k])
                
    #Sorts the listboxes based upon a column
    def sort(self, event):
        #Index of the listbox that user is sorting by
        self.index = 0
        #Determines in what order to sort the listbox
        self.parse = event.widget["text"].split(" ")

        for self.header in self.headers:
            #Finds the index of the listbox that the user wants to sort
            if (self.header == event.widget):
                self.index = self.headers.index(self.header)

            #Resets all the buttons to the neutral sort (dash instead of arrow)
            self.parsed = self.header["text"].split(" ")
            if (self.parsed[len(self.parsed) - 1] != "-"):
                self.parsed = self.parsed[0:len(self.parsed) - 1]
                self.header.config(text = " ".join(self.parsed) + " -")

        #Creates a list of data [team1, team2, league, datetime] to unzip so that sorting does not lose matches
        self.zipping = []
        self.zipping.append(tuple(self.curData[self.index]))
        for i in range(0, len(self.curData)):
            if (i != self.index):
                self.zipping.append(self.curData[i])
        #Unzips the list into the table rows instead of columns
        self.rows = list(zip(*self.zipping))

        #Checks to see whether the list is not sorted
        if (self.parse[len(self.parse) - 1] == "-"):
            #Changes the visual of the button to represent the sorting
            self.parse.remove("-")
            event.widget.config(text = " ".join(self.parse) + " " + u"\N{BLACK DOWN-POINTING TRIANGLE}")
            #Sorts the list in decending order
            self.rows = sorted(self.rows)

        #Checks to see if the list is sorted decending
        elif (self.parse[len(self.parse) - 1] == u"\N{BLACK DOWN-POINTING TRIANGLE}"):
            #Changes the visual of the buton to represent acending sorting
            self.parse.remove(u"\N{BLACK DOWN-POINTING TRIANGLE}")
            event.widget.config(text = " ".join(self.parse) + " " + u"\N{BLACK UP-POINTING TRIANGLE}")
            #Sorts the list in acending order
            self.rows = sorted(self.rows, reverse = True)

        #Checks to see if the list is sorted in acending order
        elif (self.parse[len(self.parse) - 1] == u"\N{BLACK UP-POINTING TRIANGLE}"):
            #Changes the visual of the button to represent decending sorting
            self.parse.remove(u"\N{BLACK UP-POINTING TRIANGLE}")
            event.widget.config(text = " ".join(self.parse) + u"\N{BLACK DOWN-POINTING TRIANGLE}")
            #Sorts the list in decending order
            self.rows = sorted(self.rows)

        #Unzips the data back into its columns
        self.data = list(zip(*self.rows))
        
        #Replaces old data with new sorted data
        self.columnCounter = 1
        for i in range(0, len(self.curData)):
            if (i == self.index):
                self.curData[i] = self.data[0]
            else:
                self.curData[i] = self.data[self.columnCounter]
                self.columnCounter = self.columnCounter + 1

        #Updates thelistboxes with the new sorted data
        for i in range(0, len(self.listboxes)):
            for j in range(0, len(self.curData[i])):
                self.listboxes[i].delete(j)
                self.listboxes[i].insert(j, self.curData[i][j])

        self.refresh_curdata()

    #Scrolls all the listboxes as one giant listbox
    def scroll_all(self, *args):
        for self.listbox in self.listboxes:
            self.listbox.yview(*args)

    #Gets the currently selected indexs in the custom table
    def curselection(self):
        return self.listboxes[0].curselection()

    #Gets the current data in the listboxes and puts it into a list
    def refresh_curdata(self):
        self.curData = []
        for i in range(0, len(self.listboxes)):
            self.curData.append(list(self.listboxes[i].get(0, tk.END)))

    #Loop that continuously updates various functionalities
    def update(self):
        while(True):
            #Checks to see whether the search box is used
            if (self.searchable):
                #Grabs the text from the search box and uses it to search the table
                self.update_key()
            #Updates the between row headers to stay next to the current data in the list
            self.update_betweenRowHeaders()

    #Updates the beteween headers to follow the current data
    def update_betweenRowHeaders(self):
        #Checks the difference between the number of data and the number of headers
        self.diff = len(self.betweenListboxes[0].get(0, tk.END)) - len(self.curData[0])

        #If the numbers do not match then update
        if (self.diff != 0):
            #Enables the listbox to display headers for changes
            for i in range(0, len(self.betweenListboxes)):
                self.betweenListboxes[i].config(state = tk.NORMAL)

            #Delete labels that do not correspond to a data column
            if (self.diff > 0):
                for i in range(0, len(self.betweenListboxes)):
                    for j in range(0, self.diff):
                        self.betweenListboxes[i].delete(tk.END)
            #Insert labels that are missing in the data column 
            elif (self.diff < 0):
                for i in range(0, len(self.betweenListboxes)):
                    for j in range(0, (self.diff * -1)):
                        self.betweenListboxes[i].insert(tk.END, self.betweenRowHeaders[i])

            #Disables the listbox to display headers for effect
            for i in range(0, len(self.betweenListboxes)):
                self.betweenListboxes[i].config(state = tk.DISABLED)
    
    #Updates the search key
    def update_key(self):
        self.lastKey = self.key
        self.key = self.sortEntry.get()
        #Checks to see whether the text in the entry box has changed
        if (self.key != self.lastKey):
            #Limits table display to entry box text
            self.limit_selection_to(self.key.lower())

    #Checks table for the key that is passed and then limits display to rows with that key
    def limit_selection_to(self, key):
        #Determines which columns to sort through
        self.startColumn = 0
        self.endColumn = len(self.listboxes)

        #Sorts by column if the user entered a column name followed by a :
        for i in range(0, len(self.columnHeaders)):
            if (key[0:len(self.columnHeaders[i]) + 1] == (self.columnHeaders[i].lower() + ":")):
                #Sets the key to everything after the :
                key = key[len(self.columnHeaders[i]) + 1:len(key)]
                #Makes sure to serach through only the one column
                self.startColumn = i
                self.endColumn = i + 1
                break

        #Searches through the table to find rows with the key
        self.limitedData = []
        for i in range(0, len(self.columnData[0])):
            for j in range(self.startColumn, self.endColumn):
                #Checks to see whether the listbox column has the key
                if (self.columnData[j][i].lower().find(key) != -1):
                    #Appends the index of the listbox to the list of data to display
                    self.limitedData.append(i)
        #Removes all duplicate indexes found in the list
        self.limitedData = list(set(self.limitedData))

        #Clears the entire table
        for i in range(0, len(self.listboxes)):
            for j in range(0, len(self.columnData[i])): 
                self.listboxes[i].delete(0)
    
        #Adds the limited data to the table
        for i in range(0, len(self.listboxes)):
            for j in range(0, len(self.limitedData)):
                self.listboxes[i].insert(tk.END, self.columnData[i][self.limitedData[j]])

        #Refreshs the current data list to the new set of limited data that is displayed
        self.refresh_curdata()
