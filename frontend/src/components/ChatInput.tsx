import { useState } from 'react'

type ChatInputProps = {
  onSend: (message: string) => void
  disabled?: boolean
}

function ChatInput({
  onSend,
  disabled = false,
}: ChatInputProps) {
  const [input, setInput] = useState('')

  function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    const message = input.trim()

    if (!message || disabled) {
      return
    }

    onSend(message)
    setInput('')
  }

  return (
    <form
      className="chat-input"
      onSubmit={handleSubmit}
    >
      <input
        type="text"
        value={input}
        onChange={(event) =>
          setInput(event.target.value)
        }
        placeholder="Digite uma operação matemática..."
        disabled={disabled}
      />

      <button
        type="submit"
        disabled={disabled || !input.trim()}
      >
        Enviar
      </button>
    </form>
  )
}

export default ChatInput
