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

# Expanded abusive/negative phrases
ABUSIVE_PHRASES = [
    "get out", "leave me alone", "i'm angry", "i'm furious", "i'm livid", "you're infuriating", "don't talk to me", "go away", "i hate this", "i can't stand it", "that's enough", "stop it", "you're a jerk", "you're a fool", "you're a waste of space", "i'm sick of you", "i'm done with this", "don't push me", "you're testing me", "i'm warning you", "you should be ashamed of yourself", "whatever", "it doesn't matter", "who cares", "that's not my problem", "it's fine", "i don't care", "it's no big deal", "don't worry about it", "just forget about it", "it's over", "let it go", "it's pointless to argue", "you're impossible", "i can't deal with this", "it's hopeless", "it's going nowhere"
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
    # Abusive word/phrase filter
    lowered = text.lower()
    for word in ABUSIVE_WORDS:
        if word in lowered:
            return jsonify({'error': 'Abusive or inappropriate language is not allowed.'}), 400
    for phrase in ABUSIVE_PHRASES:
        if phrase in lowered:
            return jsonify({'error': 'Negatieve of beledigende berichten zijn niet toegestaan.'}), 400
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
