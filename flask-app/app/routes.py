from flask import Blueprint, render_template, request
from .utils import answer_question, load_data

main = Blueprint('main', __name__)

# Load processed data for answering questions
df = load_data()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/results', methods=['POST'])
def ask():
    question = request.form['question']
    answer = answer_question(df, question=question)
    return render_template('result.html', question=question, answer=answer)