import streamlit as st
from gradio_client import Client
from PIL import Image
import requests
from io import BytesIO
import random  # Import the random module

# Initialize Gradio client
client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")

# Title and description
st.title('Hyperdyn - Image Generation Tool')
st.subheader('Generate images using the latest AI models.')

# Define resolutions
resolutions = {
    '256x256': (256, 256),
    '512x512': (512, 512),
    '1024x1024': (1024, 1024)
}

# Prompt input
prompt = st.text_input('Enter your prompt:', 'Astronaut riding a horse')

# Resolution selector
resolution = st.selectbox('Select resolution:', list(resolutions.keys()))

# Button to generate image
if st.button('Generate'):
    st.write('Generating image...')
    
    # Show loading spinner
    with st.spinner('Generating...'):
        # Extract dimensions from selected resolution
        width, height = resolutions[resolution]
        
        try:
            # Generate image using Gradio client
            result = client.predict(
                height=height,
                width=width,
                steps=8,
                scales=3.5,
                prompt=prompt,
                seed=random.randint(0, 10000),  # Use random seed
                api_name="/process_image"
            )
            
            # Get image path from result
            img_path = result  # Adjust based on the actual response format
            
            # Load and display image
            response = requests.get(img_path)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption='Generated Image', use_column_width=True)
            
            # Provide download button
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            st.download_button(
                label='Download Image',
                data=img_bytes,
                file_name='generated_image.png'
            )
        except Exception as e:
            st.error(f'An error occurred: {e}')
