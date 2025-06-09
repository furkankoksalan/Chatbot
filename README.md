# AI Chatbot

```
#=================================================================
# Streamlit ve LangChain kullanarak geliştirilmiş AI chatbot
#=================================================================

# Hakkında
#---------
Bu proje, OpenAI'nin GPT modellerini kullanarak geliştirilmiş
basit ve kullanışlı bir chatbot uygulamasıdır. Streamlit web 
arayüzü ve LangChain framework'ü ile oluşturulmuştur.

Temel amacı, kullanıcıların farklı GPT modelleri ile etkileşim
kurabilmelerini sağlamak ve sohbet geçmişlerini yönetebilmelerini
mümkün kılmaktır.

# Ana Özellikler
#---------------
• Modern web arayüzü (Streamlit)
• Çoklu sohbet yönetimi
• Otomatik hafıza sistemi
• Farklı asistan rolleri
• Streaming yanıtlar
• Sohbet kaydetme/yükleme

# Özellikler
#-----------
✓ Çoklu GPT model desteği (GPT-3.5, GPT-4, GPT-4o-mini)
✓ Sohbet geçmişi ve hafıza yönetimi  
✓ Otomatik sohbet kaydetme
✓ 5 farklı asistan rolü
✓ Gerçek zamanlı streaming yanıtlar
✓ Özel prompt desteği

# Kurulum
#---------
git clone <repo-url>
cd ai-chatbot

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Konfigürasyon
#--------------
# .env dosyası oluştur
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Çalıştırma
#-----------
streamlit run chatbot.py

# Kullanım
#---------
1. Tarayıcıda http://localhost:8501 adresini ziyaret et
2. Sidebar'dan model ve asistan rolünü seç  
3. Sohbete başla
4. "Yeni Sohbet" ile yeni konuşma başlat
5. Sohbetleri otomatik veya manuel kaydet

# Proje Yapısı
#--------------
ai-chatbot/
├── chatbot.py          # Ana uygulama
├── requirements.txt    # Python bağımlılıkları
├── .env               # API anahtarı (oluşturulacak)
└── README.md          # Bu dosya

# Gereksinimler
#--------------
Python >= 3.8
OpenAI API Key

# Bağımlılıklar
#--------------
streamlit
langchain
langchain-openai
python-dotenv

# API Anahtarı
#--------------
# OpenAI API anahtarını al:
# 1. https://platform.openai.com adresine git
# 2. API Keys bölümünden yeni anahtar oluştur
# 3. .env dosyasına ekle

# Asistan Rolleri
#----------------
Genel      → Genel amaçlı yardımcı
Programcı  → Yazılım geliştirme uzmanı
Öğretmen   → Eğitim ve öğretim uzmanı
Analist    → Veri analizi uzmanı
Yazar      → Yaratıcı yazım uzmanı

# Sohbet Yönetimi
#----------------
• Otomatik Kayıt → Yeni sohbet açarken mevcut sohbet kaydedilir
• Manuel Kayıt  → İstediğin isimle sohbet kaydet
• Sohbet Yükle  → Kayıtlı sohbetlere geri dön
• Sohbet Sil    → Gereksiz sohbetleri temizle

# Teknik Detaylar
#----------------
Framework    : Streamlit
LLM Library  : LangChain
Memory Type  : ConversationBufferMemory
Temperature  : 0.7
Max Tokens   : 1500
Streaming    : Aktif

# Sorun Giderme
#--------------
# Cache temizle
streamlit cache clear

# Bağımlılıkları güncelle
pip install --upgrade -r requirements.txt

# Port değiştir
streamlit run chatbot.py --server.port 8502

```
