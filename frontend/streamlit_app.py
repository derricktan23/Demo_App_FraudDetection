import streamlit as st
import requests
import numpy as np

# FastAPI endpoint URL
FASTAPI_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Credit Card Fraud Detection Demo",
    page_icon="💳",
    layout="centered",
)

st.title("💳 Credit Card Fraud Detection Demo")

st.markdown("""
This demo app uses a machine learning model to predict if a credit card transaction is fraudulent.
Input the transaction details below and click 'Predict' to get a result.
""")

st.markdown("---")

# Input fields for the simplified features
st.subheader("Transaction Details")

amt = st.number_input(
    label="Transaction Amount (amt)",
    min_value=0.0,
    value=100.0,
    help="The amount of the transaction."
)

age = st.number_input(
    label="Customer Age (age)",
    min_value=0.0,
    value=35.0,
    help="The age of the cardholder."
)

distance_km = st.number_input(
    label="Distance from Home (distance_km)",
    min_value=0.0,
    value=5.0,
    help="The distance (in km) of the transaction from the cardholder's home."
)

# Predict button
if st.button("Predict"):
    # Create the payload from user inputs
    payload = {
        "amt": amt,
        "age": age,
        "distance_km": distance_km
    }

    try:
        # Make a POST request to the FastAPI endpoint
        response = requests.post(FASTAPI_URL, json=payload)
        
        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")

            if prediction == "fraudulent":
                st.error("🚨 This transaction is predicted as **FRAUDULENT**.")
            elif prediction == "not fraudulent":
                st.success("✅ This transaction is predicted as **NOT FRAUDULENT**.")
            else:
                st.warning("Could not interpret the prediction result.")
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the FastAPI server. Please ensure it's running. Error: {e}")

st.markdown("---")
st.markdown("### How to run the demo")
st.markdown("""
1.  **Start the FastAPI backend:** Open a terminal, navigate to your project folder, and run:
    ```bash
    uvicorn your_fastapi_app_name:app --reload
    ```
    (Replace `your_fastapi_app_name` with the actual filename of your FastAPI code, e.g., `main` if your file is `main.py`).

2.  **Start the Streamlit frontend:** Open a **new** terminal, navigate to the same project folder, and run:
    ```bash
    streamlit run streamlit_app.py
    ```
""")