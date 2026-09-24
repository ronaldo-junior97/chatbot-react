const API_URL = import.meta.env.VITE_API_URL

type ChatRequest = {
  message: string
  session_id?: string
}

type ChatResponse = {
  session_id: string
  response: string
}

export async function sendMessage(
  message: string,
  sessionId: string | null,
): Promise<ChatResponse> {
  const payload: ChatRequest = {
    message,
  }

  if (sessionId) {
    payload.session_id = sessionId
  }

  const response = await fetch(
    `${API_URL}/chat/message`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  )

  if (!response.ok) {
    throw new Error(
      'Não foi possível enviar a mensagem.',
    )
  }

  return response.json()
}

export async function deleteSession(
  sessionId: string,
): Promise<void> {
  const response = await fetch(
    `${API_URL}/chat/${sessionId}`,
    {
      method: 'DELETE',
    },
  )

  if (!response.ok) {
    throw new Error(
      'Não foi possível apagar a conversa.',
    )
  }
}