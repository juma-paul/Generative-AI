# AI Voice Assistant

## Overview

This is an intelligent voice assistant developed using OpenAI's GPT and Whisper technologies for seamless voice-based interactions.

## Features

- Wake word activation
- Real-time speech recognition
- AI-powered conversational responses
- Text-to-speech output
- Multithreaded processing

## Quick Start

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Set up OpenAI API key in `.env`
   ```
   openai_api_key=your_key_here
   ```

3. Run the assistant
   ```bash
   python3 app.py
   ```

## Usage

- **Activate**: Say "hey fiwa"
- **Interact**: Ask questions or give commands
- **End**: Say "stop"

## Technologies

- Python
- OpenAI (GPT-3.5, Whisper, TTS)
- SpeechRecognition
- PyDub

## Configuration

Customize assistant behavior:
```python
assistant = VoiceAssistant(
    wake_word="hey fiwa",
    energy_threshold=300,
    verbose=True
)
```

## Requirements

- Python 3.8+
- OpenAI API Key
- Active internet connection

## Limitations

- Requires continuous internet
- API usage incurs costs
- Performance depends on microphone quality

## License

MIT License

## Project Link
Please find link to the project [here]()