import axios from 'axios';
import { get_session, update_session } from "./session"
import { TUser, TUserContext } from "./types"

const ASSISTANT_API = process.env.ASSISTANT_API
const BANK_API = process.env.BANK_API
console.log(ASSISTANT_API, BANK_API)


export const askAssistant = async (user_data: TUser, question: string) => {
    let data = await ask_context(user_data, question)
    if(data.context == null) {
        const ctx = await bankPost('/seed', user_data)
        await update_session(user_data, ctx)
        data = await ask_context(user_data, question)
    }
    
    try {
        const response = await axios.post(`${ASSISTANT_API}/ask`, data); 
        return response.data.content;
    } catch (error: any) {
        console.error(error);
        return error?.response?.data || "An error occurred while trying to ask the assistant.";
    }
}

export const bankPost = async (url: string, data: any) => {
    try {
        const response = await axios.post(`${BANK_API}${url}`, data);
        return response.data.content;
    } catch (error: any) {
        console.error(error);
        return error?.response?.data || "An error occurred while trying to ask the assistant.";
    }
}

const ask_context = async (user_data: TUser, question: string) => {
    const user_session = get_session(user_data)
    return {...user_session, question }
}

export const getSender = (message: any): TUser => ({
    user_id: message.messages[0].key.remoteJid,
    full_name: message.messages[0].pushName,
})