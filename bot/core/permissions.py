#the permission handler for the bot
#this checks if they have the appropiate badge to if they can run the command

class PermissionSystem:
    def __init__(self):
        self.permissions = {
            None: 0,
            'vip': 1,
            'og': 2,
            'founder': 2,
            'subscriber': 3,
            'moderator': 4,
            'broadcaster': 5
        }

    async def get_permission_level(self, badge_types):
        if not badge_types:
            return 0
        max_permission = 0
        for badge_type in badge_types:
            if badge_type in self.permissions:
                permission_level = self.permissions[badge_type]
                if permission_level > max_permission:
                    max_permission = permission_level
        return max_permission
