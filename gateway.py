#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify

from credentialsAPI import CredentialsAPIservice

app = Flask(__name__)
@app.route('/')
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route('/save_credentials', methods=['POST'])
def save_credentials():
    # receives credentials.json 
    # writes credentials.json data to .env/credentials.json
    credentials_file = request.args.get('credentials')
    if not credentials_file:
        return credentials_file({'error': 'File is invalid'}), 400
    
    # Check if a file was sent in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided in the request'}), 400
    
    uploaded_file = request.files['file']
    
    # Specify the path where you want to save the file
    save_path = f'.env/{uploaded_file.filename}'
    
    # Save the uploaded file to the specified location
    uploaded_file.save(save_path)
    return jsonify({'success': 'credential file saved'})

@app.route('/get_credentials', methods=['GET'])
def get_credentials():

    # uses credentials.json to get a user token for the user 
    try:
        credentials = CredentialsAPIservice.getCredentials()
    except:
        return jsonify({"error": "there was an error fetching credentials"})
    print(credentials)
    return jsonify({'success': 'credentials verified'})

@app.route('/save_settings', methods=['POST'])
def save_settings():
    # receives credentials.json 
    # writes credentials.json data to .env/credentials.json
    settings = request.args.get('results')
    if not settings:
        return jsonify({'error': 'settings parameter is required'}), 400
    
    # Check if JSON data is provided in the request body
    if not request.is_json:
        return jsonify({'error': 'No JSON data provided in the request'}), 400
    
    # Extract JSON data from the request body
    json_data = request.json
    
    # Assuming your JavaScript map is directly sent in the JSON data
    if settings in json_data:
        return jsonify(json_data[settings])
    else:
        return jsonify({'error': 'data not found for provided location'}), 404



@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    with open('/tmp/data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('/tmp/data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)
app.run()