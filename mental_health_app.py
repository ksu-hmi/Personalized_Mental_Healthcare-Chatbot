import openai
import pandas as pd
import speech_recognition as sr
import streamlit as st

# Set OpenAI API key
openai.api_key = "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"

# Load mental health dataset
mentalhealth = pd.read_csv("AI_Mental_Health.csv")

def generate_response(input_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_text}],
            temperature=0.7,
            max_tokens=100,
        )
        st.write("Chatbot Response:")
        st.write(response.choices[0].message["content"])
    except Exception as e:
        st.write(f"Error generating response: {e}")

def main():
    st.title("Personalized Mental HealthCare Chatbot App")
    st.text("By: Andrea Armstrong")

    input_type = st.radio("Select input type", ("Text", "Voice"))

    if input_type == "Text":
        user_input = st.text_input("Enter your message:")
        if st.button("Send"):
            generate_response(user_input)

    elif input_type == "Voice":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Adjusting for ambient noise. Speak after 3 seconds...")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            try:
                st.write("Listening...")
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio)
                st.write(f"You said: {query}")
                generate_response(query)
            except sr.UnknownValueError:
                st.write("Sorry, I couldn't understand the audio. Please try again.")
            except sr.RequestError as e:
                st.write(f"Could not request results; check your internet connection: {e}")

if __name__ == '__main__':
    main()

    # Suggest resources based on user query
def suggest_resources(query, dataset):
    relevant_rows = dataset[dataset['Symptoms'].str.contains(query, case=False, na=False)]
    if not relevant_rows.empty:
        st.write("Suggested Resources:")
        for _, row in relevant_rows.iterrows():
            st.write(f"- {row['Resource Name']}: {row['Details']}")
    else:
        st.write("No specific resources found for your query.")


        # Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_response(input_text):
    try:
        # Append user input to conversation history
        st.session_state.messages.append({"role": "user", "content": input_text})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=150,
        )
        
        # Append assistant's response to conversation history
        assistant_response = response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    except Exception as e:
        return f"Error generating response: {e}"

def generate_response(input_text):
    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message["content"]
    except openai.error.AuthenticationError:
        return "Authentication failed. Please check your API key."
    except openai.error.RateLimitError:
        return "Rate limit exceeded. Please try again later."
    except openai.error.APIConnectionError:
        return "Network error. Please check your internet connection."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
