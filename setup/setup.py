import json
import platform
import subprocess
import os
import sys
import pymongo
from pymongo.errors import ConnectionFailure
from bson.json_util import loads
from configparser import ConfigParser


def check_git_installed():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Error: 'git' is not installed. Please install git before running this script.")
        sys.exit(1)

def save_config_to_file(config):
    with open("config/config.ini", "w") as config_file:
        config.write(config_file)

def import_collections(config, db_name, json_filename, collection_name):
    try:
        db_client = pymongo.MongoClient(config.get('database', 'mongodb_string'))
        db_client.admin.command('ismaster')
    except ConnectionFailure:
        print("Could not connect to the server. Please check your MongoDB connection string.")
        return

    database_name = config.get('database', 'databasename')  # Read the database name from the INI file

    if not database_name:
        print("Error: Database name is missing in the INI file.")
        return

    db = db_client[database_name]

    try:
        with open(json_filename, "r") as json_file:
            json_str = json_file.read()
            data = loads(json_str)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filename}. Please check the file format.")
        return

    collection = db[collection_name]

    for document in data:
        # Check if document already exists in the collection
        if collection.count_documents(document) > 0:
            print(f"Document {document} already exists in {collection_name}. Skipping import.")
        else:
            collection.insert_one(document)
            print(f"Document {document} imported into {collection_name}.")

    print(f"Data import for {collection_name} completed.")



def get_existing_credentials(config):
    return config.get('botcredentials', 'channel'), config.get('botcredentials', 'username'), config.get('botcredentials', 'password')

def get_existing_database_string(config):
    return config.get('database', 'mongodb_string'), ""

def main():
    check_git_installed()

    config = ConfigParser()
    config_file = "config/config.ini"
    config.read(config_file)
    # Check if config.ini file exists
    if not config.has_section('database'):
        recreate_db_string = "y"
    if not config.has_section('botcredentials'):
        recreate_creds = "y"
    else:
        config.read('config/config.ini')
        recreate_creds = input("Credentials Exist? Recreate y/N: ")
        recreate_db_string = input("Database connection string exists? Recreate y/N: ")

    if recreate_creds.lower() == "y":
        channel = input("Enter the channel: ")
        bot_email = input("Enter Bot's Email: ")
        bot_password = input("Enter Bot's Password: ")

        print("Recreating botcredentials in config.ini...")
        if not config.has_section('botcredentials'):
            config.add_section('botcredentials')
        config.set('botcredentials', 'channel', channel)
        config.set('botcredentials', 'username', bot_email)
        config.set('botcredentials', 'password', bot_password)
        save_config_to_file(config)
    else:
        print("Skipping recreation of botcredentials in config.ini.")
        channel, bot_email, bot_password = get_existing_credentials(config)

    if recreate_db_string.lower() == "y":
        mongodb_string = input("Enter MongoDB Connection String: ")
        database_name = input("Enter MongoDB Database name: ")

        print("Recreating mongodb_string in config.ini...")
        if not config.has_section('database'):
            config.add_section('database')
        config.set('database', 'mongodb_string', mongodb_string)
        config.set('database', 'databasename', database_name)
        save_config_to_file(config)
    else:
        print("Skipping recreation of mongodb_string in config.ini.")
        mongodb_string, database_name = get_existing_database_string(config)

    # Save config.ini
    save_config_to_file(config)

    # Create virtual environment
    subprocess.run(["python", "-m", "venv", "venv"])

    # Determine activation script and Python interpreter based on OS
    activate_script = "venv/bin/activate" if platform.system() == "Linux" else "venv\\Scripts\\activate"
    python_interpreter = "venv/bin/python" if platform.system() == "Linux" else "venv\\Scripts\\python.exe"

    # Activate virtual environment
    activate_command = f"source {activate_script}" if "posix" in os.name else f"{activate_script}"
    subprocess.run(activate_command, shell=True)

    # Install dependencies using the Python interpreter from the virtual environment
    subprocess.run([python_interpreter, "-m", "pip", "install", "-r", "setup/requirements.txt"])

    # Import data into MongoDB collections
    import_collections(config, database_name, "setup/general.json", "general")
    import_collections(config, database_name, "setup/commands.json", "commands")
    print("setup.py completed")

if __name__ == "__main__":
    main()
