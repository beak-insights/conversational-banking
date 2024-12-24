from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

UserQuery = Query()


@dataclass
class User:
    user_id: str
    name: str
    email: str | None = None
    password: str | None = None


class UserManager:
    def get_one(self, user_id):
        if not user_id:
            raise Exception("User ID is required")
        
        account = db_manager.read(COLLECTIONS.USERS, UserQuery.user_id == user_id)
        return User(**account[0]) if account else None

    def get_all(self):
        users = db_manager.read(COLLECTIONS.USERS)
        return [User(**user) for user in users]

    def get_or_create(self, user_id, name, email, password):
        user = self.get_one(user_id)
        if user:
            return user
        user = db_manager.create(COLLECTIONS.USERS, User(user_id, name, email, password).__dict__)
        return User(**user)
