import { askAssistant, bankPost } from './utils'
import { update_session } from './session'
import { TUser } from "./types"


export const handleMessage = async (sockt: any, m: any): Promise<void> => {
    if(!m.messages[0].message?.conversation) return
    if(m.messages[0].key.fromMe) return
    if(m.messages[0].broadcast) return
    if(m.messages[0].key.remoteJid === 'status@broadcast') return

    let question = m.messages[0].message?.conversation
    if(question.startsWith('/')) {
        if(question === '/help') {
            question = 'What kind of questions can you help me with? Help me understand how to use you. Give examples of all possible question i can ask'
        } else if(question === '/start') {
            question = 'Hie, who are and how can you be help me?'
        } else if(question === '/seed') {
            const context = await bankPost('/seed', _sender(m))
            update_session(_sender(m), context)
            question = "Hie, what kind of services are available for me to use based on my details?"
        } else {
            await sockt.sendMessage(m.messages[0].key.remoteJid!, { text: "Unknown command. Please try one of /help, /seed, /start" })
            return
        }
    }

    const response = await askAssistant(_sender(m), question)
    await sockt.sendMessage(m.messages[0].key.remoteJid!, { text: response })
}

const _sender = (message: any): TUser => ({
    user_id: message.messages[0].key.remoteJid,
    full_name: message.messages[0].pushName,
})
