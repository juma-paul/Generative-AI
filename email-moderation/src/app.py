from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import random

# Initialize Flask app and enable Cross-Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("openai_api_key")
client = OpenAI(api_key=API_KEY)

# Load products data
def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)

def check_moderation(text):
    """Check text content using OpenAI's moderation API."""
    try:
        response = client.moderations.create(input=text)
        result = response["results"][0]
        flagged = result["flagged"]
        categories = {k: v for k, v in result["categories"].items() if v}
        return {
            'flagged': flagged,
            'categories': categories,
            'original_text': text
        }
    except Exception as e:
        return {'error': str(e)}

def moderate_content(text, moderation_result):
    """Provide feedback on flagged content and suggest alternatives."""
    feedback = {
        "original_text": text,
        "flagged": moderation_result['flagged'],
        "flagged_categories": moderation_result['categories'],
        "suggestion": "Please revise your input to ensure it adheres to community guidelines."
    }
    
    # Construct feedback about flagged words
    if moderation_result['flagged']:
        flagged_words = ", ".join(moderation_result['categories'].keys())
        feedback["suggested_changes"] = (
            f"The following categories were flagged in your comment: {flagged_words}. "
            "Consider revising these parts or avoiding similar language."
        )
    else:
        feedback["suggested_changes"] = "No issues detected in your input."
    
    return feedback

def generate_openai_response(messages, model="gpt-3.5-turbo", temperature=0.3):
    """Generates a response from the OpenAI model based on input messages."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def get_random_product():
    products = load_products()
    return random.choice(list(products.values()))

def generate_customer_comment(product_data):
    system_message = """
    You are a customer writing a realistic 100-word comment about this product.
    However, this comment will intentionally contain inappropriate content 
    that falls under various moderation categories such as hate speech, 
    self-harm, sexual content, and violence.
    """
    
    comment = generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Write a customer comment about: {product_data}"}
    ])
    
    # Check moderation on generated comment
    moderation_result = check_moderation(comment)
    if moderation_result.get('flagged', False):
        feedback = moderate_content(comment, moderation_result)
        return feedback  

    return comment

def generate_email_subject(comment):
    system_message = """Create an email subject based on this customer comment. 
    Maintain professionalism regardless of the comment's content."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Generate an email subject for: {comment}"}
    ])

def generate_summary(comment):
    system_message = """Summarize this customer comment professionally, 
    focusing on the key points while maintaining appropriate language."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Summarize the comment: {comment}"}
    ])

def analyze_sentiment(comment):
    system_message = """Analyze the sentiment (Positive/Negative/Neutral) of this comment, 
    focusing on the overall message rather than specific language used."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"What is the sentiment of: {comment}"}
    ])

def get_translation(text, target_language):
    system_message = f"""Translate this text to {target_language}, maintaining the appropriate
    tone while ensuring the translation is professional and appropriate."""
    return generate_openai_response([
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Translate to {target_language}: {text}"}
    ])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_product', methods=['GET'])
def random_product():
    try:
        product = get_random_product()
        return jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.json
    product_data = data.get('product_data', '')
    target_language = data.get('language', 'English')
    translate_comment = data.get('translate_comment', False)
    translate_email = data.get('translate_email', False)
    use_system_comment = data.get('use_system_comment', True)
    user_comment = data.get('user_comment', '')

    try:
        # Generate or use provided comment
        if use_system_comment:
            customer_comment = generate_customer_comment(product_data)
            # Check if the comment was flagged
            if isinstance(customer_comment, dict) and customer_comment.get('flagged', False):
                return jsonify(customer_comment)  # Return feedback if flagged
        else:
            customer_comment = user_comment
        
        # Check moderation for the customer comment
        moderation_result = check_moderation(customer_comment)
        original_comment = customer_comment if moderation_result.get('flagged', False) else None

        # Moderate content if flagged
        if moderation_result.get('flagged', False):
            feedback = moderate_content(customer_comment, moderation_result)
            return jsonify(feedback)  # Return feedback if flagged

        # Generate email content and analysis
        subject = generate_email_subject(customer_comment)
        summary = generate_summary(customer_comment)
        sentiment = analyze_sentiment(customer_comment)

        email_content = generate_openai_response([
            {"role": "system", "content": "You are a customer service representative. Write a professional response email."},
            {"role": "user", "content": f"Write an email responding to this comment: {customer_comment}"}
        ])
        
        # Check moderation for the email content
        email_moderation_result = check_moderation(email_content)
        if email_moderation_result.get('flagged', False):
            email_feedback = moderate_content(email_content, email_moderation_result)
            return jsonify(email_feedback)  # Return feedback if flagged

        # Handle translations if requested
        if translate_comment:
            customer_comment = get_translation(customer_comment, target_language)
        
        if translate_email:
            email_content = get_translation(email_content, target_language)
            subject = get_translation(subject, target_language)

        return jsonify({
            'product': product_data,
            'comment': customer_comment,
            'original_comment': original_comment,
            'moderation_result': moderation_result,
            'subject': subject,
            'summary': summary,
            'sentiment': sentiment,
            'email': email_content
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)







# # app.py
# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from dotenv import load_dotenv
# from openai import OpenAI
# import os
# import json
# import random

# # Initialize Flask app and enable Cross-Origin Resource Sharing
# app = Flask(__name__)
# CORS(app)

# # Load API key from environment variables
# load_dotenv()
# API_KEY = os.getenv("openai_api_key")
# client = OpenAI(api_key=API_KEY)

# # Load products data
# def load_products():
#     with open('products.json', 'r') as file:
#         return json.load(file)

# def check_moderation(text):
#     """Check text content using OpenAI's moderation API."""
#     try:
#         response = client.moderations.create(input=text)
#         result = response.results[0]
#         flagged = result.flagged
#         categories = {k: v for k, v in result.categories.model_dump().items() if v}
#         return {
#             'flagged': flagged,
#             'categories': categories,
#             'original_text': text
#         }
#     except Exception as e:
#         return {'error': str(e)}

# def moderate_content(text):
#     """Moderate flagged content by replacing inappropriate words."""
#     # Simple moderation - replace flagged words with asterisks
#     # In a production environment, you'd want a more sophisticated approach
#     words = text.split()
#     moderated_words = ['*' * len(word) if len(word) > 3 else word for word in words]
#     return ' '.join(moderated_words)

# def generate_openai_response(messages, model="gpt-3.5-turbo", temperature=0.3):
#     """Generates a response from the OpenAI model based on input messages."""
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature
#     )
#     return response.choices[0].message.content

# def get_random_product():
#     products = load_products()
#     return random.choice(list(products.values()))

# def generate_customer_comment(product_data, include_flagged_content=False):
#     system_message = """
#     You are a customer writing a realistic 100-word comment about this product. 
#     """ + ("""Include some controversial or inappropriate content that would trigger 
#     content moderation flags (such as mild profanity or frustration).""" if include_flagged_content else "")
    
#     comment = generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"Write a customer comment about: {product_data}"}
#     ])
    
#     return comment

# def generate_email_subject(comment):
#     system_message = """Create an email subject based on this customer comment. 
#     Maintain professionalism regardless of the comment's content."""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"Generate an email subject for: {comment}"}
#     ])

# def generate_summary(comment):
#     system_message = """Summarize this customer comment professionally, 
#     focusing on the key points while maintaining appropriate language."""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"Summarize the comment: {comment}"}
#     ])

# def analyze_sentiment(comment):
#     system_message = """Analyze the sentiment (Positive/Negative/Neutral) of this comment, 
#     focusing on the overall message rather than specific language used."""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"What is the sentiment of: {comment}"}
#     ])

# def get_translation(text, target_language):
#     system_message = f"""Translate this text to {target_language}, maintaining the appropriate
#     tone while ensuring the translation is professional and appropriate."""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"Translate to {target_language}: {text}"}
#     ])

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_random_product', methods=['GET'])
# def random_product():
#     try:
#         product = get_random_product()
#         return jsonify(product)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/generate_email', methods=['POST'])
# def generate_email():
#     data = request.json
#     product_data = data.get('product_data', '')
#     target_language = data.get('language', 'English')
#     translate_comment = data.get('translate_comment', False)
#     translate_email = data.get('translate_email', False)
#     use_system_comment = data.get('use_system_comment', True)
#     user_comment = data.get('user_comment', '')
#     include_flagged_content = data.get('include_flagged_content', False)

#     try:
#         # Generate or use provided comment
#         if use_system_comment:
#             customer_comment = generate_customer_comment(product_data, include_flagged_content)
#         else:
#             customer_comment = user_comment

#         # Check moderation
#         moderation_result = check_moderation(customer_comment)
#         original_comment = customer_comment

#         # Moderate content if flagged
#         if moderation_result.get('flagged', False):
#             customer_comment = moderate_content(customer_comment)

#         # Generate email content and analysis
#         subject = generate_email_subject(customer_comment)
#         summary = generate_summary(customer_comment)
#         sentiment = analyze_sentiment(customer_comment)

#         email_content = generate_openai_response([
#             {"role": "system", "content": "You are a customer service representative. Write a professional response email."},
#             {"role": "user", "content": f"Write an email responding to this comment: {customer_comment}"}
#         ])

#         # Handle translations if requested
#         if translate_comment:
#             customer_comment = get_translation(customer_comment, target_language)
        
#         if translate_email:
#             email_content = get_translation(email_content, target_language)
#             subject = get_translation(subject, target_language)

#         return jsonify({
#             'product': product_data,
#             'comment': customer_comment,
#             'original_comment': original_comment if moderation_result.get('flagged', False) else None,
#             'moderation_result': moderation_result,
#             'subject': subject,
#             'summary': summary,
#             'sentiment': sentiment,
#             'email': email_content
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)






# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# from dotenv import load_dotenv
# from openai import OpenAI
# import os
# import json
# import random

# # Initialize Flask app and enable Cross-Origin Resource Sharing
# app = Flask(__name__)
# CORS(app)

# # Load API key from environment variables
# load_dotenv()
# API_KEY = os.getenv("openai_api_key")
# client = OpenAI(api_key=API_KEY)

# # Load products data
# def load_products():
#     with open('products.json', 'r') as file:
#         return json.load(file)

# # Utility function for OpenAI API calls
# def generate_openai_response(messages, model="gpt-3.5-turbo", temperature=0.3):
#     """Generates a response from the OpenAI model based on input messages."""
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature
#     )
#     return response.choices[0].message.content

# # Function to get a random product
# def get_random_product():
#     products = load_products()
#     return random.choice(list(products.values()))

# # Generate customer comment based on product details
# def generate_customer_comment(product_data):
#     system_message = f"""You are a customer writing a realistic 100-word comment about this product: {product_data}"""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": "Write a customer comment"}
#     ])

# # Existing helper functions remain the same
# def generate_email_subject(comment):
#     system_message = f"""Create an email subject based on this customer comment: ```{comment}```"""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": "Generate an email subject"}
#     ])

# def generate_summary(comment):
#     system_message = f"""Summarize this customer comment: ```{comment}```"""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": "Summarize the comment"}
#     ])

# def analyze_sentiment(comment):
#     system_message = f"""Analyze the sentiment (Positive/Negative/Neutral) of this comment: ```{comment}```"""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": "What is the sentiment?"}
#     ])

# def get_translation(text, target_language):
#     system_message = f"""Translate this text to {target_language}: ```{text}```"""
#     return generate_openai_response([
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": f"Translate to {target_language}"}
#     ])

# # Route for the main page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to get a random product
# @app.route('/get_random_product', methods=['GET'])
# def random_product():
#     try:
#         product = get_random_product()
#         return jsonify(product)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Modified route to handle email generation
# @app.route('/generate_email', methods=['POST'])
# def generate_email():
#     data = request.json
#     product_data = data.get('product_data', '')
#     target_language = data.get('language', 'English')
#     translate_comment = data.get('translate_comment', False)
#     translate_email = data.get('translate_email', False)

#     try:
#         # Generate initial content
#         customer_comment = generate_customer_comment(product_data)
#         subject = generate_email_subject(customer_comment)
#         summary = generate_summary(customer_comment)
#         sentiment = analyze_sentiment(customer_comment)

#         # Generate email content
#         email_content = generate_openai_response([
#             {"role": "system", "content": "You are a customer service representative. Write a professional response email."},
#             {"role": "user", "content": f"Write an email responding to this comment: {customer_comment}"}
#         ])

#         # Handle translations if requested
#         if translate_comment:
#             customer_comment = get_translation(customer_comment, target_language)
        
#         if translate_email:
#             email_content = get_translation(email_content, target_language)
#             subject = get_translation(subject, target_language)

#         return jsonify({
#             'product': product_data,
#             'comment': customer_comment,
#             'subject': subject,
#             'summary': summary,
#             'sentiment': sentiment,
#             'email': email_content
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)