import React from 'react'

interface ChatBubble {
    content: string;
}

const ChatsPage = async ()  => {
    // need to have the user type in content here and then have it sent to llm

    // once I get the response from llm, display here
    const res = await fetch('http://127.0.0.1:8000/chats',
        {cache: 'no-store'}
        // caches in 10 second increment
        // {next: {revalidate: 10}}
    )

    const contentToLog = await res.json();
    // let allLogs: string; variable is declared but not used, declaration vs. initialiation in typescript
    // contentToLog.messages.forEach((keyValuePairs: Record<string, string>) => allLogs + ((keyValuePairs.toString())));
    
    let allLogs: string = '';
    // allLogs is an object, not an array
    contentToLog.messages.slice(1).forEach((msg: any) => {allLogs += msg.content + '\n'});
    
    // const content: string = String(contentToLog);
    return (
        <>
        <div className="chat chat-start">
        <div className="chat-bubble">
            {contentToLog.messages[0].content}
            <br />
            {allLogs};
        </div>
        
        </div>
        <div className="chat chat-end">
        </div>
        </>
    )
}

export default ChatsPage;