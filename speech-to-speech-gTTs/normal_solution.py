import os
import time
import pyaudio
import wave
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import threading

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("openai_api_key"))

class VoiceAssistant:
    def __init__(self, wake_word="hey fiwa", energy_threshold=300, pause_threshold=0.8, verbose=False):
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        
        # Configuration
        self.wake_word = wake_word
        self.verbose = verbose
        self.conversation_active = False

    def log(self, message):
        """Verbose logging method"""
        if self.verbose:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    def transcribe_audio(self, audio):
        """Transcribe audio using OpenAI Whisper"""
        temp_audio_path = "temp_audio.wav"
        try:
            with open(temp_audio_path, "wb") as temp_audio_file:
                temp_audio_file.write(audio.get_wav_data())

            with open(temp_audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text.strip()
        except Exception as e:
            self.log(f"Transcription Error: {e}")
            return None
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

    def get_ai_response(self, user_input):
        """Get response from OpenAI"""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Your responses should strictly be in english"},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                max_tokens=30
            )
            response_text = response.choices[0].message.content
            print(f"AI Response: {response_text}")  # Log response
            return response_text
        except Exception as e:
            self.log(f"AI Response Error: {e}")
            return "Sorry, I couldn't generate a response."


    def text_to_speech(self, text):
        """Convert text to speech and play"""
        try:
            # Save TTS to file
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save("response.mp3")

            # Play audio
            audio = AudioSegment.from_mp3("response.mp3")
            play(audio)

            self.log("Response spoken successfully")
        except Exception as e:
            self.log(f"Text-to-Speech Error: {e}")
        finally:
            # Clean up audio file
            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

    def listen_for_wake_word(self, source):
        """Listen for wake word in a separate thread"""
        while True:
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)

                # Listen for audio
                audio = self.recognizer.listen(source)

                # Transcribe audio
                transcription = self.transcribe_audio(audio)
                
                if transcription:
                    self.log(f"Transcribed: {transcription}")

                    # Check for conversation control
                    if "stop" in transcription.lower():
                        print("Conversation ended.")
                        self.conversation_active = False
                        continue

                    # Handle wake word or ongoing conversation
                    if (not self.conversation_active and 
                        transcription.lower().startswith(self.wake_word.lower())):
                        # Remove wake word and start conversation
                        transcription = transcription[len(self.wake_word):].strip()
                        self.conversation_active = True
                        print("Conversation started.")
                        # Generate and speak response
                        response = self.get_ai_response(transcription)
                        print(f"Response: {response}")
                        self.text_to_speech(response)

                    elif self.conversation_active:
                        # Handle conversation after wake word is detected
                        response = self.get_ai_response(transcription)
                        print(f"Response: {response}")
                        self.text_to_speech(response)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                self.log(f"Unexpected error: {e}")

    def run(self):
        """Main listening loop"""
        with sr.Microphone() as source:
            print("Listening... Say the wake word to start.")

            # Start a new thread to listen for the wake word
            wake_word_thread = threading.Thread(target=self.listen_for_wake_word, args=(source,))
            wake_word_thread.daemon = True
            wake_word_thread.start()

            # Keep the main thread alive to allow the listening thread to run
            while True:
                time.sleep(1)

def main():
    # Initialize and run the voice assistant
    assistant = VoiceAssistant(
        wake_word="hey fiwa", 
        verbose=True
    )
    assistant.run()

if __name__ == "__main__":
    main()
