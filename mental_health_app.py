import openai
import pandas as pd
import speech_recognition as sr
import streamlit as st

# Set OpenAI API key
openai.api_key = "API-Key"

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
