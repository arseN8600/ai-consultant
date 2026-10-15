import streamlit as st
from google import genai

# Вставь свой ключ
GEMINI_API_KEY = 'AQ.Ab8RN6KO9VJ5TuhcTDoPB8ewz2AY-U4NAhizbwhlj7TSjYoopw'
client = genai.Client(api_key=GEMINI_API_KEY)

# Настройка внешнего вида сайта
st.set_page_config(page_title="ИИ-Консультант", page_icon="🤖")
st.title("🤖 Умный помощник")
st.write("Задайте мне любой вопрос, и я постараюсь помочь!")

# Инициализация истории чата (чтобы бот запоминал сообщения)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Вывод истории сообщений на экран
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле для ввода текста пользователем
user_input = st.chat_input("Напишите ваше сообщение...")

if user_input:
    # Показываем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Отправляем запрос в нейросеть и показываем анимацию загрузки
    with st.spinner("Печатаю ответ..."):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=user_input
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = "Извините, произошла ошибка соединения."

    # Показываем ответ бота
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})