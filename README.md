# Customer Support Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)](https://openai.com/api/)

An intelligent chatbot powered by OpenAI's API, designed to crawl any specified website and answer user questions based on the extracted content.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The Customer Support Chatbot is a Flask-based web application that combines web crawling capabilities with natural language processing. It crawls a specified website, extracts textual content, and leverages OpenAI's API to provide intelligent responses to user queries about the website's content and services.

## Features

- Customizable web crawling functionality to extract content from any specified website
- Integration with OpenAI's API for natural language processing
- User-friendly web interface for asking questions
- Real-time responses based on crawled content
- SSL verification for secure connections
- Efficient text processing and tokenization
- Embedding generation for semantic search

## Demo

[Link to live demo](#) (Add your demo link here)

![Chatbot Interface](path/to/screenshot1.png)
![Example Conversation](path/to/screenshot2.png)

## Built With

- [Python](https://www.python.org/) - The primary programming language
- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [OpenAI API](https://openai.com/api/) - For natural language processing
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For web scraping
- [Pandas](https://pandas.pydata.org/) - For data manipulation
- [NumPy](https://numpy.org/) - For numerical computations
- [TikToken](https://github.com/openai/tiktoken) - For tokenization
- [Certifi](https://certifi.io/) - For SSL/TLS certification

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer-support-chatbot.git
   cd customer-support-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Update the `DOMAIN` and `FULL_URL` constants in the main script to point to the website you want to crawl.

2. Run the crawler to extract website content:
   ```bash
   python chatbot.py
   ```

3. Start the Flask application:
   ```bash
   flask run
   ```

4. Open a web browser and navigate to `http://127.0.0.1:5000/`

5. Enter your question in the chat interface and receive AI-powered responses based on the crawled content.

## Project Structure

```
customer-support-chatbot/
├── chatbot.py          # Main application script
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (git-ignored)
├── README.md           # Project documentation
│
├── templates/          # HTML templates
│   ├── index.html      # Main page template
│   └── result.html     # Result page template
│
├── text/               # Scraped text content
│   └── domain_name/    # Domain-specific content
│
└── processed/          # Processed data files
    ├── scraped.csv     # Initial processed data
    └── embeddings.csv  # Data with embeddings
```

## How It Works

1. **Web Crawling**: The application crawls the specified website, extracting text content from various pages.
2. **Data Processing**: Extracted text is cleaned, tokenized, and split into manageable chunks.
3. **Embedding Generation**: Text chunks are converted into embeddings using OpenAI's API.
4. **User Interface**: A simple web interface allows users to input questions.
5. **Question Answering**: When a question is asked, the application:
   - Generates an embedding for the question
   - Finds the most relevant text chunks using cosine similarity
   - Creates a context from these chunks
   - Sends the context and question to OpenAI's API for an answer
   - Displays the answer to the user

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/customer-support-chatbot](https://github.com/yourusername/customer-support-chatbot)