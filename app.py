import streamlit as st
import requests
import json

# Replace with your actual RapidAPI key and endpoint
RAPIDAPI_KEY = "40f14362a4mshf4b871f3b27fa62p1b293djsn07cfceb23c62"
RAPIDAPI_ENDPOINT = "linkedin-data-api.p.rapidapi.com"

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyDdhSQC9v1iHjXSJ0aVMmhL6i-Irln1s7c"

# Define a function to scrape LinkedIn profile data
def scrape_linkedin_profile(profile_url):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "YOUR_RAPIDAPI_HOST"
    }

    url = f"{RAPIDAPI_ENDPOINT}?url={profile_url}"
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Define a function to generate a customized email using Gemini API
def generate_email(profile_data, message):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }

    data = {
        "prompt": f"""
            Write a professional email to {profile_data["firstName"]} {profile_data["lastName"]} 
            at {profile_data["email"]} based on their LinkedIn profile. 
            {message}
        """,
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return None

# Streamlit UI
st.title("LinkedIn Email Generator")

profile_url = st.text_input("Enter LinkedIn profile URL:")

message = st.text_area("Enter your message:")

if st.button("Generate Email"):
    profile_data = scrape_linkedin_profile(profile_url)

    if profile_data:
        email = generate_email(profile_data, message)
        if email:
            st.success(f"**Generated Email:**\n\n{email}")
        else:
            st.error("Error generating email.")
    else:
        st.error("Error scraping LinkedIn profile.")