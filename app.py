import streamlit as st
from gradio_client import Client
import base64
from PIL import Image
import io
import time
import requests

# Hide Streamlit's default header and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {margin-top: -3rem;}
    .css-1v3fvcr {text-align: left;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and subtitle
st.markdown("<h1 style='text-align: left; color: white;'>Hyperdyn</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left; color: white;'>Image Generation Tool</h2>", unsafe_allow_html=True)

# Add a description
st.markdown(
    """
    <p style='text-align: left; color: white;'>This application uses the ByteDance Hyper-FLUX-8Steps-LoRA model for generating images based on the provided text prompt. The API endpoint used for image generation is `/process_image`.</p>
    """,
    unsafe_allow_html=True,
)

# Define the client for the gradio API
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Streamlit form for input
with st.form(key='image_generation_form'):
    prompt = st.text_input("Enter prompt for image generation:")
    generate_button = st.form_submit_button("Generate Image")

    if generate_button:
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            # Display progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Simulate live logs
            live_logs = st.empty()
            for i in range(10):
                time.sleep(1)
                live_logs.text(f"Generating image... {i * 10}% complete")
                progress_bar.progress((i + 1) * 10)

            # Generate the image
            try:
                result = client.predict(
                    height=1024,
                    width=1024,
                    steps=8,
                    scales=3.5,
                    prompt=prompt,
                    seed=3413,
                    api_name="/process_image"
                )

                # Check if the result is an image
                if isinstance(result, dict) and 'image' in result:
                    img_data = base64.b64decode(result['image'])  # Decode base64-encoded image
                    image = Image.open(io.BytesIO(img_data))

                    st.image(image, caption='Generated Image', use_column_width=True)
                    
                    # Create a download link
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    st.markdown(f'<a href="data:file/png;base64,{img_str}" download="generated_image.png">Download Image</a>', unsafe_allow_html=True)
                    
                elif isinstance(result, bytes):
                    # Direct image bytes response
                    image = Image.open(io.BytesIO(result))
                    
                    st.image(image, caption='Generated Image', use_column_width=True)
                    
                    # Create a download link
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    st.markdown(f'<a href="data:file/png;base64,{img_str}" download="generated_image.png">Download Image</a>', unsafe_allow_html=True)

                else:
                    st.error("Unexpected response format from the API.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display API endpoint URL in the footer
st.markdown(
    '<footer style="text-align: left; color: white;">API Endpoint: /process_image</footer>',
    unsafe_allow_html=True
)
