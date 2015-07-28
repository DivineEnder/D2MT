#Imports gui python tools
import tkinter as tk

#Creates a custom widget formed from several listboxes which resembles a table
class Table(tk.Frame):

    def __init__(self, master, columnLabels, columnData):
        #Initializes a frame that the table is going to be displayed in
        tk.Frame.__init__(self, master)

        #Gets the column data and labels for the columns
        self.columnLabels = columnLabels
        self.columnData = columnData

        #Displays the column labels above respective columns
        self.labels = []
        for i in range(0, len(self.columnLabels)):
            self.labels.append(tk.Label(self, text = self.columnLabels[i], justify = tk.CENTER, fg = "black"))
            self.labels[i].grid(row = 0, column = i)

        #Creates listboxes as columns for the table
        self.listboxes = []
        for i in range(0, len(self.columnData)):

            #Sets the width of the listboxes to the length of the max data/label
            self.width = 0
            if (len(self.labels[i]["text"]) > len(max(self.columnData[i]))):
                self.width = len(self.labels[i]["text"]) + 1
            else:
                self.width = len(max(self.columnData[i])) + 1
                
            #Creates the listbox and adds it to the list
            self.listboxes.append(tk.Listbox(self, selectmode = tk.EXTENDED, activestyle = tk.NONE, exportselection = 0, height = len(self.columnData[i]), width = self.width))

            #Adds all the data sent to the widget to the listboxes
            for self.element in self.columnData[i]:
                self.listboxes[i].insert(tk.END, self.element)

            #Causes row select on click of element
            self.listboxes[i].bind("<<ListboxSelect>>", self.select_row)

            #Displays listboxes in column
            self.listboxes[i].grid(row = 1, column = i)

    #Makes selection more tablelike (row select instead of single listbox element)
    def select_row(self, event):
        #Gets the selection of the listbox that was clicked
        self.selection = event.widget.curselection()

        #Sets the other column listboxes to have the same selection
        for j in range(0, len(self.listboxes)):
            self.listboxes[j].selection_clear(0, len(self.columnData[0]))
            for k in range(0, len(self.selection)):
                self.listboxes[j].selection_set(self.selection[k])

    #Gets the currently selected indexs in the custom table
    def curselection(self):
        return self.listboxes[0].curselection()
