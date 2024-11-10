# SFBU Customer Support System

## Overview
An intelligent customer support system built with Flask and OpenAI's GPT, leveraging Retrieval Augmented Generation (RAG) for accurate, context-aware responses based on local documentation.


## Features
- Document processing and vectorization
- Semantic search capabilities
- Conversational memory for follow-up questions
- Web-based user interface
- Real-time response generation
- Context-aware answers from local documents

## Tech Stack
- **Backend**: Flask
- **AI/ML**: OpenAI GPT-3.5, LangChain
- **Vector Store**: ChromaDB
- **Frontend**: HTML, CSS, JavaScript
- **Documentation**: PDF, Web content processing

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/sfbu-customer-support.git
cd sfbu-customer-support
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Add your OpenAI API key to .env file
```

## Project Structure
```
sfbu-customer-support/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── document_loader.py  # Document processing
│   ├── text_splitter.py    # Text chunking
│   ├── embeddings_manager.py
│   ├── vector_store.py     # Vector database management
│   ├── retriever.py        # Document retrieval
│   ├── llm_manager.py      # LLM integration
│   └── main.py            # Application entry point
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
└── requirements.txt
```

## Implementation Steps

### 1. Document Processing Pipeline
- Document loading from multiple sources
- Text splitting for optimal processing
- Embedding generation using OpenAI
- Vector store creation with ChromaDB

### 2. Retrieval System
- Similarity search implementation
- Context-aware document retrieval
- Relevance ranking

### 3. Conversation Management
- Chat memory implementation
- Follow-up question handling
- Context preservation

### 4. Web Interface
- Real-time chat interface
- Document upload functionality
- Response visualization

## Usage

1. Start the Flask server
```bash
python run.py
```

2. Access the web interface
```
http://localhost:5000
```

3. Upload documents and start chatting!

## API Endpoints

### Document Management
```python
POST /api/upload
GET  /api/documents
```

### Chat Interface
```python
POST /api/chat
GET  /api/chat/history
```

## Configuration

Key configurations in `config.py`:
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
VECTOR_DB_PATH = "vectorstore"
```

## Project Documentation
- [Google Slides Presentation](https://docs.google.com/presentation/d/1saWrs2FMyTSwFIYWc92XNO7MlsDFMGkOAJQbtbulTIw/edit?usp=sharing)
- [Project Portfolio](https://github.com/yourusername/portfolio)

## Machine Learning Components
- ChatGPT Integration
- Document Embeddings
- Similarity Search
- Conversation Management

## Future Enhancements
- [ ] Multi-language support
- [ ] Advanced document preprocessing
- [ ] Real-time document updates
- [ ] Analytics dashboard
- [ ] Custom training capabilities

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI for GPT models
- LangChain for the RAG framework
- SFBU for project guidance

## Contact

Project Link: [https://github.com/yourusername/sfbu-customer-support](https://github.com/yourusername/sfbu-customer-support)