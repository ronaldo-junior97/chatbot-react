import sys
from pathlib import Path

import streamlit as st


project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.orchestrators.chat_orchestrator import ChatOrchestrator


if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = ChatOrchestrator()


st.title("AI Math Chatbot")

st.caption(
    "Operações disponíveis: adição, subtração, "
    "multiplicação e divisão."
)


for message in st.session_state.orchestrator.memory.get_messages():
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.button("🗑 Limpar conversa"):
    st.session_state.orchestrator.memory.clear()
    st.rerun()


user_message = st.chat_input(
    "Digite uma operação matemática"
)

if user_message:
    st.session_state.orchestrator.process(
        user_message
    )

    st.rerun()