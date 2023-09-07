from datetime import datetime, timedelta, timezone
from modules.database import db_context



#adds points to the user, if there is a cooldown or just to simply add them
async def addpoints(username, userid, points, cooldown=None):
    utc_now = datetime.now(timezone.utc)
    async with db_context as db:
        points_collection = db.users
        user = await points_collection.find_one({"_id": userid})
        if not user:
            await points_collection.insert_one({'username': username, '_id': userid, 'points': 0, 'cooldown': utc_now - timedelta(seconds=30)})
            user = await points_collection.find_one({"username": username, "_id": userid})
        if not cooldown or (cooldown and user['cooldown'].replace(tzinfo=timezone.utc) < utc_now):
            await points_collection.update_one({'_id': userid}, {'$inc': {'points': int(points)}, '$set': {'cooldown': utc_now + timedelta(seconds=30)}})

#create_user_ifnotexist
async def addusertodb(username, userid):
    utc_now = datetime.now(timezone.utc)
    async with db_context as db:
        points_collection = db.users
        if await points_collection.find_one({"username": username, "_id": userid}):
            return
        else:
            await points_collection.insert_one({'username': username, '_id': userid, 'points': 0, 'cooldown': utc_now - timedelta(seconds=30)})
    return

#Set how many points a user has
async def setpoints(userid, points):
    async with db_context as db:
        points_collection = db.users
        await points_collection.update_one({'_id': userid}, {'$set': {'points': points}})

#Removes a number of points from a user
async def rmpoints(userid, points):
    async with db_context as db:
        points_collection = db.users
        await points_collection.update_one({'_id': userid}, {'$inc': {'points': -points}})

#Sets the users points back to 0
async def resetpoints(userid):
    await setpoints(userid, 0)


#View a users points by simply returning the number of points
async def viewpoints(userid):
    async with db_context as db:
        points_collection = db.users
        user = await points_collection.find_one({'_id': userid})
        return user['points'] if user else None

#Show the users points with the !points command
async def showpoints(userid):
    async with db_context as db:
        points_collection = db.users
        user = await points_collection.find_one({'_id': userid})
        if user:
            return f"{user['username']} has {round(user['points'])} Points!"
        else:
            return f"No record found for the user with ID {userid}"
