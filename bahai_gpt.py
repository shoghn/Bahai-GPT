import base64
import os
from google import genai
from google.genai import types
import streamlit as st

#Gemini API client configuration
client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

MODEL = "gemini-2.0-flash"
#chat= client.chats.create(model=MODEL)

generate_content_config = types.GenerateContentConfig(
        temperature=0,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Answer questions from a Baha'i perspective, 
                                 as in always reference the Baha'i Faith explicitly in every single answer 
                                 to every single question. Do not be shy about voluntarily giving Baha'i quotes 
                                 as reference when answering questions, even if they are not perfectly related 
                                 to the topic. Try to source information and provide direct quotes from 
                                 bahai.org, https://www.bahai.org/library/, and https://www.bahai.org/library/authoritative-texts/. 
                                 If you're not able to find the information on these sites then find the information on 
                                 other sites on Google. Explicitly reference the name of the website (not the link) where you get information 
                                 from in each answer (especially for quotes)."""),
        ],
    )


st.title("Baha'i-GPT")

image="https://media.bahai.org/icons/icon-512x512.png?w=1200&h=630&q=70&fit=fillmax&fill=blur&fm=pjpg"

if "chat" not in st.session_state:
    st.session_state.chat=client.chats.create(model=MODEL)

if "history" not in st.session_state:
    st.session_state.history=[]
    first_messsage="Allah'U'Abha, weclome to Baha'i-GPT. How can I help you today?"
    st.session_state.history.append({"role":"assistant","content":first_messsage})
for message in st.session_state.history:
    if message["role"]=="assistant":
        av=image
    else:
        av="🪞"
    with st.chat_message(message["role"],avatar=av):
        st.markdown(message["content"])#maybe use .markdown() instead

if prompt:=st.chat_input("Type your question here"):
    #user
    with st.chat_message("user",avatar="🪞"):
        st.markdown(prompt)#maybe use .markdown() instead
    st.session_state.history.append({"role":"user","content":prompt})#maybe use .append() instead of +=
    #B-GPT
    with st.chat_message(name="assistant",avatar=image):
        message_holder=st.empty()
        full_response=""
        response = st.session_state.chat.send_message_stream(prompt,config=generate_content_config)
        for chunk in response:
            #print(chunk.text, end="",flush=True)
            flush=True
            full_response+=chunk.text
            message_holder.markdown(full_response)#maybe use .markdown() instead
    st.session_state.history.append({"role":"assistant","content":full_response})#maybe use .append() instead of +=
