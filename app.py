from flask import Flask, render_template, request, jsonify
from service.service import fetch_mentions

from dotenv import load_dotenv


load_dotenv(".env", override=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_term = data.get('search_term', '').strip()

    if not search_term:
        return jsonify({'error': 'search_term is required'}), 400

    results = fetch_mentions(search_term)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
