from app.memory.conversation_memory import ConversationMemory


def test_add_and_get_messages():
    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Quanto é 5 mais 4?",
    )

    memory.add_message(
        "assistant",
        "O resultado é 9.",
    )

    assert memory.get_messages() == [
        {
            "role": "user",
            "content": "Quanto é 5 mais 4?",
        },
        {
            "role": "assistant",
            "content": "O resultado é 9.",
        },
    ]


def test_get_messages_returns_copy():
    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Teste",
    )

    messages = memory.get_messages()
    messages.clear()

    assert memory.get_messages() == [
        {
            "role": "user",
            "content": "Teste",
        }
    ]


def test_set_and_get_last_result():
    memory = ConversationMemory()

    memory.set_last_result(9.0)

    assert memory.get_last_result() == 9.0


def test_last_result_starts_as_none():
    memory = ConversationMemory()

    assert memory.get_last_result() is None


def test_clear_memory():
    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Quanto é 5 mais 4?",
    )

    memory.set_last_result(9.0)

    memory.clear()

    assert memory.get_messages() == []
    assert memory.get_last_result() is None