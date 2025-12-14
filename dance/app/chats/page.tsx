'use client';
import { useState } from "react";

const ChatsPage = ()  => {
    const [input, setInput] = useState("");
    const [currentChat, setCurrentChat] = useState([]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const res = await fetch('http://127.0.0.1:8000/chats', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: input})
        });
        const data = await res.json();

    // Extract LLM response content
    const lastMessage = data.messages[data.messages.length - 1];
    const llmContent = lastMessage.content || JSON.stringify(data);
    setCurrentChat(llmContent);
    setInput('');}

    return (
        <>
        <div className="chat chat-start">
        <div className="chat-bubble">
            {currentChat};
        </div>
        
        </div>
        {/* <div className="chat chat-end">
        </div> */}
        <div>
        <form onSubmit={handleSubmit}>
        <input 
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
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
