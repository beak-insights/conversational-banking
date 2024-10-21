from datetime import datetime
from pydantic.dataclasses import dataclass
from timeit import default_timer as timer
import functools
from tinydb import Query

from .db import COLLECTIONS, db_manager

ActivityQuery = Query()


class Category:
    ASK = "ask"
    TOOL = "tool"


@dataclass
class Activity:
    user_id: str
    category: str
    activity: str
    duration: int
    messagein: str | None = None
    messageout: str | dict | None = None
    params: dict | None = None
    created: str | None = None


class ActivityManager:
    async def get_all(self):
        activities = await db_manager.read(COLLECTIONS.ACTIVITIES)
        return [Activity(**act) for act in activities]

    async def create(self, activity: Activity) -> Activity:
        data = activity.__dict__
        data["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        activity = await db_manager.create(COLLECTIONS.ACTIVITIES, data)
        return Activity(**activity)


def asking_activity(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        # Extract the query from args
        query = args[0] if args else kwargs.get('query', None)
        
        # Start the timer
        start = timer()
        
        # Execute the original function
        response = await func(self, *args, **kwargs)
        
        # Calculate the time taken
        taken = timer() - start
        
        # Access user_id and save required data
        act = Activity(**{
            "user_id": self.user_id,
            "category": Category.ASK,
            "activity": func.__name__,
            "duration": taken,
            "params": None,
            "messagein": query, 
            "messageout": response
        })
        await ActivityManager().create(act)
        
        # Return the response
        return response
    return wrapper


def tool_activity(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Capture all args and kwargs as a dictionary
        func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        params = {**dict(zip(func_args, args)), **kwargs}

        # Start the timer
        start = timer()

        # Execute the original function
        response = await func(*args, **kwargs)

        # Calculate the time taken
        taken = timer() - start

        # Access user_id and save required data
        act = Activity(**{
            "user_id": params.get("user_id"),
            "category": Category.TOOL,
            "activity": func.__name__,
            "duration": taken,
            "params": params,
            "messagein": None, 
            "messageout": response
        })
        await ActivityManager().create(act)
    
        # Return the original response
        return response

    return wrapper
