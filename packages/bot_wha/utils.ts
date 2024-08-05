import axios from 'axios';
import { get_session } from "./session"
import { TUser } from "./types"

const ASSISTANT_API = process.env.ASSISTANT_API
const BANK_API = process.env.BANK_API
console.log(ASSISTANT_API, BANK_API)


export const askAssistant = async (user_data: TUser, question: string) => {
    const data = await ask_context(user_data, question)
    try {
        const response = await axios.post(`${ASSISTANT_API}/ask`, data); 
        return response.data.content;
    } catch (error: any) {
        // console.error(error);
        return error.response.data || "An error occurred while trying to ask the assistant.";
    }
}

export const bankPost = async (url: string, data: any) => {
    try {
        const response = await axios.post(`${BANK_API}${url}`, data);
        return response.data.content;
    } catch (error: any) {
        // console.error(error);
        return error.response.data || "An error occurred while trying to ask the assistant.";
    }
}

const ask_context = async (user_data: TUser, question: string) => {
    user_data = get_session(user_data)
    return {...user_data, question }
}