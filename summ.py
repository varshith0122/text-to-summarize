import streamlit as st
from gtts import gTTS
import coh
import os

# Initialize Cohere API
API_KEY = "rujUGkqF0GNqEoaU4ifFy2i7oUlUKT4mAgaoJaG4"  # Replace with your Cohere API key
co = cohere.Client(API_KEY)

# Function for text summarization (optional step before TTS)
def summarize_text(input_text, model="summarize-xlarge", length="medium"):
    """
    Summarizes the input text using the Cohere API.
    """
    try:
        response = co.summarize(
            text=input_text,
            model=model,
            length=length
        )
        return response.summary
    except cohere.CohereError as e:
        return f"An error occurred with Cohere: {e}"

# Streamlit App UI
st.title("Text-to-Speech App with Cohere Integration")
st.subheader("Enter your text below, summarize it with Cohere (optional), and convert it to speech!")

# Input Text
input_text = st.text_area("Enter the text to convert to speech", height=200)

# Cohere Summarization
if st.button("Summarize Text with Cohere"):
    if input_text.strip():
        summary = summarize_text(input_text)
        st.success("Summary generated:")
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")

# Text-to-Speech Conversion
if st.button("Convert Text to Speech"):
    if input_text.strip():
        # Generate speech using gTTS
        try:
            tts = gTTS(text=input_text, lang="en")
            tts.save("output.mp3")
            st.audio("output.mp3", format="audio/mp3")
            st.success("Speech generated successfully!")
        except Exception as e:
            st.error(f"An error occurred during speech synthesis: {e}")
    else:
        st.warning("Please enter some text to convert to speech.")

# Footer
st.markdown("Developed with ❤️ using Streamlit, Cohere, and gTTS.")
