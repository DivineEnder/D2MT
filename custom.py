#Imports a library used to access certain os features (cmd in this case)
import os

#Own number to string function that places a zero in front of a single digit number
def toString(n):
    if (n < 10):
        return "0" + str(n)
    else:
        return str(n)

#Clears the command line current screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])
