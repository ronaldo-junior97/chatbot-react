import { useEffect, useRef, useState } from 'react'

import './App.css'
import ChatInput from './components/ChatInput'
import ChatMessage from './components/ChatMessage'
import {
  deleteSession,
  sendMessage,
} from './services/chatApi'

type Message = {
  id: number
  role: 'user' | 'assistant'
  content: string
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    })
  }, [messages, isLoading])

  async function handleSend(message: string) {
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: message,
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ])

    setIsLoading(true)

    try {
      const data = await sendMessage(
        message,
        sessionId,
      )

      setSessionId(data.session_id)

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ])
    } catch {
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content:
          'Não foi possível obter uma resposta. Tente novamente.',
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        errorMessage,
      ])
    } finally {
      setIsLoading(false)
    }
  }

  async function handleClearConversation() {
    if (isLoading) {
      return
    }

    if (sessionId) {
      try {
        await deleteSession(sessionId)
      } catch {
        return
      }
    }

    setMessages([])
    setSessionId(null)
  }

  return (
    <main className="chat-page">
      <section className="chat-container">
        <header className="chat-header">
          <div>
            <h1>Math Chatbot</h1>
            <p>
              Soma, subtração, multiplicação e divisão
            </p>
          </div>

          <button
            type="button"
            className="clear-button"
            disabled={
              messages.length === 0 || isLoading
            }
            onClick={handleClearConversation}
          >
            Limpar conversa
          </button>
        </header>

        <div className="messages">
          {messages.length === 0 ? (
            <div className="empty-state">
              <h2>Como posso ajudar?</h2>

              <p>
                Digite uma operação de soma, subtração,
                multiplicação ou divisão.
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <ChatMessage
                key={message.id}
                role={message.role}
                content={message.content}
              />
            ))
          )}

          {isLoading && (
            <ChatMessage
              role="assistant"
              content="Pensando..."
            />
          )}

          <div ref={messagesEndRef} />
        </div>

        <ChatInput
          onSend={handleSend}
          disabled={isLoading}
        />
      </section>
    </main>
  )
}

export default App