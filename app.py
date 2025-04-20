from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# In-memory storage for posts
posts = []

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts[::-1])  # newest first

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text is required'}), 400
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
