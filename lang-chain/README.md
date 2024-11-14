# SFBU Customer Support System

An intelligent customer support system built with Flask and OpenAI's GPT, leveraging Retrieval Augmented Generation (RAG) for context-aware document search and responses.

![Alt text](./uploads/main-page.png)


## Features
- PDF and text document processing with vectorization
- Semantic search with ChromaDB
- Real-time chat interface
- Document upload functionality
- Context-aware responses using RAG

## Tech Stack
- **Backend**: Flask, LangChain
- **AI/ML**: OpenAI GPT-3.5
- **Vector Store**: ChromaDB
- **Frontend**: HTML, TailwindCSS, JavaScript

## Setup

1. Clone the repository:
```bash
git clone https://github.com/juma-paul/customer-support-chatbot/tree/main
cd lang-chain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## API Endpoints

- `POST /api/upload`: Upload documents
- `POST /api/chat`: Send chat messages
- `GET /`: Main interface

## Configuration

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL_NAME = "gpt-3.5-turbo"
VECTOR_DB_PATH = "vectorstore"
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
```

## Usage

1. Start the server:
```bash
python3 run.py
```

2. Access the interface:
```
http://localhost:5000
```

3. Upload documents and start chatting!

## License
MIT License

## Project Documentation
- [Google Slides Presentation](https://docs.google.com/presentation/d/1saWrs2FMyTSwFIYWc92XNO7MlsDFMGkOAJQbtbulTIw/edit?usp=sharing)
- [Project Link](https://github.com/juma-paul/customer-support-chatbot/tree/main/lang-chain)