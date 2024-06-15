import requests
import streamlit as st
import base64
import locale
from dotenv import load_dotenv
import os

# Set the locale to the user's default locale
locale.setlocale(locale.LC_ALL, '')

load_dotenv()
api_key = st.secrets["OPENAI_API_KEY"]

#base_api_url = "http://localhost:7071"

def get_open_ai_response(image, mime):
    
    with st.spinner(text="Analyzing the image..."):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        base64_image = base64.b64encode(image).decode('utf-8')

        prompt = """
            Extract the information related to the petition, title, description and information from the table of the people that have signed it.

            Return a response strictly in this JSON format and don't include any text before or after:

            {
            "title": "string (if not available, empty string)",
            "description: "string (if not available, empty string)",
            "signatures: [
            {
            "name": "string",
            "mobile" "number",
            "email": "email",
            "postcode: "string",
            "contact_by_email": "bool",
            "contact_by_phone": "bool"
            }
            ]
        """
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1200
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers, json=payload)

        json_response = response.json()['choices'][0]['message']['content']
        
        return json_response