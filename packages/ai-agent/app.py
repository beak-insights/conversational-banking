import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

from .langc import BankAgent
from .user import UserManager, create_superuser
from .activity import ActivityManager

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR  = os.path.join(CURRENT_DIR, "static")
TEMPLATE_DIR  = os.path.join(CURRENT_DIR, "templates")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

sessions: dict[str, BankAgent] = {}

class UserQuery(BaseModel):
    user_id: str
    question: str

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    await create_superuser()
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )
    
@app.post("/login", response_class=HTMLResponse)
async def read_item(request: Request, username: str = Form(), password: str = Form()):
    if not (await UserManager().login(username, password)):   
        return templates.TemplateResponse(
            request=request, name="index.html", context={
                "message": "Incorrect username and password: Please try again"
            }
        )
    else:
        return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
async def read_item(request: Request):
    activities = await ActivityManager().get_all()
    acts = [
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 45,
            "created": "2024-05-25 18:06:43"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 60,
            "created": "2024-07-29 10:20:43"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 30,
            "created": "2024-01-06 20:45:08"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 35,
            "created": "2024-07-17 10:51:36"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 12,
            "created": "2024-09-22 04:06:07"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 46,
            "created": "2024-08-18 12:53:51"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 24,
            "created": "2024-08-23 00:22:41"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 12,
            "created": "2024-04-08 14:05:18"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 25,
            "created": "2024-04-12 16:30:01"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 32,
            "created": "2024-06-02 18:44:03"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 44,
            "created": "2024-10-03 11:04:05"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 24,
            "created": "2024-06-23 13:12:34"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 44,
            "created": "2024-01-09 01:20:11"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 26,
            "created": "2024-07-10 13:03:17"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 30,
            "created": "2024-02-29 06:06:12"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 53,
            "created": "2024-02-14 21:08:00"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 8,
            "created": "2024-03-16 14:31:33"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 42,
            "created": "2024-04-14 11:38:12"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 51,
            "created": "2024-06-05 10:08:49"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 17,
            "created": "2024-03-01 02:07:55"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 52,
            "created": "2024-02-28 17:25:33"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 11,
            "created": "2024-08-22 13:38:53"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 22,
            "created": "2024-01-29 19:38:56"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 44,
            "created": "2024-04-27 11:20:20"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 60,
            "created": "2024-10-08 12:41:48"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 44,
            "created": "2024-09-19 02:03:28"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 42,
            "created": "2024-04-27 08:32:20"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 18,
            "created": "2024-05-25 04:02:52"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 25,
            "created": "2024-06-17 07:29:46"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 37,
            "created": "2024-09-29 10:10:09"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 43,
            "created": "2024-05-07 00:00:41"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 27,
            "created": "2024-08-03 17:48:48"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 31,
            "created": "2024-03-03 00:19:01"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 49,
            "created": "2024-02-11 14:33:07"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 40,
            "created": "2024-06-10 14:36:50"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 29,
            "created": "2024-06-01 20:40:19"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 25,
            "created": "2024-06-17 05:31:10"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 16,
            "created": "2024-07-17 20:29:13"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 9,
            "created": "2024-01-03 08:41:33"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 21,
            "created": "2024-10-02 16:12:01"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 18,
            "created": "2024-09-10 21:50:52"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 49,
            "created": "2024-02-20 11:31:02"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 17,
            "created": "2024-04-16 01:34:12"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 21,
            "created": "2024-07-23 08:15:00"
        },
        {
            "user_id": "User3",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 10,
            "created": "2024-03-26 22:00:56"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 38,
            "created": "2024-01-19 07:47:15"
        },
        {
            "user_id": "User4",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 12,
            "created": "2024-08-30 10:48:08"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 38,
            "created": "2024-03-13 20:02:27"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 25,
            "created": "2024-06-27 17:54:04"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 51,
            "created": "2024-05-23 14:41:05"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 50,
            "created": "2024-04-12 21:21:42"
        },
        {
            "user_id": "User1",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 35,
            "created": "2024-03-18 14:04:38"
        },
        {
            "user_id": "User5",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 18,
            "created": "2024-02-13 03:57:00"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 5,
            "created": "2024-05-07 23:15:17"
        },
        {
            "user_id": "User2",
            "category": "ask",
            "activity": "aaprompt",
            "duration": 27,
            "created": "2024-08-02 02:44:45"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 24,
            "created": "2024-08-13 17:46:05"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 44,
            "created": "2024-10-06 21:10:02"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 49,
            "created": "2024-07-19 09:21:22"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 5,
            "created": "2024-07-25 15:25:26"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 35,
            "created": "2024-01-08 23:42:13"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 60,
            "created": "2024-04-28 02:29:20"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 38,
            "created": "2024-07-19 21:10:20"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 21,
            "created": "2024-01-19 01:31:26"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 16,
            "created": "2024-01-07 10:32:14"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 42,
            "created": "2024-10-08 13:17:31"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 19,
            "created": "2024-05-09 19:20:23"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 6,
            "created": "2024-08-22 07:03:10"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 13,
            "created": "2024-04-27 22:15:01"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 33,
            "created": "2024-03-22 11:56:21"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 10,
            "created": "2024-07-23 22:48:46"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 39,
            "created": "2024-10-04 07:51:50"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 25,
            "created": "2024-02-16 21:52:05"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 21,
            "created": "2024-05-10 16:12:14"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 28,
            "created": "2024-08-26 20:04:41"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 40,
            "created": "2024-07-16 10:09:21"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 58,
            "created": "2024-01-02 16:09:22"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 43,
            "created": "2024-01-06 23:49:08"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 14,
            "created": "2024-04-15 07:16:54"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 31,
            "created": "2024-07-05 11:04:28"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 10,
            "created": "2024-07-31 07:07:32"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 17,
            "created": "2024-09-02 04:14:47"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 38,
            "created": "2024-04-06 22:04:01"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 5,
            "created": "2024-09-07 07:19:27"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 5,
            "created": "2024-07-24 18:08:23"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 42,
            "created": "2024-01-05 11:36:26"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 11,
            "created": "2024-01-16 14:35:09"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 16,
            "created": "2024-02-15 10:07:05"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 46,
            "created": "2024-02-23 03:55:11"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 46,
            "created": "2024-04-18 09:39:11"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 20,
            "created": "2024-08-28 12:21:17"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 45,
            "created": "2024-06-14 12:56:57"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 16,
            "created": "2024-03-22 07:08:00"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 8,
            "created": "2024-03-07 00:59:43"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 7,
            "created": "2024-02-23 08:49:31"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 5,
            "created": "2024-02-22 03:43:29"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 45,
            "created": "2024-03-06 05:16:33"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 59,
            "created": "2024-07-06 23:27:51"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 41,
            "created": "2024-08-18 08:23:43"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 59,
            "created": "2024-10-13 19:43:36"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 50,
            "created": "2024-05-20 10:54:13"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 54,
            "created": "2024-01-09 08:22:13"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 6,
            "created": "2024-10-12 01:02:58"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 36,
            "created": "2024-09-05 01:31:36"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 14,
            "created": "2024-04-18 20:16:07"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 32,
            "created": "2024-04-03 17:30:46"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 45,
            "created": "2024-04-04 13:56:45"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 54,
            "created": "2024-08-27 21:46:19"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 31,
            "created": "2024-01-24 17:59:35"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 35,
            "created": "2024-04-21 06:50:50"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 33,
            "created": "2024-08-19 22:44:54"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 19,
            "created": "2024-05-26 00:31:28"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 22,
            "created": "2024-07-09 20:58:23"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 12,
            "created": "2024-06-11 13:58:14"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 38,
            "created": "2024-09-26 10:03:59"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 33,
            "created": "2024-09-17 19:11:19"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 39,
            "created": "2024-09-01 08:53:05"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 35,
            "created": "2024-03-06 15:16:51"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 55,
            "created": "2024-07-05 16:56:06"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 51,
            "created": "2024-04-09 07:12:21"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 14,
            "created": "2024-01-09 08:59:00"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 56,
            "created": "2024-05-16 06:57:00"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 8,
            "created": "2024-04-10 03:05:22"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 19,
            "created": "2024-03-26 10:47:35"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 34,
            "created": "2024-06-22 16:40:15"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 49,
            "created": "2024-09-27 18:41:36"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 46,
            "created": "2024-03-03 05:00:24"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 28,
            "created": "2024-07-12 20:27:55"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 42,
            "created": "2024-03-15 19:33:04"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 26,
            "created": "2024-09-08 03:17:25"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 11,
            "created": "2024-05-08 17:34:20"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 15,
            "created": "2024-07-09 23:49:59"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 28,
            "created": "2024-08-21 20:14:11"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 47,
            "created": "2024-07-12 15:27:33"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 27,
            "created": "2024-08-20 17:06:27"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 60,
            "created": "2024-03-10 20:51:27"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 37,
            "created": "2024-06-23 01:53:48"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 56,
            "created": "2024-01-01 22:45:26"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 15,
            "created": "2024-05-29 09:21:37"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 10,
            "created": "2024-05-19 05:43:06"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 30,
            "created": "2024-02-14 20:10:58"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 10,
            "created": "2024-09-28 15:07:42"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 52,
            "created": "2024-02-02 03:30:36"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 41,
            "created": "2024-04-24 21:55:13"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 57,
            "created": "2024-08-06 06:53:22"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 23,
            "created": "2024-02-23 23:39:22"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 10,
            "created": "2024-01-02 14:22:49"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 51,
            "created": "2024-07-12 21:49:07"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 14,
            "created": "2024-03-17 00:30:55"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 34,
            "created": "2024-06-08 16:31:31"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_balance",
            "duration": 25,
            "created": "2024-05-23 01:42:52"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 50,
            "created": "2024-03-29 06:31:23"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 45,
            "created": "2024-08-02 13:38:39"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 58,
            "created": "2024-04-08 07:27:23"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 45,
            "created": "2024-06-28 08:39:36"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_withdraw",
            "duration": 26,
            "created": "2024-06-25 00:00:55"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 19,
            "created": "2024-03-18 15:11:06"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 42,
            "created": "2024-06-04 10:53:09"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 27,
            "created": "2024-06-25 20:19:49"
        },
        {
            "user_id": "User1",
            "category": "tools",
            "activity": "lc_statement",
            "duration": 42,
            "created": "2024-05-11 03:17:55"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 50,
            "created": "2024-03-03 17:32:09"
        },
        {
            "user_id": "User4",
            "category": "tools",
            "activity": "lc_external_transfer",
            "duration": 8,
            "created": "2024-03-11 19:07:34"
        },
        {
            "user_id": "User2",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 54,
            "created": "2024-07-05 23:06:55"
        },
        {
            "user_id": "User5",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 52,
            "created": "2024-08-13 07:48:02"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_deposit",
            "duration": 17,
            "created": "2024-02-18 19:26:22"
        },
        {
            "user_id": "User3",
            "category": "tools",
            "activity": "lc_internal_transfer",
            "duration": 19,
            "created": "2024-03-17 18:44:48"
        }
    ]
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={
            "activities": [a.__dict__ for a in activities]
        }
    )


@app.post("/ask")
async def ask_assistant(query: UserQuery):
    if query.user_id not in sessions:
        logger.info(f"User does not exist in session:  contextualising ...")
        with_context = await BankAgent().contextualise(
            query.user_id
        )
        logger.info(f"Applying context ...")
        sessions[query.user_id] = with_context.init()
        logger.info(f"Context Applied ...")
    
    logger.info(f"Sending query to assistant ... from {sessions[query.user_id].user_id}")
    resp = await sessions[query.user_id].aprompt(query.question)
    logger.info(f"Received response from assistant")
    return {"content": resp}

add_routes(app, RunnableLambda(ask_assistant))

