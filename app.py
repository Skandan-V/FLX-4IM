import streamlit as st
from gradio_client import Client
from concurrent.futures import ThreadPoolExecutor
import base64
from io import BytesIO
from PIL import Image
import socket
import os

# Set page config to hide header and logo
st.set_page_config(page_title="Hyperdyn Image Generation Tool", layout="centered")

# Disable the Streamlit header and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize Gradio Client
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Cache the result to avoid recalculating the same image generation
@st.cache_data(show_spinner=False)
def generate_image(prompt: str, height: int = 1024, width: int = 1024, steps: int = 8, scales: float = 3.5, seed: int = 3413):
    result = client.predict(height=height, width=width, steps=steps, scales=scales, prompt=prompt, seed=seed, api_name="/process_image")
    return result

# Function to run in parallel for faster generation
def generate_parallel(prompt):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(generate_image, prompt)
        return future.result()

# UI Design
st.title("Hyperdyn")
st.subheader("Image Generation Tool")
st.markdown("<style>body {background-color: black;}</style>", unsafe_allow_html=True)

# Input form for image generation
prompt = st.text_input("Enter the prompt for image generation", "Hello!!")

if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        result = generate_parallel(prompt)
        st.success("Image generated successfully!")

        # Display the image
        image = Image.open(BytesIO(base64.b64decode(result)))
        st.image(image, caption="Generated Image", use_column_width=True)

        # Download button for the image
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{img_str}" download="generated_image.png">Download Image</a>'
        st.markdown(href, unsafe_allow_html=True)

# Live log simulation (prints every second)
if st.button("Start Live Logs"):
    import time
    log_placeholder = st.empty()
    for i in range 10):  # Simulate live logs for 10 seconds
        log_placeholder.text(f"Log {i+1}: Processing request...")
        time.sleep(1)

# Function to auto-generate API URL based on the server's environment
def get_base_url():
    # Attempt to get base URL based on environment variables
    if "PORT" in os.environ:
        port = os.environ["PORT"]
    else:
        port = 8501  # Default Streamlit port

    # Get the machine's IP address (adjust this depending on your deployment)
    ip_address = socket.gethostbyname(socket.gethostname())

    # Construct the URL (adjust the protocol based on your environment)
    base_url = f"http://{ip_address}:{port}/api"
    
    return base_url

# Automatically generate API endpoint at the footer
st.write("---")
api_url = get_base_url()
st.markdown(
    f'<p style="text-align:center;">API Endpoint: <a href="{api_url}">{api_url}</a></p>',
    unsafe_allow_html=True,
)
