# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from model_handler import ModelHandler
from database import DatabaseHandler
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize handlers
QDRANT_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.WHWgODRKHPQLOcbNxjU1t_WnP-5zdqs1NM7HW6Yqqmg'
QDRANT_HOST = 'https://c12eb6fc-bc48-41ab-bd2f-889fb87e93f2.eu-central-1-0.aws.cloud.qdrant.io'

model_handler = ModelHandler()
db_handler = DatabaseHandler(QDRANT_HOST, QDRANT_KEY)

@app.route('/api/search/text', methods=['POST'])
def search_by_text():
    data = request.json
    query_text = data.get('query', '')
    
    if not query_text:
        return jsonify({'error': 'Query text is required'}), 400
    
    print('Get embedding')
    # Get text embedding from the model
    text_embedding = model_handler.get_text_embedding(query_text)
    print('Embedding successfully created')
    # Search in QDrant
    
    results = db_handler.search_by_text(text_embedding)
    print('Result acquired from QDrant')
    # Format and return results
    formatted_results = []
    for res in results:
        formatted_results.append({
            'id': res.id,
            'score': res.score,
            'payload': res.payload
        })
    
    print()
    return jsonify({'results': formatted_results})

@app.route('/api/search/image', methods=['POST'])
def search_by_image():
    # Check if the request contains an image
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Get the image from the request
    image_file = request.files['image']
    image = Image.open(image_file)
    
    # Get image embedding from the model
    image_embedding = model_handler.get_image_embedding(image)
    
    # Search in QDrant
    results = db_handler.search_by_text(image_embedding)
    
    # Format and return results
    formatted_results = []
    for res in results:
        formatted_results.append({
            'id': res.id,
            'score': res.score,
            'payload': res.payload
        })
    
    return jsonify({'results': formatted_results})

@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"})

if __name__ == '__main__':
    app.run(debug=True, port=8000)