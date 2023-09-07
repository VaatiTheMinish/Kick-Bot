from modules.database import db_context
from kick import Message

#Points Multiplier based on the users badges, applys to the highest badge the user has

async def pointsmultiplier(msg: Message, points):
    async with db_context as db:
        pointsmultiplier = await db.general.find_one({"name": "multiplier"})
        if not pointsmultiplier['enabled']:
            print(points)
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
                print(result)
            else:
                result = points * 1
                print(result)
                #print("No valid badge found in the pointsmultiplier document")
        else:
            print("No document found with name 'multiplier'")
    return result

#TODO 
# {'type': 'sub_gifter', 'text': 'Sub Gifter', 'count': 4}
# {'type': 'subscriber', 'text': 'Subscriber', 'count': 1}
# sub_gifter count 1 25 50 100 200