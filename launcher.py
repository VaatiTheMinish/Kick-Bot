import platform
import requests
import subprocess
import os

python_interpreter = "venv/bin/python" if platform.system() == "Linux" else "venv\\Scripts\\python.exe"

import configparser
import os
import requests

message = ""

def check_version():
    config_file = "config/config.ini"
    global bot_version
    global message
    bot_version = ""

    # Read the bot's version from the config file
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        bot_version = config.get("version", "version")
    except:
        global message
        bot_version = '????'
        message = "Config does not exist, please run setup first"

    # Fetch the latest version from example.com/version.txt
    try:
        response = requests.get("https://raw.githubusercontent.com/VaatiTheMinish/Kick-Bot/main/version.txt")
        latest_version = response.text.strip()

        if latest_version != bot_version:
            print(f"You are on version: {bot_version} ")
            update_choice = input(f"A new version is available {latest_version}. Do you want to update? (y/N): ")
            message = (f"New Version Detected: {latest_version}")
            if update_choice.lower() == "y":
                updater()
    except requests.exceptions.RequestException:
        message = ("Failed to fetch the latest version. Skipping update check.")


def setup():
    subprocess.run(["python", "setup/setup.py"])
    global message
    message = ("Setup has completed. You may now start the bot.")

def run_bot():
    subprocess.run([f"{python_interpreter}", "bot/bot.py"])

def run_bypass_script():
    subprocess.Popen(["bypass.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    global message
    message = "Please wait for the message starting in the window that opened"

def updater():
    global message
    message = ("Updater coming soon")

def main_menu():
    if not os.path.exists("config/config.ini"):
        global message
        message = ("Detected first launch. Please run setup")


    while True:
        os.system("clear")
        print("Status: " + message)
        print("Kick Bot launcher V1")
        print(f"Bot Version: {bot_version}")
        print("Main Menu:")
        print("1. Run Setup")
        print("2. Run Bot")
        print("3. Run Bypass Script")
        print("4. Check for and update")
        print("5. Exit")
        choice = input("Enter your choice: ")


        match choice:
            case "1":
                setup()
            case "2":
                run_bot()
            case "3":
                run_bypass_script()
            case "4":
                updater()
            case "5":
                break
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    check_version()
    main_menu()
