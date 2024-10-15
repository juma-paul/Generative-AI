from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Set up your OpenAI API key
load_dotenv()
API_KEY = os.getenv("openai_api_key")
client = OpenAI(api_key=API_KEY)

@app.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.json
    comment = data['comment']
    language = data['language']

    # Step 2: Generate email subject
    subject = generate_subject(comment)

    # Step 3: Generate summary
    summary = generate_summary(comment)

    # Step 4: Sentiment analysis
    sentiment = analyze_sentiment(comment)

    # Step 5: Generate email
    email = generate_email_content(comment, subject, summary, sentiment, language)

    return jsonify({
        'subject': subject,
        'email': email
    })

def generate_subject(comment):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a customer support assistant for an electronics store."},
            {"role": "user", "content": f"Generate a subject for an email based on this comment: {comment}"}
        ]
    )
    return response.choices[0].message.content

def generate_summary(comment):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a customer support assistant for an electronics store."},
            {"role": "user", "content": f"Generate a summary of this comment: {comment}"}
        ]
    )
    return response.choices[0].message.content

def analyze_sentiment(comment):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis tool."},
            {"role": "user", "content": f"Analyze the sentiment of this comment as either Positive or Negative: {comment}"}
        ]
    )
    return response.choices[0].message.content

def generate_email_content(comment, subject, summary, sentiment, language):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a customer support assistant for an electronics store."},
            {"role": "user", "content": f"Create an email in {language} based on this comment: '{comment}', summary: '{summary}', sentiment: '{sentiment}', and subject: '{subject}'"}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)