#!flask/bin/python
from textblob import TextBlob

from flask import Flask, jsonify, abort, request
import uuid 
from flask_cors import CORS
import os
from connector import get_database
dbname = get_database()
collection_name = dbname["sentimentCollection"]
app = Flask(__name__)
CORS(app)
@app.route('/api/post_sentiment', methods=['POST'])
def post_sentiment():
    if not request.json or not 'text' in request.json:
        abort(400)
    blob = TextBlob(request.json['text'])
    print(blob.sentiment)
    dictObj = {
        "id": uuid.uuid4().hex[:6].lower(),
        "sentiment": blob.polarity,
        "text": request.json['text']
    }
    response = collection_name.insert_one(dictObj)
    return jsonify({'message': 'succesfully posted to cloudant', "text": request.json['text'], "sentiment": blob.polarity }), 201

if __name__ == '__main__':
    app.run(debug=True, port=8080)