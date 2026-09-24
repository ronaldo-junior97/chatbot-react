type ChatMessageProps = {
  role: 'user' | 'assistant'
  content: string
}

function ChatMessage({
  role,
  content,
}: ChatMessageProps) {
  const isUser = role === 'user'

  return (
    <div
      className={`message ${
        isUser ? 'message-user' : 'message-assistant'
      }`}
    >
      <span className="message-author">
        {isUser ? 'Você' : 'Chatbot'}
      </span>

      <p>{content}</p>
    </div>
  )
}

export default ChatMessage