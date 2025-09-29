import streamlit as st
import openai
from langdetect import detect
from deep_translator import GoogleTranslator
from PIL import Image
import pytesseract
from gtts import gTTS
import os

# 🔐 OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual key

# 🎨 Branding
st.set_page_config(page_title="AiSathi 🇳🇵", layout="centered")
st.title("🤖 AiSathi™")
st.caption("Made in Nepal, Loved Worldwide 🌏")
st.write("Namaste Gopal! Your app is now fully powered 🎉")

# 🛡️ Ethical Filter
def is_safe(text):
    banned = ["hack", "kill", "drugs", "bomb", "illegal"]
    return not any(word in text.lower() for word in banned)

# 🤖 AI Response
def get_ai_reply(prompt, model="gpt-3.5-turbo"):
    return openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

# 🧩 Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat", "📚 Homework", "💻 Code", "📸 Photo Upload", "🔊 Voice", "🌐 Translate"
])

# 💬 Chat Tab
with tab1:
    mode = st.radio("Reply mode:", ["💬 Chat only", "🔊 Voice only", "💬 + 🔊 Both"])
    user_input = st.text_area("Ask AiSathi anything:")
    if st.button("Send", key="chat"):
        if is_safe(user_input):
            lang = detect(user_input)
            translated = GoogleTranslator(source='auto', target='en').translate(user_input)
            reply = get_ai_reply(translated)
            final = GoogleTranslator(source='en', target=lang).translate(reply)

            if mode in ["💬 Chat only", "💬 + 🔊 Both"]:
                st.write("🤖", final)

            if mode in ["🔊 Voice only", "💬 + 🔊 Both"]:
                tts = gTTS(text=final, lang=lang)
                tts.save("voice.mp3")
                audio_file = open("voice.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")
                os.remove("voice.mp3")
        else:
            st.warning("❌ Unsafe or blocked content.")

# 📚 Homework Tab
with tab2:
    hw_question = st.text_input("Enter your homework question:")
    if st.button("Solve", key="homework"):
        if is_safe(hw_question):
            lang = detect(hw_question)
            translated = GoogleTranslator(source='auto', target='en').translate(hw_question)
            prompt = f"Help solve this homework:\n{translated}"
            reply = get_ai_reply(prompt)
            final = GoogleTranslator(source='en', target=lang).translate(reply)
            st.write("📚", final)
        else:
            st.warning("❌ Unsafe question.")

# 💻 Code Tab
with tab3:
    code_task = st.text_input("Describe the code you need:")
    if st.button("Generate Code", key="code"):
        if is_safe(code_task):
            lang = detect(code_task)
            translated = GoogleTranslator(source='auto', target='en').translate(code_task)
            prompt = f"Write code for:\n{translated}"
            reply = get_ai_reply(prompt, model="gpt-4")
            st.code(reply, language="python")
        else:
            st.warning("❌ Unsafe code request.")

# 📸 Photo Upload Tab
with tab4:
    uploaded_file = st.file_uploader("📚 Upload homework photo", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        image = Image.open(uploaded_file)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path if needed
        extracted_text = pytesseract.image_to_string(image)
        st.write("📖 Extracted Text:", extracted_text)
        if st.button("Solve from photo"):
            prompt = f"Please solve this homework:\n{extracted_text}"
            reply = get_ai_reply(prompt)
            st.write("📚", reply)

# 🔊 Voice Tab
with tab5:
    voice_text = st.text_area("Enter text to speak:")
    if st.button("Generate Voice"):
        lang = detect(voice_text)
        tts = gTTS(voice_text, lang=lang)
        tts.save("voice.mp3")
        audio_file = open("voice.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        os.remove("voice.mp3")

# 🌐 Translate Tab
with tab6:
    text_to_translate = st.text_area("Enter text to translate:")
    target_lang = st.selectbox("Choose target language", ["en", "ne", "hi", "fr", "es", "zh-cn", "ja", "ko", "ar"])
    if st.button("Translate", key="translate"):
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)
        st.write("🌐 Translated Text:", translated)
