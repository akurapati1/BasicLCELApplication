"""Streamlit front-end for the LangServe translation API (run serve.py first)."""
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chain/invoke")


def translate(text: str, language: str) -> str:
    """Call the LangServe /invoke endpoint and return the translated text."""
    response = requests.post(API_URL, json={"input": {"language": language, "text": text}}, timeout=60)
    response.raise_for_status()
    return response.json()["output"]


st.title("LLM Application Using LCEL")
language = st.selectbox("Translate into", ["French", "Spanish", "German", "Hindi", "Telugu", "Japanese"])
input_text = st.text_input("Enter the text you want to translate")

if input_text:
    try:
        with st.spinner("Translating..."):
            st.write(translate(input_text, language))
    except requests.RequestException as exc:
        st.error(f"Could not reach the API at {API_URL}. Is serve.py running? ({exc})")
