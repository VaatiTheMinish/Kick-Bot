# How to setup and run the kick self hosted streaming bot

1. Download and install: python 3.11 or later and git
2. Download the [Latest release]()
3. Extract the zip to a folder 
4. **For Windows 10:**

- Shift right-click in the directory, making sure no files are selected.
- Click 'Open PowerShell window here'.

4. **For Windows 11:**
- Right-click in the folder.
- Click 'Terminal'.

5. run the command 'python launcher.py' 
6. In the manu that opens, if there is a update for now we can ignore the message by hitting 'N' or just pressing enter. When we are in the main menu, we will want to press 1 to run setup

7. Once we are in the setup we will need to press 'y' to recreate the credentials for both credentials and database,

8. It will ask for your channel, the bots credentials, and the database string and name
- Enter your channel - Here you will put your channel you want the bot to be on
- Enter Bot's Email: - Put the email used to login to the bot here
- Enter Bot's Password: - Put the password used to log into the bot

When we get to this part please follow [Database setup guide](https://github.com/VaatiTheMinish/Kick-Streaming-Bot/blob/main/docs/installation/database.md), then come back to this step
- Enter MongoDB Connection String: Paste the connection string provided, make sure to change the values
- Enter MongoDB Database name: this is the <database> value in the connection string

After this completes, the bot will finish the setup script and take you back to the main menu

9. We need to run the bypass script to allow the bot to connect. so we will press '3'
A new window will open and we will wait for it to display 'starting'. Once that is running, leave the window open

10. We can now run the bot press '2' on the main menu


