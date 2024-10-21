from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

UserQuery = Query()


@dataclass
class User:
    user_id: str
    name: str
    username: str | None = None
    password: str | None = None


class UserManager:
    async def get_one(self, user_id):
        if not user_id:
            raise Exception("User ID is required")
        
        account = await db_manager.read(COLLECTIONS.USERS, UserQuery.user_id == user_id)
        return User(**account[0]) if account else None
    
    async def get_by_username(self, username):
        if not username:
            raise Exception("Username is required")
        
        users = await db_manager.read(COLLECTIONS.USERS, UserQuery.username == username)
        return User(**users[0]) if users else None

    async def get_all(self):
        users = await db_manager.read(COLLECTIONS.USERS)
        return [User(**user) for user in users]

    async def get_or_create(self, user_id, name, username, password):
        user = await self.get_one(user_id)
        if user:
            return user
        user = await db_manager.create(COLLECTIONS.USERS, User(user_id, name, username, password).__dict__)
        return User(**user)

    async def login(self, username, password):
        user = await self.get_by_username(username)
        if not user:
            return False
        return user.password == password


async def create_superuser():
    user = await UserManager().get_or_create(
        "akhsdiwalskncoi932nn230293njb3b2", "Super User","admin", "admin"
    )
    return user