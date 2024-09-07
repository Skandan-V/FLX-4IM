import streamlit as st
import requests
import base64
import subprocess
import time
import json

# Start Ngrok tunnel
def start_ngrok():
    ngrok_process = subprocess.Popen(["ngrok", "http", "8501"])
    time.sleep(5)  # Wait for Ngrok to start
    response = requests.get("http://localhost:4040/api/tunnels")
    public_url = response.json()['tunnels'][0]['public_url']
    return public_url

# Fetch Ngrok public URL
try:
    public_url = start_ngrok()
except Exception as e:
    st.error(f"Failed to start Ngrok: {e}")
    public_url = "http://localhost:8501"

st.set_page_config(page_title="Hyperdyn - Image Generation Tool", page_icon=":camera:", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: white;'>Hyperdyn</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Image Generation Tool</h2>", unsafe_allow_html=True)

# Predefined resolutions
resolutions = {
    "1024x1024": "📏",
    "1280x720": "📐",
    "1920x1080": "📐",
    "2560x1440": "📏",
    "3840x2160": "📏"
}

# Resolution selection
resolution = st.selectbox(
    "Select resolution:",
    options=list(resolutions.keys()),
    format_func=lambda x: f"{resolutions[x]} {x}"
)

# Upload image file
uploaded_file = st.file_uploader("Choose an image file...", type=["png", "jpg", "jpeg"])

# Text prompt input
prompt = st.text_input("Enter a prompt for the image generation:")

if st.button("Generate Image"):
    if uploaded_file and prompt:
        st.markdown("<h3 style='color: white;'>Generating image...</h3>", unsafe_allow_html=True)
        st.spinner("Processing...")

        # Convert image file to base64
        image_data = uploaded_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Prepare payload for API request
        height, width = map(int, resolution.split('x'))
        payload = {
            "height": height,
            "width": width,
            "steps": 8,
            "scales": 3.5,
            "prompt": prompt,
            "seed": 3413,
            "image": encoded_image
        }

        try:
            response = requests.post(f"{public_url}/process_image", json=payload)
            response.raise_for_status()
            result = response.json()

            if "image" in result:
                st.image(result["image"], caption="Generated Image")
                st.download_button(
                    label="Download Image",
                    data=base64.b64decode(result["image"].split(",")[1]),
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("Unexpected response format from the API.")
                st.write(f"Raw response: {result}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.error("Please upload an image and enter a prompt.")

# Footer
st.markdown(f"<h6 style='text-align: center; color: white;'>API endpoint: {public_url}/process_image</h6>", unsafe_allow_html=True)
