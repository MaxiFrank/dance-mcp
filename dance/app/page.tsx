import Link from 'next/link'
// import Chat from './components/ChatBubble/Chat'

// python fastapi and this /chats path use different ports
export default function Home() {
  // Link is client site navigation
  return (
   <main>
    <Link href="/chats">Dance Chat</Link>
    {/* <Chat /> */}
  </main>  
  )
}