export type TUser = {
    user_id: string
    full_name: string
}

export type TUserContext = {
    user_id: string
    full_name: string
    context: string
}

export type TSession = {
    [key: string]: TUserContext;
}