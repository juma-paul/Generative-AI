import os
import io
import requests
from PIL import Image
from gtts import gTTS
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Get API key and endpoints from environment variables
hf_api_key = os.getenv("hf-general-api-key")
BLIP_API_URL = os.getenv("itt-blip-model")
SD_API_URL = os.getenv("tti-diffusion-model")

headers = {"Authorization": f"Bearer {hf_api_key}"}

from PIL import Image

def resize_image(image, max_size=(1024, 1024)):
    """Resize image to fit within max_size dimensions, preserving aspect ratio."""
    image.thumbnail(max_size, Image.LANCZOS)
    return image

def captioner(image):
    # Resize large images to improve compatibility
    image = resize_image(image)  # Limit to max dimensions of 1024x1024

    # Convert all image formats to RGB and save to bytes
    img_byte_arr = io.BytesIO()
    
    # Ensure compatibility by converting mode and setting format
    image = image.convert("RGB")  # Standardize color format for compatibility
    image_format = image.format if image.format in ['JPEG', 'PNG', 'BMP', 'GIF'] else 'PNG'
    image.save(img_byte_arr, format=image_format)
    
    # Send image bytes to the API
    response = requests.post(BLIP_API_URL, headers=headers, data=img_byte_arr.getvalue())
    response.raise_for_status()
    
    return response.json()[0]['generated_text']


def generate(text_prompt):
    # Send request to Stable Diffusion model
    response = requests.post(
        SD_API_URL,
        headers=headers,
        json={"inputs": text_prompt}
    )
    
    # Convert response bytes to PIL Image
    image = Image.open(io.BytesIO(response.content))
    return image

def text_to_speech(text):
    # Convert text to speech and save to temporary file
    tts = gTTS(text=text, lang='en')
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name
