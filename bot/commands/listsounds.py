import os
from kick import Message

def parse_message_content(message_content: str):
        '''Parses the page number from message content. Returns 1 if no valid number found.'''
        components = message_content.split()
        if len(components) > 1 and components[1].isdigit():
            return int(components[1])
        else:
            return 1

async def listsounds(message: Message):
        # Parse the desired page number from message content
        page_num = parse_message_content(message.content)
        
        # The path to look for the files
        directory = "sounds/"
        
        # List all .mp3 files in directory, remove '.mp3' part from each name
        filenames = [f.replace('.wav', '') for f in os.listdir(directory) if f.endswith('.wav')]
        
        # Define the number of results per page and calculate start and end indices for slicing
        PAGE_SIZE = 10
        start_index = (page_num - 1) * PAGE_SIZE
        end_index = start_index + PAGE_SIZE
        files = filenames[start_index:end_index]
        
        # Calculate max page number for display
        max_page = (len(filenames)-1) // PAGE_SIZE + 1
        
        await message.chatroom.send(
            f"Viewing page {page_num}/{max_page}: {', '.join(files)}")
