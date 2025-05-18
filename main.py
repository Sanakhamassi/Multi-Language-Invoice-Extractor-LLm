from dotenv import load_dotenv 
import streamlit as st 
import os # to asign the env variable
from PIL import Image 
import google.generativeai as genai
load_dotenv() ## load all teh env variables feom .env

genai.configure(api_key=os.getenv('google_api_key')) 
#Function to load Gemini pro vision (we will work with images)
model=genai.GenerativeModel('gemini-1.5-flash') 

def get_geimini_response(input,image,prompt): 
    response=model.generate_content([input,image[0],prompt]) 
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None: 
        #read the file into bytes 
        bytes_data=uploaded_file.getvalue() 
        image_parts = [{

        "mime_type": uploaded_file.type, 
        "data": bytes_data }

        ]
        return image_parts 
    else: 
        raise FileNotFoundError("No file uploaded")



# streamlit setup 
st.set_page_config(page_title="Multi language Invoice Extracter",page_icon='📜') 
st.header("Multilanguage Invoice Extractor") 
input=st.text_input("Input prompt : ",key="input") 
uploaded_file=st.file_uploader("Choose an image of the invoice ...",type=['jpg','jpeg','png']) 
image=''
if uploaded_file is not None: 
    image=Image.open(uploaded_file) 
    st.image(image,caption="Uploaded image",use_container_width=True) 

submit=st.button("tell me about the invoice") 

input_prompt="""
You're an expert in understanding invoices. We will upload an image as invoice
and you will have to answer any question based on the uploaded invoice image.
"""
if submit: 
    image_data=input_image_details(uploaded_file) 
    response=get_geimini_response(input_prompt,image_data,input) 
    st.subheader("The response is ")
    st.write(response)