import streamlit as st
import openai
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
from PIL import Image
import pytesseract
import os

# 🔐 OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# 🎨 Page Setup
st.set_page_config(page_title="AiSathi 🇳🇵", layout="centered")
st.title("🤖 AiSathi – One Box, All Power")
st.caption("Type your command below. Examples: `solve:`, `translate:`, `code:`, `voice:`")

# 🛡️ Ethical Filter
def is_safe(text):
    banned = ["hack", "kill", "drugs", "bomb", "illegal"]
    return not any(word in text.lower() for word in banned)

# 🤖 AI Response
def get_ai_reply(prompt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

# 🌐 Translation
def translate(text, target_lang="en"):
    source_lang = detect(text)
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

# 🧠 Main Input
user_input = st.text_area("Ask anything (with command):")

if st.button("Send"):
    if not is_safe(user_input):
        st.warning("❌ Unsafe or blocked content.")
    elif ":" not in user_input:
        st.warning("⚠️ Use a command like `solve:`, `translate:`, `code:`, etc.")
    else:
        command, content = user_input.split(":", 1)
        command = command.strip().lower()
        content = content.strip()
        lang = detect(content)

        if command == "solve":
            prompt = f"Help solve this homework:\n{translate(content)}"
            reply = get_ai_reply(prompt)
            final = translate(reply, target_lang=lang)
            st.write("📚", final)

        elif command == "translate":
            translated = translate(content, target_lang="en")
            st.write("🌐 Translated to English:", translated)

        elif command == "code":
            prompt = f"Write code for:\n{translate(content)}"
            reply = get_ai_reply(prompt)
            st.code(reply, language="python")

        elif command == "voice":
            reply = get_ai_reply(content)
            final = translate(reply, target_lang=lang)
            st.write("🔊", final)
            tts = gTTS(text=final, lang=lang)
            tts.save("voice.mp3")
            st.audio("voice.mp3")
            os.remove("voice.mp3")

        else:
            reply = get_ai_reply(content)
            final = translate(reply, target_lang=lang)
            st.write("🤖", final)
