import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json

# Load the pre-trained model
with open("BANGALORE_HOME_PRICE.pkl", "rb") as f:
    model = pickle.load(f)

# Load the columns.json file
with open("columns.json", "r") as f:
    data_columns = json.load(f)["data_columns"]
    locations = data_columns[3:]  # Assuming locations start from index 3

# Function to predict price
def predict_price(location, sqft, bath, bhk):
    try:
        # Find the index of the location
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1  # If location is not found

    # Create a numpy array with zeros
    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1  # Set the location index to 1

    # Predict the price
    return model.predict([x])[0]

# Streamlit app
st.title("Bangalore House Price Predictor 🏠")
st.write("""
### Enter the details to predict the house price
""")

# Input fields
location = st.selectbox("Location", locations)
sqft = st.number_input("Square Feet", min_value=300, max_value=10000, value=1000)
bath = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
bhk = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=2)

# Predict button
if st.button("Predict Price"):
    price = predict_price(location, sqft, bath, bhk)
    st.success(f"### Predicted Price: ₹{price*100000:,.2f}")

# Creator Section
st.markdown("""
---
<style>
    .creator-box {
        background-color: grey;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .creator-name {
        font-size: 22px;
        font-weight: bold;
        color: black;
    }
    .creator-links a {
        color: black;
        font-weight: bold;
        text-decoration: none;
        margin: 0 10px;
    }
    .creator-links a:hover {
        text-decoration: underline;
    }
    .creator-year{
        color: black; 
        font-weight: bold; 
    }
</style>

<div class="creator-box">
    <p class="creator-name">👨‍💻 Created by: Aniket Ghosh</p>
    <p class="creator-year">2nd Year CSE Student</p>
    <p class="creator-links">
        <a href="https://www.linkedin.com/in/aniket-ghosh-3942b6242/" target="_blank">LinkedIn</a> |
        <a href="https://github.com/KETTO8" target="_blank">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)