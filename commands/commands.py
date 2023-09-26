import os
from kick import Message
from core.permissions import PermissionSystem
from core.database import db_context

permission_system = PermissionSystem()

def parse_message_content(message_content: str):
        '''Parses the page number from message content. Returns 1 if no valid number found.'''
        components = message_content.split()
        if len(components) > 1 and components[1].isdigit():
            return int(components[1])
        else:
            return 1

async def commands(message: Message):
    # Parse the desired page number from message content
    page_num = parse_message_content(message.content)
    
    # Query the database to get the command documents
    async with db_context as db:
        command_docs = await db.commands.find().to_list(length=None)
    
    # Extract the command names from the command documents
    command_names = [doc['name'] for doc in command_docs]

    badges = message.author.badges
    badge_types = [badge['type'] for badge in badges]
    user_permission = await permission_system.get_permission_level(badge_types)
    # Get the user's permission level
    #badges = message.author.badges
    #badge_types = [badge['type'] for badge in badges]
    #user_permission = await PermissionSystem.get_permission_level(badge_types)
    
    # Filter the commands based on user's permission level
    accessible_commands = [doc['name'] for doc in command_docs if user_permission >= doc['permission']]
    
    # Define the number of results per page and calculate start and end indices for slicing
    PAGE_SIZE = 10
    start_index = (page_num - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    commands = accessible_commands[start_index:end_index]
    
    # Calculate max page number for display
    max_page = (len(accessible_commands)-1) // PAGE_SIZE + 1
    
    await message.chatroom.send(
        f"@{message.author.slug} - Viewing page {page_num}/{max_page}: {', '.join(commands)}"
)
