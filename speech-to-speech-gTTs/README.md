# AI Voice Assistant

## Overview

The voice assistant is a real-time voice assistant that leverages speech recognition, AI-powered conversation, and text-to-speech technologies to create an interactive voice interface. The assistant can listen for a wake word, transcribe speech, generate intelligent responses, and speak back to the user.

## Features

- **Wake Word Detection**: Activates with the custom wake word "hey fiwa"
- **Speech-to-Text**: Uses OpenAI's Whisper for accurate audio transcription
- **AI Conversation**: Powered by OpenAI's GPT-3.5-turbo for intelligent responses
- **Text-to-Speech**: Converts AI responses to spoken audio using Google Text-to-Speech (gTTS)
- **Multithreaded Design**: Ensures responsive and efficient processing
- **Configurable Settings**: Customize wake word, audio sensitivity, and verbosity

## Prerequisites

- Python 3.8+
- OpenAI API Key
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/juma-paul/customer-support-chatbot/tree/main/speech-to-speech-gTTs
   cd speech-to-speech-gTTs
   ```

2. Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     openai_api_key=your_openai_api_key_here
     ```

## Usage

Run the assistant:
```bash
python3 threaded.py
```

### Interaction Commands
- **Wake Up**: Say "hey fiwa" to start the conversation
- **Stop Conversation**: Say "stop" to end the active conversation

## Customization

Modify the `VoiceAssistant` initialization to customize:
- Wake word
- Energy threshold for speech detection
- Pause threshold
- Verbose logging

```python
assistant = VoiceAssistant(
    wake_word="hey fiwa",  # Change wake word
    energy_threshold=300,  # Adjust mic sensitivity
    pause_threshold=0.8,   # Adjust speech pause detection
    verbose=True           # Toggle detailed logging
)
```

## Dependencies

- `speech_recognition`: Audio capture and processing
- `openai`: AI response generation and transcription
- `gtts`: Text-to-speech conversion
- `pydub`: Audio playback
- `python-dotenv`: Environment variable management

## Troubleshooting

- Ensure microphone permissions are granted
- Check internet connectivity
- Verify API key is valid and has sufficient credits
- Adjust `energy_threshold` if wake word detection is inconsistent

## Limitations

- Requires continuous internet connection
- Performance depends on microphone quality and background noise
- Uses OpenAI's API, which may incur usage costs

## Future Improvements

- Add wake word training
- Implement more advanced conversation context management
- Support multiple languages
- Add wake word and conversation logging

## License

MIT License

## Acknowledgments

- OpenAI for Whisper and GPT models
- Google Text-to-Speech
- Python Speech Recognition community

## Contributing

Contributions are welcome! Please read the contributing guidelines before getting started.

## Project Link
Please find link to the project [here](https://github.com/juma-paul/customer-support-chatbot/tree/main/spech-to-speech-gTTs)