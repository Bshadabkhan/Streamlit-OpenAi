# import streamlit as st
# import os
# from utils import expl, text_to_speech, autoplay_audio, speech_to_text
# from audio_recorder_streamlit import audio_recorder
# from streamlit_float import *

# # Float feature initialization
# float_init()

# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "Hi! How may I assist you today?"}
#         ]
#     # if "audio_initialized" not in st.session_state:
#     #     st.session_state.audio_initialized = False

# initialize_session_state()

# st.title("OpenAI SPEECH BOT 🤖")

# # Create footer container for the microphone
# footer_container = st.container()
# with footer_container:
#     audio_bytes = audio_recorder()


# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# if audio_bytes:
#     # Write the audio bytes to a file
#     with st.spinner("Transcribing..."):
#         webm_file_path = "temp_audio.mp3"
#         with open(webm_file_path, "wb") as f:
#             f.write(audio_bytes)

#         transcript = speech_to_text(webm_file_path)
#         if transcript:
#             st.session_state.messages.append({"role": "user", "content": transcript})
#             with st.chat_message("user"):
#                 st.write(transcript)
#             os.remove(webm_file_path)

# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking🤔..."):
#             final_response = expl(st.session_state.messages)
#         with st.spinner("Generating audio response..."):    
#             audio_file = text_to_speech(final_response)
#             autoplay_audio(audio_file)
#         st.write(final_response)
#         st.session_state.messages.append({"role": "assistant", "content": final_response})
#         os.remove(audio_file)

# # Float the footer container and provide CSS to target it with
# footer_container.float("bottom: 0rem;")
import openai
from flask import Flask, request, jsonify

openai.api_key="lm-studio"
openai.api_type="http://sreeai:1234/v1"

model = "llm_gpt4all_falcon_7b_q4_gguf"

messages = []

app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, How may i help you. "

def chatfun(request_text):
    

# Initialize messages history (optional: you can store conversation context if needed)
messages = []

# Flask app initialization
app = Flask(__name__)

# Simple route to handle the root URL ("/")
@app.route('/')
def home():
    return "Welcome to the OpenAI Chat Server! Use /chat to send a message."

# Chat function to handle user requests
def chatfun(request_text):
    # Append the user input to the conversation history
    messages.append({'role': 'user', 'content': request_text})
    
    # Call OpenAI API to get the model's response
    try:
        response = openai.Completion.create(
            model=model,
            prompt=request_text,  # Directly use the user's request as the prompt
            max_tokens=150,       # Set max_tokens to allow longer responses
            temperature=0.7,      # Adjust temperature for more natural responses
            top_p=0.95,           # Use top_p to adjust the diversity of responses
            n=1,
            echo=True,
            stream=False          # Stream option can be set to True for streaming responses
        )
        
        # Extract the model's response from the API response
        model_response = response.choices[0].text.strip()
        messages.append({'role': 'assistant', 'content': model_response})

        return model_response

    except Exception as e:
        return str(e)


# Route to handle user input and chat responses
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user request from the JSON payload
        user_request = request.json.get("message", "")
        
        if not user_request:
            return jsonify({"error": "No message provided"}), 400
        
        # Get the model's response using the chat function
        model_response = chatfun(user_request)
        
        return jsonify({"response": model_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
