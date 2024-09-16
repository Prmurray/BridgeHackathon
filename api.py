from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import search_consultants

app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "*"}}, methods=['POST', 'OPTIONS'], allow_headers=['Content-Type'])

@app.route('/search', methods=['OPTIONS'])
def options():
    return '', 204

@app.route('/search', methods=['POST'])
def generate():
    data = request.json
    skills = data.get('skills', '')
    recommendations = search_consultants(skills)

    return jsonify({'recommendations': recommendations})


if __name__ == "__main__":
    app.run(host="dev.bridgeskills.com", port=5000,)