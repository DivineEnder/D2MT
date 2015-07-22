import os

#Takes a package name and installs that package
def install(package):
    import pip
    pip.main(["install", package])

#Installs the needed modules for the script to run
install("httplib2")
install("google-api-python-client")
install("BeautifulSoup4")
install("requests")
#Not need in python 3
#install("python-tk")

##    try:
##        file = "D2MT.py"
##        name = os.path.splitext(file)[0]
##        os.rename(file, name + ".pyw")
##    except FileNotFoundError:
##        print("Modules already installed")
