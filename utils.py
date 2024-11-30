from openai import OpenAI
import os
# from dotenv import load_dotenv
import base64
import streamlit as st
# load_dotenv()
# api_key = os.getenv("openai_api_key")

# client = OpenAI(api_key=api_key)



# Point to the local server
import streamlit as st
from openai import OpenAI
client = OpenAI(base_url="", api_key="lm-studio")

def expl(user,question):
  a=question+user
  completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
      # {"role": "system", "content": ""},
      {"role": "user", "content": a}
    ],
    temperature=0.7,
  )
  return completion


question = st.text_input("enter question")
user = st.text_input("enter text")
if st.button('submit'):
  completion = expl(user,question)
  st.write(completion.choices[0].message.content)
  print(completion.choices[0].message.content)
  
  # st.rerun()


# def get_answer(messages):
#     system_message = [{"role": "system", "content": "You are an helpful AI chatbot, that answers questions asked by User."}]
#     messages = system_message + messages
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return response.choices[0].message.content




def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)