import streamlit as st
from gradio_client import Client
import base64
from PIL import Image
import io

# Streamlit configuration
st.set_page_config(page_title="Image Generation Tool", layout="wide")
st.title("Hyperdyn")
st.subheader("Image Generation Tool")

# Initialize Gradio client
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Function to encode image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to process image generation
def generate_image(prompt):
    try:
        st.write("Generating image... Please wait.")
        result = client.predict(
            height=1024,
            width=1024,
            steps=8,
            scales=3.5,
            prompt=prompt,
            seed=3413,
            api_name="/process_image"
        )
        return result
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Displaying UI elements
prompt = st.text_input("Enter your prompt for image generation", "")

if st.button("Generate Image"):
    if prompt:
        # Show process loader
        with st.spinner("Generating image..."):
            response = generate_image(prompt)
        
        if response:
            # Display raw response
            st.write("Raw response:", response)
            
            # If response is a path to an image file
            image_path = response
            if image_path:
                # Load image
                image = Image.open(image_path)
                
                # Display image
                st.image(image, caption="Generated Image")
                
                # Convert image to base64
                base64_image = image_to_base64(image)
                
                # Download button
                st.download_button(
                    label="Download Image",
                    data=base64.b64decode(base64_image),
                    file_name="generated_image.png",
                    mime="image/png"
                )
    else:
        st.warning("Please enter a prompt to generate an image.")

# Display API endpoint URL in footer
st.markdown(
    """
    <footer style="text-align: center;">
        <p>API endpoint: <code>{}</code></p>
    </footer>
    """.format("http://localhost:8501/process_image"), 
    unsafe_allow_html=True
)
