import time
from collections import defaultdict

cooldown_dict = defaultdict(dict)

#the core to the cooldown system witl all the commands

async def command_cooldown(userid, command, cooldown_duration):
    current_time = time.time()

    if userid in cooldown_dict and command in cooldown_dict[userid] and current_time - cooldown_dict[userid][command] < cooldown_duration:
        return True

    cooldown_dict[userid][command] = current_time
    return False
