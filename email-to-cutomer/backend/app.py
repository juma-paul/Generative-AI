
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Initialize Flask app and enable Cross-Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("openai_api_key")  # Updated key name for consistency
client = OpenAI(api_key=API_KEY)

# Utility function for OpenAI API calls, centralizing repetitive logic
def generate_openai_response(messages, model="gpt-3.5-turbo", temperature=0.3):
    """Generates a response from the OpenAI model based on input messages."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

# Function to generate a simulated customer comment based on product details
def generate_customer_comment(products_data):
    system_message = f"""Assume you are a customer of an electronics company. The following products' details are provided between triple backticks: ```{products_data}```. Your task is to write a realistic 100-word comment about these products."""
    user_message = "Please generate a customer comment based on the provided product details."
    
    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    return generate_openai_response(prompt)

# Function to generate an email subject based on the customer comment
def generate_email_subject(comment):
    system_message = f"""You are a customer support assistant for an electronics company. The following is a customer comment about a product. The comment is delimited by triple backticks. ```{comment}```. Based on this comment, create an appropriate email subject."""
    user_message = "Generate an email subject for a customer support email."
    
    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    return generate_openai_response(prompt)

# Function to generate a summary of the customer's comment
def generate_summary(comment):
    system_message = f"""You are a customer support assistant. The following is a customer comment about products. The comment is delimited by triple backticks: ```{comment}```. Summarize the key points of the comment in a concise manner."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Please summarize the following customer comment."}
    ])

# Function to analyze the sentiment of the customer's comment (Positive/Negative/Neutral)
def analyze_sentiment(comment):
    system_message = f"""You are a sentiment analysis tool. The following is a customer's comment about products. The comment is delimited by triple backticks: ```{comment}```. Please analyze the sentiment of this comment and categorize it as Positive, Negative, or Neutral."""
    
    result = generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Analyze the sentiment of this comment."}
    ])
    
    return result.strip().capitalize()  # Ensuring output is properly formatted (positive, negative, neutral)

# Function to translate text into a specified language
def get_translation(text, language):
    system_message = f"""You are a professional translator. The following text is delimited by triple backticks: ```{text}```. Translate it into {language}."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Translate this text into {language}."}
    ])

# Route to handle email generation based on customer feedback
@app.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.json
    comment = data.get('comment', '')
    language = data.get('language', 'English')
    translate_comment = data.get('translate_comment', False)  # Translate the comment if true
    translate_email = data.get('translate_email', False)  # Translate the generated email if true

    # Validate that a comment was provided
    if not comment:
        return jsonify({'error': 'Comment is required'}), 400

    try:
        # Generate customer comment, subject, summary, and sentiment
        customer_comment = generate_customer_comment(comment)
        subject = generate_email_subject(customer_comment)
        summary = generate_summary(customer_comment)
        sentiment = analyze_sentiment(customer_comment)

        # Generate the email content based on the customer interaction data
        email_content = generate_openai_response([
            {"role": "system", "content": f"Create a customer support email based on the following details: comment: `{customer_comment}`, subject: `{subject}`, summary: `{summary}`, sentiment: `{sentiment}`."},
            {"role": "user", "content": f"Generate an email in {language} based on the information provided."}
        ])

        # Handle translation requests if needed
        if translate_comment:
            customer_comment = get_translation(customer_comment, language)
        
        if translate_email:
            email_content = get_translation(email_content, language)

        return jsonify({
            'subject': subject,
            'email': email_content,
            'comment': customer_comment,
            'summary': summary,
            'sentiment': sentiment
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Simple test endpoint to check if the backend is working
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is working'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)