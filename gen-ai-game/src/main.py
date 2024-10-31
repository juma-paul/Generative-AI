import gradio as gr
from game_functions import captioner, generate, text_to_speech

def caption_and_generate(image):
    # Generate caption from uploaded image
    caption = captioner(image)
    
    # Generate new image from caption
    generated_image = generate(caption)
    
    # Convert caption to speech
    audio_file = text_to_speech(caption)
    
    return [caption, generated_image, audio_file]

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Describe-and-Generate Game")
    
    # Input
    image_upload = gr.Image(label="Your first image", type="pil")
    
    # Button
    btn_all = gr.Button("Caption, Generate, and Play Audio")
    
    # Outputs
    caption = gr.Textbox(label="Generated caption")
    image_output = gr.Image(label="Generated Image")
    audio_output = gr.Audio(label="Audio Caption")

    # Connect components
    btn_all.click(
        fn=caption_and_generate,
        inputs=[image_upload],
        outputs=[caption, image_output, audio_output]
    )

if __name__ == "__main__":
    demo.launch(share=True)