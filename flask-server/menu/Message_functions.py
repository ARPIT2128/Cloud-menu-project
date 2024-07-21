"""
This module implements the common texting and emails functionality
provideds the ability to send different kinds of messages in different formats.

Packages:
    - pip install twilio pywhatkit
"""

from twilio.rest import Client
import pywhatkit
from googlesearch import search

from email.message import EmailMessage
import ssl,smtplib

import os
from dotenv import load_dotenv

import google.generativeai as genai



# accessing the related env variables.
load_dotenv("menu/Secret.env")


# flask
def send_sms(input_text,phone):
    """
    This function is used to send an SMS using the Twilio API.
    -Parameters:
        - input_text (str): The text to be sent in the SMS.
    -Returns:
        - No return value.
    """
    # Your Twilio account SID and Auth Token
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    # Send an SMS
    message = client.messages.create(
        body=input_text,
        from_='+18285190691',
        to='+91'+str(phone)
    )

    print(f"Message sent with SID: {message.sid}")


# flask
def send_whatsapp(mobile,message):
    """
    This function is used to send whatsapp msg using the Twilio API.
    or pywhatkit message.
    """
    pywhatkit.sendwhatmsg_instantly(str(mobile),message,10,tab_close=True)

# flask
def search_google(query='ML ops courses'):
    """
    This function is used to search for a query on Google.
    -Parameters:
        - query (str): The query to be searched on Google.
    -Returns:
        - No return value.
    """
    for j in search(query, num_results=5,advanced=True):
        print(f"""
        {j.title}
        {j.url}
        {j.description}
        """)


# flask
def send_email(email_receiver,sub,body):

    email_sender='arpitsharma2128@gmail.com'
    email_password = os.getenv('EMAIL_PASSWORD_KEY')
    # default email address to send the msg
    email_receiver = 'deadshort811@gmail.com'

    sub = "Test python mail code"
    body  = """This is a mail send through python!!!"""

    em = EmailMessage() # email instance
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject']=sub
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())



# Configure the API key
gemini_key = os.getenv('GEMINI_KEY')

genai.configure(api_key=gemini_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def chat_with_model(prompt):
    # Start a chat session
    chat_session = model.start_chat(history=[])

    # Send the prompt to the model and get the response
    response = chat_session.send_message(prompt)
    return response.text

