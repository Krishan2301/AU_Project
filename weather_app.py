import streamlit as st
import requests

st.title("🌦 Weather API")

cities = ["Jaipur", "Dausa", "Udaipur", "Madhya Pradesh", "Delhi", "Paris", "Gujarat"]
city = st.selectbox("Choose a City", cities)

if city:
    api_key = "fc41686f199db2050f20bb9e6a8520c6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        st.write("*City:*", data["name"])
        st.write("*Temperature:*", data["main"]["temp"], "°C")
        st.write("*Weather:*", data["weather"][0]["description"].title())
    else:
        st.error("City not found.")