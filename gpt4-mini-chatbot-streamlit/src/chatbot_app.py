# Import necessary dependencies
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Load environment variables and set up OpenAI client
load_dotenv()
API_KEY = os.getenv("openai_api_key")
client = OpenAI(api_key=API_KEY)
MODEL_NAME = "gpt-4o-mini"

def get_chatbot_response(messages):
    """
    Get a response from the chatbot using OpenAI API
    """

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
        )
        
        return stream
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    st.title("GPT-4 Powered Support Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask anything in your mind . . ."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display chatbot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for chunk in get_chatbot_response(st.session_state.messages):
                if chunk is not None and chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
















