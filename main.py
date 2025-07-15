import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image

# Load Azure OpenAI credentials
load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

if not deployment_name:
    st.error("❌ Error: Deployment name not found. Check your .env file for AZURE_DEPLOYMENT_NAME.")
    st.stop()

# Page setup
st.set_page_config(page_title="AI Meme Judge", page_icon="😂")
st.title("😂 AI Meme Judge — Rate My Meme")
st.markdown("Upload a meme image or caption and let the AI roast, rate, and suggest a funnier version!")

# Meme judging logic
def judge_meme(caption):
    try:
        prompt = f"""You're a brutally honest and sarcastic AI meme judge. Rate this meme from 1 to 10, roast it, and suggest a funnier version.

Meme Caption: "{caption}"

Respond in this format:
Rating: x/10
Comment: <sarcastic or honest roast>
Suggestion: <funnier version>
"""
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": "You are a funny and brutally honest meme judge."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=150
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {e}"

# UI Inputs
option = st.radio("Choose meme type:", ["Text Caption", "Image with Caption"])

if option == "Text Caption":
    caption_input = st.text_input("Enter your meme caption:")
    if st.button("Judge my meme!"):
        if caption_input:
            with st.spinner("Roasting your meme..."):
                st.success(judge_meme(caption_input))
        else:
            st.warning("Please enter a meme caption.")

elif option == "Image with Caption":
    image_file = st.file_uploader("Upload your meme image (jpg/png)", type=["jpg", "jpeg", "png"])
    image_caption = st.text_input("Enter the caption for this meme (if any):")
    if st.button("Judge my meme image!") and (image_file or image_caption):
        with st.spinner("Judging your meme..."):
            if image_file:
                st.image(Image.open(image_file), caption="Uploaded Meme", use_column_width=True)
            caption = image_caption if image_caption else "Just an image meme with no caption."
            st.success(judge_meme(caption))
