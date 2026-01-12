'use client';
import { useState } from "react";
import ReactMarkdown from 'react-markdown';
import './chat.css'

const ChatsPage = ()  => {
    const [input, setInput] = useState("");
    const [currentChat, setCurrentChat] = useState<Array<{role: string, content: string}>>([]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const currentInput = input;
        setInput('');
        // Add user message to messages array
        const userMessage = { role: 'user', content: currentInput };
        const updatedMessagesWithUser = currentChat.concat(userMessage);
        setCurrentChat(updatedMessagesWithUser);
        
        try {
            const apiUrl = 'http://localhost:8000';
            console.log('Fetching from:', apiUrl);
            const res = await fetch(`${apiUrl}/chats`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: currentInput})
            });
            
            console.log('Response status:', res.status, res.statusText);
            
            if (!res.ok) {
                const errorText = await res.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
            }
            
            const data = await res.json();
            console.log("Full response: ", JSON.stringify(data, null, 2));

            // Extract LLM response content
            if (!data.messages || !Array.isArray(data.messages) || data.messages.length === 0) {
                const errorMessage = data.error || "No response from server";
                const aiMessage = { role: 'assistant', content: errorMessage };
                const updatedMessagesWithAI = updatedMessagesWithUser.concat(aiMessage);
                setCurrentChat(updatedMessagesWithAI);
                return;
            }
            
            const lastMessage = data.messages[data.messages.length - 1];
            const llmContent = lastMessage.content || "response has no content";

            // Add AI message to array
            const aiMessage = { role: 'assistant', content: llmContent };
            const updatedMessagesWithAI = updatedMessagesWithUser.concat(aiMessage);
            setCurrentChat(updatedMessagesWithAI);
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Failed to connect to server";
            const aiMessage = { role: 'assistant', content: `Error: ${errorMessage}` };
            const updatedMessagesWithAI = updatedMessagesWithUser.concat(aiMessage);
            setCurrentChat(updatedMessagesWithAI);
        }
    }

    return (
        <>
        {currentChat.map((msg, index) => (
            <div key={index} className={msg.role === 'user' ? 'chat chat-start' : 'chat chat-end'}>
                {msg.role === 'user' ? (
                <div className="chat-bubble chat-bubble-error">
                    {msg.content}
                </div>
                ) :
                (
                <div className="chat-bubble">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
                )}
            </div>
        ))}
        <div>
        <form onSubmit={handleSubmit}>
        <input 
        type="text"
        value={input}
        onChange={(e) => {
            setInput(e.target.value);
        }}
        placeholder="Type here"
        className="input" 
        />
        <div>
        <button type="submit">Send</button>
        </div>
        </form>
        </div>
        </>
    )
}

export default ChatsPage;
