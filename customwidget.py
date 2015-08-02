#Imports gui python tools
import tkinter as tk

#Creates a custom widget formed from several listboxes which resembles a table
class Table(tk.Frame):

    def __init__(self, master, columnHeaders, columnData):
        #Initializes a frame that the table is going to be displayed in
        tk.Frame.__init__(self, master)

        #Gets the column data and labels for the columns
        self.columnHeaders = columnHeaders
        self.columnData = columnData

        #Displays the column headers above respective columns (buttons for sorting purposes)
        self.headers = []
        for i in range(0, len(self.columnHeaders)):
            self.headers.append(tk.Button(self, text = self.columnHeaders[i] + " -"))
            #Using bind instead of built in command because bind sends event which a widget can be pulled from
            self.headers[i].bind("<Button-1>", self.sort)
            self.headers[i].grid(row = 0, column = i, padx = 3, pady = 1)

        #Creates listboxes as columns for the table
        self.listboxes = []
        for i in range(0, len(self.columnData)):

            #Sets the width of the listboxes to the length of the max data/label
            self.width = 0
            if (len(self.headers[i]["text"]) > len(max(self.columnData[i]))):
                self.width = len(self.headers[i]["text"]) + 3
            else:
                self.width = len(max(self.columnData[i])) + 1
                
            #Creates the listbox and adds it to the list
            self.listboxes.append(tk.Listbox(self, selectmode = tk.EXTENDED, activestyle = tk.NONE, exportselection = 0, height = 15, width = self.width))

            #Adds all the data sent to the widget to the listboxes
            for self.element in self.columnData[i]:
                self.listboxes[i].insert(tk.END, self.element)

            #Causes row select on click of element
            self.listboxes[i].bind("<<ListboxSelect>>", self.select_row)

            #Displays listboxes in column
            self.listboxes[i].grid(row = 1, column = i)

        if (len(columnData) > 15):
            self.scrollbar = tk.Scrollbar(self)
            self.scrollbar.grid(row = 1, column = len(self.columnData), sticky = "NS")
            self.scrollbar.config(command = self.scroll_all)

    #Makes selection more tablelike (row select instead of single listbox element)
    def select_row(self, event):
        #Gets the selection of the listbox that was clicked
        self.selection = event.widget.curselection()

        #Sets the other column listboxes to have the same selection
        for j in range(0, len(self.listboxes)):
            self.listboxes[j].selection_clear(0, len(self.columnData[0]))
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
        self.zipping.append(tuple(self.columnData[self.index]))
        for i in range(0, len(self.columnData)):
            if (i != self.index):
                self.zipping.append(self.columnData[i])
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
        for i in range(0, len(self.columnData)):
            if (i == self.index):
                self.columnData[i] = self.data[0]
            else:
                self.columnData[i] = self.data[self.columnCounter]
                self.columnCounter = self.columnCounter + 1

        #Updates thelistboxes with the new sorted data
        for i in range(0, len(self.listboxes)):
            for j in range(0, len(self.columnData[i])):
                self.listboxes[i].delete(j)
                self.listboxes[i].insert(j, self.columnData[i][j])

    #Scrolls all the listboxes as one giant listbox
    def scroll_all(self, *args):
        for self.listbox in self.listboxes:
            self.listbox.yview(*args)

    #Gets the currently selected indexs in the custom table
    def curselection(self):
        return self.listboxes[0].curselection()
