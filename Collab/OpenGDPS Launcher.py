import os
import urllib.request
import shutil
import zipfile
from zipfile import *
import requests
import io
from tkinter import *
import webbrowser
import subprocess
import time
import threading
from os import path

updateUrl = ""

appData = os.getenv('APPDATA')
openGDPSDir = appData + "\OpenGDPSLauncher"

def launch():
    createDataFolder()
    checkUpdate()
    openGDPS_directory = os.path.join(openGDPSDir, "OpenGDPS")

    # Find OpenGDPS.exe within the OpenGDPS directory
    exe_file_path = None
    for root, dirs, files in os.walk(openGDPS_directory):
        for file in files:
            if file.lower() == "opengdps.exe":
                startDir = root
                exe_file_path = os.path.join(root, file)
                exeFile = file

    if exe_file_path:
        print(f"Launching OpenGDPS: {exe_file_path}")
        print(f'Current Working Directory: {startDir}')
        print(f'Executable Name: {exeFile}')
        
        dirCommand = startDir.replace('\\', "/")
        launchCommand = f'{exeFile}'

        commands = [dirCommand, launchCommand]

        print(f'Launch Command: {launchCommand} {dirCommand}')
        os.chdir(dirCommand)
        subprocess.call(exeFile)
    else:
        print("OpenGDPS.exe not found.")

def getVersion():
    currentVersion = requests.get("https://raw.githubusercontent.com/zShadowSkilled1/OpenGDPS-Data/main/Data/version.txt")
    return currentVersion.text

def createDataFolder():
    global openGDPSDir
    global appData
    
    if os.path.exists(appData + "\OpenGDPSLauncher"):
        print('Already ready.')
        checkUpdate()
    else:
        os.mkdir(appData + "\OpenGDPSLauncher")
        print('OpenGDPS Folder Created')

        openGDPSData = open(openGDPSDir + "\currentVersion.txt", "w")
        os.mkdir(openGDPSDir + r"\OpenGDPS")
        openGDPSDataContent = getVersion()
        openGDPSData.write(openGDPSDataContent)

def download_and_unzip_update(update_url, update_path, openGDPS_directory):
    try:
        # Download the update
        update_response = urllib.request.urlopen(update_url)
        with open(update_path, "wb") as update_zip:
            update_zip.write(update_response.read())

        # Unzip the update
        with ZipFile(update_path, 'r') as zip_ref:
            zip_ref.extractall(openGDPS_directory)

        # Update the version file
        with open(os.path.join(openGDPSDir, "currentVersion.txt"), "w") as openGDPSData:
            openGDPSData.write(getVersion())
            openGDPSData.close()


        print('Update completed.')
        print('Launching OpenGDPS.')
        launch()
    except Exception as e:
        print(f"Error during update: {e}")

def checkUpdate():
    # Get the latest version from the GitHub repository
    version_response = urllib.request.urlopen("https://raw.githubusercontent.com/zShadowSkilled1/OpenGDPS-Data/main/Data/version.txt")
    latest_version = version_response.read().decode('utf-8').strip()

    # Read the current version from the local file
    current_version_path = os.path.join(openGDPSDir, "currentVersion.txt")
    with open(current_version_path, "r") as version_file:
        current_version = version_file.read().strip()

    print("Latest Version:", latest_version)
    print("Current Version:", current_version)

    if latest_version == current_version:
        print('Up to date.')
    else:
        print('Updating')

        # Remove all files and folders in the OpenGDPS directory
        openGDPS_directory = os.path.join(openGDPSDir, "OpenGDPS")

        # Deleting contents of the OpenGDPS directory
        for root, dirs, files in os.walk(openGDPS_directory):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)

        # Download and unzip the update in a separate thread
        update_url_response = urllib.request.urlopen("https://raw.githubusercontent.com/zShadowSkilled1/OpenGDPS-Data/main/Data/updateUrl.txt")
        update_url = update_url_response.read().decode('utf-8').strip()
        update_path = os.path.join(openGDPSDir, "update.zip")

        # Create a thread for downloading and unzipping the update
        update_thread = threading.Thread(target=download_and_unzip_update, args=(update_url, update_path, openGDPS_directory))
        update_thread.start()

        print('Update process started in the background.')

def OpenDiscord():
    webbrowser.open("https://discord.gg/V6z24dRf")

def OpenWebside():
    webbrowser.open("https://opengdps.vercel.app/")

root = Tk()
root.geometry('420x300')
root.title("OpenGDPS")

# Function to update the status text
update_status_var = StringVar()
update_status_var.set("Ready")
update_status_label = Label(root, textvariable=update_status_var)
update_status_label.pack()

OpenGDPS = Label(root, text="OpenGDPS")
OpenGDPS.pack()

# Launch button
launchButton = Button(root, text="Launch OpenGDPS", command=launch, width=20)
launchButton.pack(side=TOP, pady=5)

# Get Version button
getVersionBtn = Button(root, text="Get Version", command=getVersion, width=20)
getVersionBtn.pack(side=TOP, pady=5)

# Check Update button
checkUpdateBtn = Button(root, text="Check Update", command=checkUpdate, width=20)
checkUpdateBtn.pack(side=TOP, pady=5)

# Discord button
OpenDiscordbtn = Button(root, text="Buage. Discord", command=OpenDiscord, width=20)
OpenDiscordbtn.pack(side=TOP, pady=5)

# Website button
Website = Button(root, text="Website", command=OpenWebside, width=20)
Website.pack(side=TOP, pady=5)

root.mainloop()
