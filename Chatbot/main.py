import streamlit as st

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide"
)

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.title("AI Chatbot")
st.markdown("---")


def auto_save_current_chat():
    if st.session_state.get('messages') and len(st.session_state.messages) > 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        first_message = st.session_state.messages[0]['content'][:30] + "..." if len(
            st.session_state.messages[0]['content']) > 30 else st.session_state.messages[0]['content']
        auto_name = f"Sohbet {timestamp} - {first_message}"

        if 'saved_chats' not in st.session_state:
            st.session_state.saved_chats = {}

        memory_buffer = str(st.session_state.memory.buffer) if hasattr(st.session_state.memory, 'buffer') else ""
        st.session_state.saved_chats[auto_name] = {
            'messages': st.session_state.messages.copy(),
            'memory_buffer': memory_buffer,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'auto_saved': True
        }
        return auto_name
    return None


def save_chat(chat_name, messages, memory_buffer):
    if 'saved_chats' not in st.session_state:
        st.session_state.saved_chats = {}

    st.session_state.saved_chats[chat_name] = {
        'messages': messages,
        'memory_buffer': memory_buffer,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'auto_saved': False
    }


def load_chat(chat_name):
    if chat_name in st.session_state.saved_chats:
        chat_data = st.session_state.saved_chats[chat_name]
        st.session_state.messages = chat_data['messages']
        st.session_state.memory = ConversationBufferMemory(return_messages=True)
        for msg in chat_data['messages']:
            if msg['role'] == 'user':
                st.session_state.memory.chat_memory.add_user_message(msg['content'])
            else:
                st.session_state.memory.chat_memory.add_ai_message(msg['content'])


def delete_chat(chat_name):
    if chat_name in st.session_state.saved_chats:
        del st.session_state.saved_chats[chat_name]


# Sidebar ayarları
with st.sidebar:
    st.header("Ayarlar")

    st.subheader("Sohbet Yönetimi")

    if 'saved_chats' not in st.session_state:
        st.session_state.saved_chats = {}

    if st.session_state.saved_chats:
        st.write("Kayıtlı Sohbetler:")
        for chat_name, chat_data in st.session_state.saved_chats.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                icon = "🔄" if chat_data.get('auto_saved', False) else "📂"
                if st.button(f"{icon} {chat_name}", key=f"load_{chat_name}"):
                    load_chat(chat_name)
                    st.success(f"{chat_name} yüklendi!")
                    st.rerun()
            with col2:
                st.caption(chat_data['timestamp'][:16])
            with col3:
                if st.button("❌", key=f"del_{chat_name}"):
                    delete_chat(chat_name)
                    st.success(f"{chat_name} silindi!")
                    st.rerun()
    else:
        st.info("Henüz kayıtlı sohbet yok")

    if st.button("Yeni Sohbet", type="primary"):
        saved_name = auto_save_current_chat()
        if saved_name:
            st.success("Mevcut sohbet otomatik kaydedildi")

        st.session_state.messages = []
        st.session_state.memory = ConversationBufferMemory(return_messages=True)
        st.rerun()

    chat_name = st.text_input("Sohbet adı")
    if st.button("Kaydet") and chat_name:
        if st.session_state.get('messages'):
            memory_buffer = str(st.session_state.memory.buffer) if hasattr(st.session_state.memory, 'buffer') else ""
            save_chat(chat_name, st.session_state.messages, memory_buffer)
            st.success(f"'{chat_name}' kaydedildi!")
            st.rerun()
        else:
            st.warning("Kaydedilecek mesaj yok!")

    st.markdown("---")

    model_list = [
        "gpt-3.5-turbo",
        "gpt-4o-mini",
        "gpt-4",
        "gpt-4-turbo-preview"
    ]

    model = st.selectbox("Model", model_list, index=1)

    st.subheader("Asistan Rolü")

    roles = {
        "Genel": "Sen yardımcı bir asistansın.",
        "Programcı": "Sen yazılım geliştirme uzmanısın.",
        "Öğretmen": "Sen eğitim ve öğretim uzmanısın.",
        "Analist": "Sen veri analizi ve araştırma uzmanısın.",
        "Yazar": "Sen yaratıcı yazım uzmanısın."
    }

    selected_role = st.selectbox("Rol seç", list(roles.keys()))

    manual_prompt = st.text_area("Özel talimat", height=80)

# Ana alan
col1, col2 = st.columns([4, 1])

with col2:
    st.subheader("Durum")
    st.write(f"Model: {model}")
    st.write(f"Rol: {selected_role}")

    msg_count = len(st.session_state.get('messages', []))
    st.write(f"Mesaj sayısı: {msg_count}")

    chat_count = len(st.session_state.get('saved_chats', {}))
    st.write(f"Kayıtlı sohbetler: {chat_count}")

with col1:
    # Session başlatma
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(return_messages=True)

    # API key kontrol
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("OPENAI_API_KEY bulunamadı. .env dosyasını kontrol edin.")
        st.stop()

    try:
        # LLM kurulumu
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=1500,
            streaming=True
        )

        # Prompt hazırlama
        system_text = manual_prompt if manual_prompt else roles[selected_role]

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_text),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        # Chain kurulumu
        chain = ConversationChain(
            llm=llm,
            memory=st.session_state.memory,
            prompt=prompt,
            verbose=False
        )

    except Exception as e:
        st.error(f"Bağlantı hatası: {str(e)}")
        st.stop()

    # Mesaj geçmişi
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "time" in msg:
                st.caption(msg["time"])

    # Kullanıcı input
    if user_input := st.chat_input("Mesajınızı yazın"):
        # Kullanıcı mesajı
        current_time = datetime.now().strftime("%H:%M")
        user_msg = {
            "role": "user",
            "content": user_input,
            "time": current_time
        }
        st.session_state.messages.append(user_msg)

        with st.chat_message("user"):
            st.write(user_input)
            st.caption(current_time)

        # AI yanıt
        with st.chat_message("assistant"):
            try:
                response = chain.predict(input=user_input)
                st.write(response)

                ai_time = datetime.now().strftime("%H:%M")
                ai_msg = {
                    "role": "assistant",
                    "content": response,
                    "time": ai_time
                }
                st.session_state.messages.append(ai_msg)

                st.caption(ai_time)

            except Exception as e:
                st.error(f"Hata: {str(e)}")

st.markdown("---")
st.caption("LangChain ve Streamlit tabanlı chatbot uygulaması")

with st.expander("Kullanım Talimatları"):
    st.markdown("""
    ### Nasıl Kullanılır?

    1. **Model Seçimi:** Sidebar'dan GPT modelini seçin
    2. **Asistan Rolü:** Hangi tür yardım istediğinizi seçin
    3. **Özel Talimat:** İsterseniz kendi özel talimatınızı yazın
    4. **Sohbet:** Alt kısımdan mesajınızı yazın ve Enter'a basın

    ### Sohbet Yönetimi

    - **Yeni Sohbet:** "Yeni Sohbet" ile yeni konuşma başlatın
    - **Otomatik Kayıt:** Mevcut sohbetiniz otomatik olarak kaydedilir
    - **Manuel Kayıt:** İstediğiniz isimle sohbeti kaydedin
    - **Sohbet Yükle:** Kayıtlı sohbetlerden birine tıklayarak devam edin
    - **Sohbet Sil:** X butonuyla gereksiz sohbetleri silin

    ### Özellikler

    - Otomatik hafıza ve konuşma geçmişi
    - Çoklu sohbet yönetimi
    - 4 farklı GPT modeli
    - 5 hazır asistan rolü
    - Gerçek zamanlı streaming yanıtlar
    - Zaman damgası

    ### Kurulum

    ```bash
    pip install streamlit langchain langchain-openai python-dotenv
    ```

    **.env dosyası:**
    ```
    OPENAI_API_KEY=your-api-key-here
    ```

    **Çalıştırma:**
    ```bash
    streamlit run chatbot.py
    ```
    """)