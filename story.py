import streamlit as st
import cohere

# Initialize the Cohere API client
API_KEY = "clvRh2trNT5sCW1AcXTNrFtqdjIIMUfIxkwHUIh0"  # Replace with your actual Cohere API key
co = cohere.Client(API_KEY)

# Function for generating a story with Cohere based on genre, character name, and description
def generate_story(genre, character_name, character_description):
    try:
        # Use Cohere to generate a story based on the selected genre, character name, and description
        prompt = f"Write a {genre} story of approximately 100 words featuring a character named {character_name}. {character_description}"

        response = co.generate(
            model="command-xlarge-nightly",  # You can use other models if needed
            prompt=prompt,
            max_tokens=200,  # Max tokens for a story of 100 words (approx. 2 tokens/word)
            temperature=0.7,  # Set a temperature for creativity
        )
        
        generated_text = response.generations[0].text.strip()
        return generated_text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI setup
st.set_page_config(page_title="Story Generator", page_icon="📖")

# Application Title
st.title("📖 Story Generator")
st.write("Generate a creative story based on the genre, character name, and description you provide!")

# Genre selection dropdown
genre = st.selectbox("Select a genre for your story", ["Love", "Adventure", "Mystery", "Fantasy", "Sci-Fi", "Horror"])

# Character name input field
character_name = st.text_input("Enter the character's name")

# Character description input field
character_description = st.text_area("Enter a description of the character", height=100)

# Button to generate the story
if st.button("Generate Story"):
    if genre.strip() and character_name.strip() and character_description.strip():
        with st.spinner("Generating story..."):
            generated_story = generate_story(genre, character_name, character_description)

            if not generated_story.startswith("Error"):
                st.write("### Generated Story:")
                st.write(generated_story)
            else:
                st.error(generated_story)
    else:
        st.error("Please select a genre, enter a character's name, and provide a character description.")
