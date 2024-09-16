from flask import Flask, request, jsonify
from gpt import search_consultants

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def generate():
    data = request.json
    skills = data.get('skills', '')
    recommendations = search_consultants(skills)

    return jsonify({'recommendations': recommendations})


if __name__ == "__main__":
    app.run(port=5000)