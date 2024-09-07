import streamlit as st
from gradio_client import Client
from PIL import Image
import requests
from io import BytesIO

# Initialize Gradio Client
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Define function to generate image
def generate_image(height, width, steps, scales, prompt, seed):
    try:
        # Call the model with the provided parameters
        result = client.predict(
            height=height,
            width=width,
            steps=steps,
            scales=scales,
            prompt=prompt,
            seed=seed,
            api_name="/process_image"
        )
        # Extract image path from result
        image_path = result.get('filepath', '')
        return image_path
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app layout
st.set_page_config(page_title="Hyperdyn - Image Generation Tool", layout="centered")

st.title("Hyperdyn - Image Generation Tool")

# Define available resolutions with icons
resolutions = {
    "512x512": (512, 512),
    "1024x1024": (1024, 1024),
    "2048x2048": (2048, 2048)
}

# Input fields
selected_resolution = st.selectbox("Select resolution:", list(resolutions.keys()))
height, width = resolutions[selected_resolution]
steps = st.slider("Inference Steps", min_value=1, max_value=50, value=8)
scales = st.slider("Guidance Scale", min_value=1.0, max_value=10.0, value=3.5, step=0.1)
prompt = st.text_input("Enter your prompt:")
seed = st.number_input("Seed (for reproducibility)", min_value=0, max_value=10000, value=3413)

# Add a button to generate the image
if st.button("Generate"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            # Generate the image
            image_path = generate_image(height, width, steps, scales, prompt, seed)
            
            if image_path:
                # Display the image preview
                st.image(image_path, caption="Generated Image", use_column_width=True)
                
                # Provide a download button
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name="generated_image.png",
                        mime="image/png"
                    )
