
from telegram import User
from assistant.langc import BankAgent
from banking.seeder import get_user_context

users = {}


async def update_context(user: User, extra_context: str) -> None:
    user_id = str(user.id)
    users[user_id]["agent"].contextualise(user_id, user.full_name, extra_context).init(),
    users[user_id]["has_context"] = True
    return users[user_id]


async def get_session(user: User, has_context=False) -> None:
    user_id = str(user.id)
    if not user_id in users:
        users[user_id] = {
            "user_id": user_id,
            "username": user.username,
            "fullname": user.full_name,
            "has_context": False,
            "agent": BankAgent().contextualise(user_id, user.full_name, "").init(),
        }
    if has_context and not users[user_id]["has_context"]:
        context = get_user_context(user_id)
        await update_context(user, context)
    return users[user_id]
