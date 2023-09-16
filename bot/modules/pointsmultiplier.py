import logging
from modules.database import db_context
from kick import Message

#Points Multiplier based on the users badges, applys to the highest badge the user has

async def pointsmultiplier(msg: Message, points):
    async with db_context as db:
        pointsmultiplier = await db.general.find_one({"name": "multiplier"})
        if not pointsmultiplier['enabled']:
            return 1
            #print("Not enabled")

        badges = msg.author.badges
        badge_types = [badge['type'] for badge in badges]

        if pointsmultiplier is not None:
            multiplier = None

            for badge_type in badge_types:
                if badge_type in pointsmultiplier:
                    multiplier = float(pointsmultiplier[badge_type].to_decimal())
                    break

            if multiplier is not None:
                result = points * multiplier
                logging.info(result)
            else:
                result = points * 1
                logging.info(result)
                #print("No valid badge found in the pointsmultiplier document")
        else:
            print("Points multiplier data does not exist in the database")
    return result
