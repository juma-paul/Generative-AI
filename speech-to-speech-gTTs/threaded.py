import os
import time
import queue
import threading
import re
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("openai_api_key"))

# Global flags for threading
shutdown_event = threading.Event()

class VoiceAssistant:
    def __init__(self, wake_word="hey fiwa", energy_threshold=300, pause_threshold=0.8, verbose=False):
        self.wake_word = wake_word
        self.energy_threshold = energy_threshold
        self.pause_threshold = pause_threshold
        self.verbose = verbose
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.conversation_active = False  # Track whether conversation is active

    def log(self, message):
        """Log messages for debugging."""
        if self.verbose:
            print(f"[{datetime.now()}] {message}")

    def record_audio(self):
        """Record audio and push it to the queue."""
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.energy_threshold
        recognizer.pause_threshold = self.pause_threshold

        with sr.Microphone(sample_rate=16000) as source:
            self.log("Listening for wake word...")
            while not shutdown_event.is_set():
                try:
                    audio = recognizer.listen(source)
                    self.audio_queue.put(audio.get_wav_data())
                except sr.WaitTimeoutError:
                    self.log("No speech detected.")
                except Exception as e:
                    self.log(f"Recording error: {e}")

    def transcribe_audio(self):
        """Transcribe audio and push the transcription to the queue."""
        while not shutdown_event.is_set():
            try:
                audio_data = self.audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            temp_audio_path = "temp_audio.wav"
            with open(temp_audio_path, "wb") as temp_audio_file:
                temp_audio_file.write(audio_data)

            try:
                with open(temp_audio_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", file=audio_file
                    )
                text = transcription.text.strip()
                self.log(f"Transcribed: {text}")

                # Ignore short or invalid inputs
                if len(text) < 3:
                    self.log(f"Ignored short transcription: {text}")
                    continue

                # Wake word detection
                if not self.conversation_active and re.search(self.wake_word, text, re.IGNORECASE):
                    text = re.sub(self.wake_word, "", text, flags=re.IGNORECASE).strip()
                    self.conversation_active = True
                    self.log("Wake word detected. Starting conversation.")

                # Stop command
                if "stop" in text.lower():
                    self.log("Stop command received. Conversation ended.")
                    self.conversation_active = False
                    continue

                if self.conversation_active:
                    self.result_queue.put(text)
            except Exception as e:
                self.log(f"Transcription error: {e}")
            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)


    def generate_response(self):
        """Generate responses for transcribed text."""
        while not shutdown_event.is_set():
            try:
                user_input = self.result_queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.5
                )
                reply = response.choices[0].message.content.strip()
                self.log(f"AI Response: {reply}")
                self.text_to_speech(reply)
            except Exception as e:
                self.log(f"AI response error: {e}")

    def text_to_speech(self, text):
        """Convert text to speech and play it."""
        try:
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save("response.mp3")
            audio = AudioSegment.from_mp3("response.mp3")
            play(audio)
            self.log("Response spoken.")
        except Exception as e:
            self.log(f"TTS error: {e}")
        finally:
            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

    def run(self):
        """Run the voice assistant using threading."""
        threads = [
            threading.Thread(target=self.record_audio),
            threading.Thread(target=self.transcribe_audio),
            threading.Thread(target=self.generate_response)
        ]

        for thread in threads:
            thread.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            shutdown_event.set()
        finally:
            for thread in threads:
                thread.join()
            print("Voice assistant terminated.")

def main():
    assistant = VoiceAssistant(
        wake_word="hey fiwa",
        verbose=True
    )
    assistant.run()

if __name__ == "__main__":
    main()
