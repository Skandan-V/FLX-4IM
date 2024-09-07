import streamlit as st
from PIL import Image
from io import BytesIO
import random
import time

# Dummy image generation function (replace with actual model code)
def generate_image(prompt, width, height):
    # Simulate image generation
    time.sleep(3)  # Simulate processing time
    img = Image.new('RGB', (width, height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    return img

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
        
        # Generate the image
        try:
            image = generate_image(prompt, width, height)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            # Display the image
            st.image(image, caption='Generated Image', use_column_width=True)
            
            # Provide download button
            st.download_button(
                label='Download Image',
                data=img_bytes,
                file_name='generated_image.png'
            )
        except Exception as e:
            st.error(f'An error occurred: {e}')
