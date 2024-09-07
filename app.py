import streamlit as st
from gradio_client import Client
import base64
import io
from PIL import Image
import time

# Initialize Gradio client
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Function to convert image to base64
def image_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Function to generate image
def generate_image(prompt, resolution):
    with st.spinner('Generating image...'):
        result = client.predict(
            height=resolution[1],
            width=resolution[0],
            steps=8,
            scales=3.5,
            prompt=prompt,
            seed=3413,
            api_name="/process_image"
        )
        return result

# Streamlit UI
st.set_page_config(page_title="Image Generation Tool", layout="wide")
st.title("Hyperdyn - Image Generation Tool")

# Resolution options
resolutions = {
    "1024x1024": (1024, 1024),
    "512x512": (512, 512),
    "256x256": (256, 256)
}

# User input
st.sidebar.header("Settings")
prompt = st.sidebar.text_area("Enter prompt", "Astronaut riding a horse")
resolution = st.sidebar.selectbox("Select Resolution", options=list(resolutions.keys()))
resolution = resolutions[resolution]

if st.sidebar.button("Generate"):
    try:
        image_base64 = generate_image(prompt, resolution)
        st.image(f"data:image/png;base64,{image_base64}", caption="Generated Image", use_column_width=True)
        st.download_button(
            label="Download Image",
            data=base64.b64decode(image_base64),
            file_name="generated_image.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Live logs
st.sidebar.subheader("Live Logs")
log_container = st.sidebar.empty()

for i in range(10):
    log_container.text(f"Fetching logs... ({i+1}/10)")
    time.sleep(1)

log_container.text("Logs updated.")
