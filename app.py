from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

app = Flask(__name__)
CORS(app)

# SQLite database config (no env needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(32), nullable=False)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([
        {'text': p.text, 'timestamp': p.timestamp} for p in posts
    ])

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
    allowed = {'Ik', 'We', 'Ons', 'Onze', 'Oranje', 'Koningsdag', 'Koning', 'Koningin', 'Nederland', 'NL', 'Feest'}
    tokens = re.findall(NAME_PATTERN, text)
    for name in tokens:
        if name not in allowed and not text.startswith(name):
            return jsonify({'error': 'Het is niet toegestaan om namen van personen te noemen.'}), 400
    post = Post(text=text, timestamp=datetime.now().isoformat(timespec='seconds'))
    db.session.add(post)
    db.session.commit()
    return jsonify({'text': post.text, 'timestamp': post.timestamp}), 201

@app.route('/initdb', methods=['POST'])
def initdb():
    db.create_all()
    return 'Database initialized!', 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
