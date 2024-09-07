import streamlit as st
import time
import base64
from PIL import Image
import requests

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
        # Example API call, replace with actual API call
        # Extract dimensions from selected resolution
        width, height = resolutions[resolution]

        # Example request payload (replace with actual API URL)
        url = 'http://your-api-endpoint.com/process_image'
        payload = {
            'height': height,
            'width': width,
            'steps': 8,
            'scales': 3.5,
            'prompt': prompt,
            'seed': 3413
        }

        # Send request to API
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        # Check response and display image
        if 'image_path' in result:
            img_path = result['image_path']
            image = Image.open(img_path)
            st.image(image, caption='Generated Image', use_column_width=True)
            
            # Provide download button
            with open(img_path, 'rb') as file:
                st.download_button(label='Download Image', data=file, file_name='generated_image.png')
        else:
            st.error('Failed to generate image. Please try again.')

# Live logs section
st.subheader('Live Logs:')
log_text = st.empty()
for i in range(10):  # Simulate live logs for 10 seconds
    log_text.text(f'Log entry {i + 1}: Processing...')
    time.sleep(1)
log_text.text('Completed.')
