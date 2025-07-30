import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask API Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# File Upload Configuration
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4', 'txt', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Google Services Configuration
import os
BASE_DIR = Path(__file__).parent
GOOGLE_CREDENTIALS_FILE = BASE_DIR / "festfusion-project-cc628988dd80.json"
GOOGLE_DRIVE_FOLDER_ID = "1DBeE3IW9h3i4m67OXS7nZ2iVO0zXXk0Q"  # FestFusion Uploads folder
GOOGLE_SHEET_NAME = "FestFusion Data"  # Google Sheet name

# AI Model Configuration
SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"
TRANSCRIPTION_MODEL = "openai/whisper-base"

# Telangana Districts
TELANGANA_DISTRICTS = [
    "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", 
    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", 
    "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", 
    "Mancherial", "Medak", "Medchal-Malkajgiri", "Nagarkurnool", "Nalgonda", 
    "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", 
    "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
    "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri"
]

# Create necessary directories
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Environment variables (for production)
def get_env_var(key, default=None):
    """Get environment variable with fallback to default"""
    return os.getenv(key, default)

# Production settings
PRODUCTION = get_env_var('PRODUCTION', 'False').lower() == 'true'
if PRODUCTION:
    FLASK_DEBUG = False
    FLASK_HOST = get_env_var('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(get_env_var('FLASK_PORT', 5000)) 