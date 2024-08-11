// Description: This file contains the session management for the bot.

import { TSession, TUserContext, TUser } from "./types"


const users: TSession = {}


export const init_session = (user_data: TUser): TUserContext => {
    const user_id: string = user_data["user_id"]
    users[user_id] = {
        ...user_data,
        "context": null
    }
    return users[user_id]
}

export const get_session = (user_data: TUser): TUserContext => {
    const user_id: string = user_data["user_id"]
    if (!users[user_id]) {
        return init_session(user_data)
    }
    return users[user_id] as TUserContext
}

export const update_session = (user_data: TUser, context: string): TUserContext => {
    const user_id: string = user_data["user_id"]
    users[user_id] = {
        ...users[user_id],
        ...user_data,
        context
    }
    return users[user_id]
}
