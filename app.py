import streamlit as st
from google import genai
from google.genai import types

# === НАСТРОЙКИ СТРАНИЦЫ ===
st.set_page_config(page_title="SVOYDOM | Новостройки Астаны", page_icon="🏢", layout="wide")

# === ПОДКЛЮЧЕНИЕ КЛЮЧА ИЗ SECRETS ===
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

# === ДИЗАЙН КАТАЛОГА И ИСПРАВЛЕНИЕ ЦВЕТА ТЕКСТА (CSS) ===
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    .main-header { font-family: 'Helvetica Neue', sans-serif; color: #1E293B; font-weight: 800; font-size: 3rem; text-align: center; margin-bottom: 5px; }
    .sub-header { color: #64748B; font-size: 1.2rem; text-align: center; margin-bottom: 40px; }
    .property-card { background: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; height: 100%; }
    .property-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
    .price-tag { color: #2563EB; font-weight: bold; font-size: 1.3rem; margin: 10px 0; }
    .badge { background: #E2E8F0; color: #475569; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; }
    
    /* Принудительно делаем текст сообщений темным для читаемости */
    [data-testid="stChatMessageContent"] {
        color: #1E293B !important;
    }
    [data-testid="stChatMessage"] {
        color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

# === ШАПКА ПОРТАЛА ===
st.markdown('<div class="main-header">SVOYDOM.KZ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Надежные новостройки Астаны. Найдите квартиру своей мечты.</div>', unsafe_allow_html=True)

# === ВИТРИНА ЖИЛЫХ КОМПЛЕКСОВ ===
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="property-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=800", use_container_width=True)
    st.markdown('<h3>ЖК «Esil Park»</h3>', unsafe_allow_html=True)
    st.markdown('<span class="badge">Бизнес-класс</span> <span class="badge">Левый берег</span>', unsafe_allow_html=True)
    st.markdown('<div class="price-tag">от 21.5 млн ₸</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:gray; font-size:0.9rem;">Есильский р-н, 5 мин от EXPO. Панорамные окна, умный дом.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="property-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1460317442991-0ec209397118?q=80&w=800", use_container_width=True)
    st.markdown('<h3>ЖК «Turan Residence»</h3>', unsafe_allow_html=True)
    st.markdown('<span class="badge">Комфорт+</span> <span class="badge">Р-н Нура</span>', unsafe_allow_html=True)
    st.markdown('<div class="price-tag">от 18.2 млн ₸</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:gray; font-size:0.9rem;">Семейный формат, закрытый двор, рядом новые школы.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="property-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?q=80&w=800", use_container_width=True)
    st.markdown('<h3>ЖК «Nomad City»</h3>', unsafe_allow_html=True)
    st.markdown('<span class="badge">Комфорт</span> <span class="badge">Правый берег</span>', unsafe_allow_html=True)
    st.markdown('<div class="price-tag">от 14.5 млн ₸</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:gray; font-size:0.9rem;">Алматинский р-н. Идеально для первой квартиры и инвестиций.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# === УМНЫЙ ПОИСКОВИК (ИИ-БРОКЕР) ===
st.subheader("🤖 Умный подбор недвижимости")
st.info("Напишите ваш бюджет, желаемый район или класс жилья, и наш ИИ моментально подберет лучшие варианты из каталога!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Например: У меня есть 20 млн тенге, хочу двушку на левом берегу...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Анализирую базу новостроек..."):
        try:
            system_prompt = """Ты — старший эксперт по недвижимости компании 'SVOYDOM' в Астане.
            Твоя задача — анализировать запросы клиентов (бюджет, район, пожелания) и рекомендовать подходящие ЖК из нашей базы.
            Отвечай на языке клиента. Будь профессиональным, дружелюбным и лаконичным.
            
            Твоя база новостроек:
            1. ЖК 'Esil Park': Бизнес-класс, Левый берег (Есильский р-н, у EXPO). Цены: 1-комн от 21.5 млн, 2-комн от 32 млн, 3-комн от 48.5 млн. Плюсы: панорамные окна, премиум-отделка.
            2. ЖК 'Turan Residence': Комфорт+, Левый берег (р-н Нура). Цены: 1-комн от 18.2 млн, 2-комн от 26 млн, 3-комн от 35 млн. Плюсы: семейный ЖК, рядом школы, закрытый безопасный двор.
            3. ЖК 'Nomad City': Комфорт-класс, Правый берег (Алматинский р-н). Цены: 1-комн от 14.5 млн, 2-комн от 21 млн. Плюсы: доступная цена, отличный вариант для инвестиций и сдачи в аренду.
            
            Условия по всем ЖК: Ипотека Отбасы банк, Halyk, рассрочка от застройщика.
            
            Твой алгоритм ответа:
            1. Проанализируй запрос и предложи 1 или 2 наиболее подходящих ЖК из базы, объяснив почему они подходят.
            2. Назови стартовую цену для подходящей планировки.
            3. В конце обязательно задай вовлекающий вопрос (например: 'Хотите расскажу подробнее про условия рассрочки на этот ЖК?' или 'Оставить за вами эту цену для фиксации?').
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
            bot_reply = f"Техническая ошибка: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
