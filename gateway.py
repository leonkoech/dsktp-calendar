#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from credentialsAPI import CredentialsAPIservice

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/check_application', methods=['GET'])
def check_application():
    return jsonify({"success": "application is running"}), 200

@app.route('/get_credentials', methods=['GET'])
def get_credentials():

    # uses credentials.json to get a user token for the user 
    try:
        credentials = CredentialsAPIservice.getCredentials()
    except:
        return jsonify({"error": "there was an error fetching credentials"}), 400
    print(credentials)
    return jsonify({'success': 'credentials verified'}), 200

@app.route('/save_settings', methods=['POST'])
def save_settings():
    # receives credentials.json 
    # writes credentials.json data to .env/credentials.json
    settings = request.json.get('results')
    if not settings:
        return jsonify({'error': 'settings parameter is required'}), 400
    
    # Check if JSON data is provided in the request body
    if not request.is_json:
        return jsonify({'error': 'No JSON data provided in the request'}), 400
    
    with open('./components/settings.json', 'w') as f:
        json.dump(settings, f)
    return jsonify({'success':"data has been received"}), 200


if __name__ == '__main__':
    app.run()
