# A Self hosted Kick Bot
Made by Ryohei



# Commands
All the non file based commands supports the following args
- [sender] - this will return the name of the person who sent the command

- (arg[num]) - this will break the text after the command into arguments  For example if you create a command !test (arg1) (arg2) the usage will be !test example 123

### addcmd
- addcmd (name) (text)

### edit cmd
- addalias (command name) (alias)
- enabled (command name) (true|false)
- cost (command name) (int)
- cooldown (command name) (int)
- message (command name) (string)
- permission (command name) (0|1|2|3|4|5)
- file (command name) (true|false)
- cooldowntype (command name) (global|user)
- delete (command name)

### apoints
the admin command for managing the users points
- add (username) (int)
- set (username) (int)
- reset (username)
- rm (username) (int)


## Text-to-Speech (TTS) Settings

### tts
- **cooldown** (int): How long to wait before reading the user's next message
- **maxchars** (int): The maximum length of the TTS message before characters are skipped
- **maxint** (int): The maximum number of numbers the TTS should read
- **enabled** (options: chat|cmd|off): Toggle for TTS (chat, command, or off)

## Default Bot Module Settings
usage !settings (name)

### points
- **enabled** (bool): Should a user receive points for sending a chat message
- **cooldown** (int): Time interval before a user can earn more points
- **amount range**: The range of points awarded per chat message



### pointsmultiplier
- **enabled**: Whether to apply a points multiplier based on user badges
- **set**
    - **vip** (float)
    - **og** (float)
    - **founder** (float)
    - **subscriber** (float)
    - **mod** (float)
    - **broadcaster** (float) 



