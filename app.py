import streamlit as st
import requests
import time
import random
from PIL import Image
from io import BytesIO

# Define the function to generate the image using the provided API
def generate_image(prompt, resolution):
    # Set the API URL
    api_url = "http://your-api-endpoint.com/process_image"  # Replace with your actual API URL
    
    # Define payload with image generation parameters
    payload = {
        'prompt': prompt,
        'resolution': resolution
    }
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        # Check if the response contains image path
        response_json = response.json()
        if 'image_path' in response_json:
            image_path = response_json['image_path']
            return image_path
        else:
            st.error("Unexpected response format from the API.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
    except requests.exceptions.JSONDecodeError:
        st.error("Failed to decode JSON response.")

# Streamlit app layout
st.set_page_config(page_title="Hyperdyn - Image Generation Tool", layout="centered")

st.title("Hyperdyn - Image Generation Tool")

# Define available resolutions with icons
resolutions = {
    "512x512": "512x512",
    "1024x1024": "1024x1024",
    "2048x2048": "2048x2048"
}

# Input prompt and resolution selection
prompt = st.text_input("Enter your prompt:")
selected_resolution = st.selectbox("Select resolution:", list(resolutions.keys()))

# Add a button to generate the image
if st.button("Generate"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            # Generate the image
            image_path = generate_image(prompt, resolutions[selected_resolution])
            
            if image_path:
                # Display the image preview
                image_url = f"http://localhost:8501{image_path}"  # Adjust URL as needed
                st.image(image_url, caption="Generated Image", use_column_width=True)
                
                # Provide a download button
                st.download_button(
                    label="Download Image",
                    data=image_url,
                    file_name="generated_image.png",
                    mime="image/png"
                )
