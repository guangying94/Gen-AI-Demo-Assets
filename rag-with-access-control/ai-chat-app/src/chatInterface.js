import { AiChat, useAsBatchAdapter } from '@nlux/react';
import '@nlux/themes/nova.css';
import './LLMChatApp.css';
import { useState } from "react";

const LLMChatApp = ({userInfo}) => {
    const [chatHistory, setChatHistory] = useState([]);

    const myCustomAdapter = useAsBatchAdapter(
        async (prompts) => {
            const roles = userInfo.userRoles.filter(role => role !== 'authenticated' && role !== 'anonymous');

            let requestBody = {
                "history": chatHistory,
                "question": prompts,
                "roles": roles
            };

            const response = await fetch("/api/GetLLMResponse", {
                method: "POST",
                body: JSON.stringify(requestBody)
            });

            let reply = await response.text();

            let chat_entry = {
                "inputs": {
                    "question": prompts
                },
                "outputs": {
                    "answer": reply
                }
            }

            setChatHistory([...chatHistory, chat_entry]);

            return reply;
        }
    );

    return (
        <div className="chatContainer">
            <AiChat
                personaOptions={{
                    assistant: {
                        name: 'Document AI Bot',
                        avatar: 'https://robohash.org/cute',
                        tagline: 'Find information that answers your questions.'
                    },
                    user: {
                        name: userInfo.userDetails,
                        avatar: 'https://robohash.org/4B1.png?set=set3&size=150x150',
                    }
                }}
                displayOptions={{ colorScheme: 'dark' }}
                adapter={myCustomAdapter} />
        </div>
    );
}

export default LLMChatApp;