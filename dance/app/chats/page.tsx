'use client';
import { useState } from "react";

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
        
        const res = await fetch('http://127.0.0.1:8000/chats', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: currentInput})
        });
        const data = await res.json();
        console.log("Full response: ", JSON.stringify(data, null, 2));

        // Extract LLM response content
        const lastMessage = data.messages[data.messages.length - 1];
        const llmContent = lastMessage.content || "response has no content";

        // Add AI message to array
        const aiMessage = { role: 'assistant', content: llmContent };
        const updatedMessagesWithAI = updatedMessagesWithUser.concat(aiMessage);
        setCurrentChat(updatedMessagesWithAI);
    }

    return (
        <>
        {currentChat.map((msg, index) => (
            <div key={index} className={msg.role === 'user' ? 'chat chat-end' : 'chat chat-start'}>
                <div className="chat-bubble">
                    {msg.content}
                </div>
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
