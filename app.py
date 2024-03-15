from dotenv import load_dotenv

load_dotenv() ##load all the environment variable from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
import base64

# #Debug: Print loaded environment variables
# st.write("Loaded Environment Variables:")
# st.write(os.environ)
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    #Check if a file has been uploaded
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type, #Get the mime type of the uploaded file
                "data":bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def text_to_speech(text):
    tts=gTTS(text=text,lang='en')
    tts.save("output.mp3")
    with open("output.mp3", "rb") as audio_file:
        audio_data = audio_file.read()
        return base64.b64encode(audio_data).decode('utf-8')


##Initialize our streamlit app

st.set_page_config(page_title="MultiLanguageInvoice Extractor")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload an image as invoice
and you will have to answer any questions based on the uploaded invoice image.
If the text is in another language, translate it to English, as well.
"""

audio_file_path="output.mp3"
#If submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
    
    audio_data=text_to_speech(response)
    audio_html = f'<audio controls autoplay><source type="audio/mp3" src="data:audio/mp3;base64,{audio_data}"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)