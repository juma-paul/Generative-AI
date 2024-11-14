# from flask import Blueprint, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from app.document_processor import DocumentProcessor
# from app.vector_store import VectorStore
# from app.chat_manager import ChatManager
# from config import Config

# main = Blueprint('main', __name__)

# document_processor = DocumentProcessor(Config)
# vector_store = VectorStore(Config)
# chat_manager = ChatManager(Config)

# @main.route('/')
# def index():
#     return render_template('index.html')

# @main.route('/api/upload', methods=['POST'])
# def upload_document():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join('uploads', filename)
#         file.save(file_path)
        
#         # Process document
#         document = document_processor.load_document(file_path)
#         chunks = document_processor.process_document(document)
#         embeddings = document_processor.generate_embeddings(chunks)
        
#         # Store in vector database
#         vector_store.add_documents(chunks, embeddings)
        
#         return jsonify({'message': 'Document processed successfully'}), 200
    
#     return jsonify({'error': 'Invalid file type'}), 400

import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.chat_manager import ChatManager
from config import Config

main = Blueprint('main', __name__)

document_processor = DocumentProcessor(Config)
vector_store = VectorStore(Config)
chat_manager = ChatManager(Config)

# Add this constant at the top of the file
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Ensure the uploads directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the file
            file.save(file_path)
            
            # Process document
            document = document_processor.load_document(file_path)
            chunks = document_processor.process_document(document)
            embeddings = document_processor.generate_embeddings(chunks)
            
            # Store in vector database
            vector_store.add_documents(chunks, embeddings)
            
            return jsonify({'message': 'Document processed successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing document: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Generate query embedding
    query_embedding = document_processor.embeddings.embed_query(query)
    
    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(query_embedding)
    
    # Generate response
    response = chat_manager.generate_response(query, relevant_docs)
    
    return jsonify({'response': response}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS