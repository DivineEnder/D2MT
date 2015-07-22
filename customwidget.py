import tkinter as tk
from tkinter import font

class FitListbox(tk.Listbox):

    def autowidth(self, maxwidth=100):
        autowidth(self, maxwidth)


def autowidth(list, maxwidth=100):
    f = font.Font(font=list.cget("font"))
    pixels = 0
    for item in list.get(0, "end"):
        pixels = max(pixels, f.measure(item))
    # bump listbox size until all entries fit
    pixels = pixels + 10
    width = int(list.cget("width"))
    for w in range(0, maxwidth+1, 5):
        if list.winfo_reqwidth() >= pixels:
            break
        list.config(width=width+w)
