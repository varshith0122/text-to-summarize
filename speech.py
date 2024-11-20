import streamlit as st
from gtts import gTTS
import cohere

# Initialize the Cohere client with your API key
API_KEY = 'plefNO4jx33CV3WSBhndABbnlvAQ2SjumrCELAMx'
co = cohere.Client(API_KEY)

# Streamlit interface
st.title("Text to Speech with Cohere")
st.write("Enter text below to generate speech using TTS and optionally summarize using Cohere.")

# Text input field
text_input = st.text_area("Enter your text:", height=200)

# Optional: Enable summarization with Cohere
summarize = st.checkbox("Summarize text with Cohere before converting to speech")

# Summarization settings (if enabled)
if summarize:
    length = st.selectbox("Select summary length:", options=["short", "medium", "long"])
    format_type = st.selectbox("Select summary format:", options=["paragraph", "bullet_points"])
    extractiveness = st.selectbox("Select extractiveness level:", options=["low", "medium", "high"])
    temperature = st.slider("Adjust creativity (temperature):", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

# Generate speech button
if st.button("Convert to Speech"):
    if text_input.strip():
        try:
            # Ensure the text is at least 250 characters long
            if summarize and len(text_input) < 250:
                st.error("Text must be at least 250 characters long to use summarization.")
            else:
                # Summarize text if the option is enabled
                if summarize:
                    response = co.summarize(
                        text=text_input,
                        length=length,
                        format=format_type,
                        extractiveness=extractiveness,
                        temperature=temperature,
                    )
                    text_to_speak = response.summary
                    st.subheader("Summary:")
                    st.write(text_to_speak)
                else:
                    text_to_speak = text_input

                # Convert text to speech using gTTS
                tts = gTTS(text_to_speak, lang='en')
                tts.save("output.mp3")

                # Audio playback in Streamlit
                st.audio("output.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter valid text to convert to speech.")
