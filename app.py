import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "431afd17-aae3-4cc2-ac6d-bedcad04deaa"
FLOW_ID = "aee5ffd9-4433-4490-bff0-3d01ef7e049b"
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]    
ENDPOINT = st.secrets["END_POINT"]

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    st.title("IBOT GPT")
    message = st.text_area("הודעה", placeholder="מה תרצה לדעת ?")

    if st.button("תשלח"):
        if not message.strip():
            st.error("לא התקבלה הודעה, תכתוב משהו...")
            return
        try:
            with st.spinner("השאלה בבדיקה..."):
                response = run_flow(message)
            # Extract the text from the response
            text_response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(text_response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
