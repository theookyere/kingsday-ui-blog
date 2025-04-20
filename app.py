from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import os
import re

app = Flask(__name__)
CORS(app)

# In-memory storage for posts
posts = []

# List of Dutch and English abusive words (expand as needed)
ABUSIVE_WORDS = [
    'klootzak', 'lul', 'sukkel', 'hufter', 'kut', 'tering', 'fuck', 'shit', 'bitch', 'asshole', 'idiot', 'hoer', 'dom', 'stom', 'slet',
    'cancer', 'kanker', 'nazi', 'racist', 'neuk', 'pis', 'dick', 'damn', 'retard', 'gay', 'homo', 'faggot', 'slut', 'whore'
]

# Very basic name pattern (capitalized word, not at start of sentence)
NAME_PATTERN = re.compile(r'(?:\b[A-Z][a-z]{2,}\b)')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts[::-1])  # newest first

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    # Abusive word filter
    lowered = text.lower()
    for word in ABUSIVE_WORDS:
        if word in lowered:
            return jsonify({'error': 'Abusive or inappropriate language is not allowed.'}), 400
    # Name detection (Dutch/English style)
    # Disallow any capitalized word not at the start, and not "Ik", "We", "Oranje", etc.
    allowed = {'Ik', 'We', 'Ons', 'Onze', 'Oranje', 'Koningsdag', 'Koning', 'Koningin', 'Nederland', 'NL', 'Feest'}
    tokens = re.findall(NAME_PATTERN, text)
    for name in tokens:
        if name not in allowed and not text.startswith(name):
            return jsonify({'error': 'Het is niet toegestaan om namen van personen te noemen.'}), 400
    post = {
        'text': text,
        'timestamp': datetime.now().isoformat(timespec='seconds')
    }
    posts.append(post)
    return jsonify(post), 201

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
