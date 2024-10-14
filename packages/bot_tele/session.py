from telegram import User

users = {}


async def init_session(user: User) -> None:
    user_id = str(user.id)
    if not user_id in users:
        users[user_id] = {
            "user_id": user_id,
            "full_name": user.full_name,
        }
    return users[user_id]

async def get_session(user: User): 
    if not str(user.id) in users:
        await init_session(user)
    return users[str(user.id)]

async def update_session(user: User) -> None:
    user_id = str(user.id)
    if not user_id in users:
        await init_session(user)
    users[user_id] = {**users[user_id] }
    return users[user_id]


