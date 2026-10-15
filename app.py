import streamlit as st
from google import genai
from google.genai import types

# === НАСТРОЙКИ СТРАНИЦЫ ===
st.set_page_config(page_title="ESIL PARK | Премиум Резиденция", page_icon="🏛️", layout="wide")

# === ВСТАВЬ СВОЙ КЛЮЧ ===
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

# === ПРЕМИАЛЬНЫЙ ДИЗАЙН (CSS) ===
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0B132B;
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .sub-header {
        font-family: 'Georgia', serif;
        color: #C5A059;
        font-size: 1.5rem;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 40px;
        font-style: italic;
    }
    .info-box {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 4px solid #C5A059;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .info-box:hover { transform: translateY(-5px); }
    .info-box h3 { color: #0B132B; font-size: 1.2rem; margin-bottom: 10px; }
    .info-box p { color: #555555; font-size: 1rem; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# === ГЛАВНЫЙ ЭКРАН ===
st.markdown('<div class="main-header">ESIL PARK</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Искусство жить на высоте. Левый берег Астаны.</div>', unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop", use_container_width=True)

st.write("")
st.write("")

# === ИНФОРМАЦИОННЫЕ КАРТОЧКИ ===
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="info-box"><h3>📍 Локация</h3><p>Есильский район, 5 минут от EXPO</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="info-box"><h3>📐 Архитектура</h3><p>Потолки 3.2м, панорамные окна</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="info-box"><h3>🌳 Инфраструктура</h3><p>Закрытый двор без машин, фитнес</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="info-box"><h3>🔑 Сдача объекта</h3><p>Ключи в IV квартале 2026 года</p></div>', unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# === БЛОК ИИ-МЕНЕДЖЕРА ===
st.subheader("💬 Персональный ИИ-Брокер")
st.write("Наш искусственный интеллект ответит на любые вопросы о ценах, планировках и условиях ипотеки.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Спросите про условия рассрочки или цены...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Брокер подбирает информацию..."):
        try:
            system_prompt = """Ты — элитный, супер-вежливый VIP-брокер отдела продаж строящегося ЖК 'Esil Park' в Астане.
            Отвечай на том языке, на котором пишет клиент (казахский или русский). Общайся уважительно, на 'Вы'.
            Твоя цель — презентовать ЖК так, чтобы клиент захотел купить квартиру, и в конце обязательно взять его номер телефона для приглашения в офис.
            
            Твоя база знаний о ЖК 'Esil Park':
            - Статус: Бизнес-класс+.
            - Особенности: Панорамные окна (Германия), система 'Умный дом' в каждой квартире, Face ID на входе, подземный паркинг.
            - Цены (фиксированные):
              * 1-комнатные (от 45 кв.м) — от 21 500 000 тг.
              * 2-комнатные (от 70 кв.м) — от 32 000 000 тг.
              * 3-комнатные (от 105 кв.м) — от 48 500 000 тг.
            - Способы покупки:
              * 100% оплата (скидка 5%).
              * Ипотека через Отбасы банк, Halyk, BCC (первоначалка от 20%).
              * Беспроцентная рассрочка от застройщика на 24 месяца (первоначалка 30%).
            
            Сценарий общения:
            1. Поблагодари за интерес к нашему премиальному ЖК.
            2. Четко и красиво ответь на вопрос клиента.
            3. Если клиент спрашивает цену, расскажи про планировки и задай встречный вопрос: 'Рассматриваете покупку для себя или как инвестицию?'
            4. Когда клиент получил ответ, напиши: 'Я могу забронировать за Вами эту цену. Оставьте, пожалуйста, Ваш номер телефона, и я организую для Вас VIP-презентацию за чашечкой кофе в нашем офисе продаж.'
            """

            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                )
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = "Приносим извинения, сейчас линия перегружена. Пожалуйста, оставьте ваш номер телефона, и мы перезвоним."

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
