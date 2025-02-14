import streamlit as st
import openai
import http.client
import json

# Replace with your API keys
GEMINI_API_KEY = '40f14362a4mshf4b871f3b27fa62p1b293djsn07cfceb23c62'

def scrape_linkedin_profile(url):
    conn = http.client.HTTPSConnection(GEMINI_API_KEY)

    headers = {
        'x-rapidapi-key': GEMINI_API_KEY,
        'x-rapidapi-host': GEMINI_API_HOST
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
        try:
            profile_data = scrape_linkedin_profile(linkedin_url)
            email_text = generate_custom_email(profile_data)
            st.subheader("Generated Email")
            st.write(email_text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please enter a valid LinkedIn profile URL.")
