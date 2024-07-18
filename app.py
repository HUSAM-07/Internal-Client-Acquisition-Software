import streamlit as st
import openai
import http.client
import json

# Replace with your API keys
RAPIDAPI_KEY = '40f14362a4mshf4b871f3b27fa62p1b293djsn07cfceb23c62'
RAPIDAPI_HOST = 'linkedin-data-api.p.rapidapi.com'
OPENAI_API_KEY = 'your_openai_api_key'

openai.api_key = OPENAI_API_KEY

def scrape_linkedin_profile(url):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    # URL encode the LinkedIn profile URL
    profile_url_encoded = url.replace("/", "%2F").replace(":", "%3A")
    endpoint = f"/get-profile-data-by-url?url={profile_url_encoded}"

    conn.request("GET", endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))

def generate_custom_email(profile_data):
    prompt = f"Generate a customized email based on the following LinkedIn profile data: {profile_data}"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=200
    )
    
    email_text = response.choices[0].text.strip()
    return email_text

st.title("LinkedIn Profile Scraper and Email Generator")
st.write("Enter a LinkedIn profile URL to generate a customized email.")

linkedin_url = st.text_input("LinkedIn Profile URL")

if st.button("Generate Email"):
    if linkedin_url:
        profile_data = scrape_linkedin_profile(linkedin_url)
        email_text = generate_custom_email(profile_data)
        st.subheader("Generated Email")
        st.write(email_text)
    else:
        st.write("Please enter a valid LinkedIn profile URL.")
