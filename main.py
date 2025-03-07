from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import json

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

class Function:
    def search_file(api_key, folder_id, filename):
        """
        Searches for a file inside a public Google Drive folder.

        Returns:
            dict: JSON response containing 'filename', 'view_link', and 'download_link'
        """
        service = build('drive', 'v3', developerKey=api_key)
        
        # Query: Find file by name inside the given folder
        query = f"'{folder_id}' in parents and name='{filename}'"
        
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if files:
            file_id = files[0]['id']
            view_link = f"https://drive.google.com/file/d/{file_id}/view"
            download_link = f"https://drive.google.com/uc?id={file_id}&export=download"
            
            return {
                "filename": filename,
                "view_link": view_link,
                "download_link": download_link
            }
        else:
            return {
                "filename": filename,
                "view_link": "",
                "download_link": ""
            }
    def load_data():
        try:
            with open("data.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

@app.route('/search', methods=['GET'])
def search():
    folder_id = request.args.get('folder_id')  # Get folder ID from request
    filename = request.args.get('filename')  # Get filename from request
    
    if not folder_id or not filename:
        return jsonify({"error": "Missing 'folder_id' or 'filename' parameter"}), 400
    
    result = Function.search_file(API_KEY, folder_id, filename)
    return jsonify(result)  # Return JSON response


@app.route('/verifycertificate/<string:code>/', methods=['GET'])
def verify_certificate(code):
    code = str(code)
    if len(code) == 10:
        # Load data from data.json
        data = Function.load_data()
        folder_id = "1zQq-d9ykmhI7vbhW5ls5idaCgU4bahUK"
        # Check if the code exists in the data.json
        if code in data:
            try:
                certificate_details = Function.search_file(API_KEY, folder_id, f"{code}.png")
            except:
                certificate_details = {}
            return jsonify({
                "message": "valid code", 
                "user_details": data[code],
                "certificate_details": certificate_details
                })
        else:
            return jsonify({"message": "invalid code"}), 400  # Entry not found
    else:
        return jsonify({"message": "invalid code"}), 400  # 400 for bad request

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
