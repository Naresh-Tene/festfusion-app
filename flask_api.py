from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
from config import *

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set maximum content length
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# File handling functions
def save_file_locally(file, village):
    """Save uploaded file to local folder organized by village"""
    try:
        # Create village folder if it doesn't exist
        village_folder = UPLOAD_FOLDER / village
        village_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        saved_filename = f"{timestamp}_{original_filename}"
        
        # Save file to village folder
        file_path = village_folder / saved_filename
        file.save(str(file_path))
        
        return {
            "success": True,
            "saved_filename": saved_filename,
            "file_path": str(file_path),
            "original_filename": original_filename,
            "file_type": file.content_type,
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        print(f"Error saving file: {e}")
        return {"success": False, "error": str(e)}

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "FestFusion API is running",
        "endpoints": {
            "/upload": "POST - Upload files and generate summaries",
            "/villages": "GET - Get list of Telangana districts",
            "/health": "GET - Health check"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/villages')
def get_villages():
    """Get list of Telangana districts"""
    return jsonify({"villages": sorted(TELANGANA_DISTRICTS)})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload - just save file locally and return info"""
    try:
        # Check if village is provided
        village = request.form.get('village')
        if not village or village not in TELANGANA_DISTRICTS:
            return jsonify({"error": "Valid village/district is required"}), 400
        
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "File is required"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Save file locally organized by village
        result = save_file_locally(file, village)
        
        if not result["success"]:
            return jsonify({"error": result["error"]}), 500
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "data": {
                "village": village,
                "saved_filename": result["saved_filename"],
                "original_filename": result["original_filename"],
                "file_type": result["file_type"],
                "file_size": result["file_size"],
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(str(UPLOAD_FOLDER), filename)

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT) 