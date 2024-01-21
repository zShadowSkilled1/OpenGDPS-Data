import requests
import os
import urllib
import shutil
from zipfile import ZipFile
import subprocess

updateUrl = ""

appData = os.getenv('APPDATA')
openGDPSDir = appData + "\OpenGDPSLauncher"

def launch():
    openGDPS_directory = os.path.join(openGDPSDir, "OpenGDPS")

    # Find OpenGDPS.exe within the OpenGDPS directory
    exe_file_path = None
    for root, dirs, files in os.walk(openGDPS_directory):
        for file in files:
            if file.lower() == "opengdps.exe":
                exe_file_path = os.path.join(root, file)
                break

    if exe_file_path:
        print(f"Launching OpenGDPS: {exe_file_path}")
        subprocess.Popen(exe_file_path)
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

def checkUpdate():
    # Get the latest version from the GitHub repository
    version_response = requests.get("https://raw.githubusercontent.com/zShadowSkilled1/OpenGDPS-Data/main/Data/version.txt")
    latest_version = version_response.text.strip()

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
        for root, dirs, files in os.walk(openGDPS_directory):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print("Removed file:", file)

            for directory in dirs:
                dir_path = os.path.join(root, directory)
                os.rmdir(dir_path)
                print("Removed directory:", directory)

        # Download and unzip the update
        endpoint = requests.get("https://raw.githubusercontent.com/zShadowSkilled1/OpenGDPS-Data/main/Data/updateUrl.txt")
        update_url = endpoint.text
        update_path = os.path.join(openGDPSDir, "update.zip")

        update_response = requests.get(update_url)

        with open(update_path, "wb") as update_zip:
            update_zip.write(update_response.content)

        # Unzip the update
        with ZipFile(update_path, 'r') as zip_ref:
            zip_ref.extractall(openGDPS_directory)

        print('Update completed.')
        print('Launching OpenGDPS.')
        launch()

createDataFolder()
