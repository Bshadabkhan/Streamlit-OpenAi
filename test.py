import streamlit as st
from openai import OpenAI
client = OpenAI(base_url="", api_key="lm-studio")

def expl(user,question):
  a=question+user
  completion = client.chat.completions.create(
    model="llm_gpt4all_falcon_7b_q4_gguf",
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

