# 🏛️ FestFusion Telangana

An AI-powered platform that preserves and celebrates the rich cultural heritage of Telangana's festivals through story collection, AI summarization, and digital archiving.

## 🚀 Features

- **📝 Story Submission**: Users can submit festival stories with text and multimedia files
- **🎵 Audio Transcription**: Automatic transcription of audio recordings using Whisper AI
- **🤖 AI Summarization**: Intelligent summarization of stories using Hugging Face models
- **📁 File Archiving**: Secure storage of uploaded files in Google Drive
- **📊 Data Organization**: Structured data storage in Google Sheets by village/district
- **🌐 Modern UI**: Beautiful Streamlit frontend with responsive design
- **🔌 RESTful API**: Flask backend for scalable architecture

## 📋 Project Roadmap

| Step | Description | Status |
|------|-------------|--------|
| 1️⃣ | Set up Flask API to receive uploads on your PC | ✅ **Complete** |
| 2️⃣ | Use Ngrok to expose your local Flask endpoint | 🔄 **Next** |
| 3️⃣ | Build a Streamlit frontend for user uploads + village selection | ✅ **Complete** |
| 4️⃣ | Once uploaded, run AI model (Hugging Face) to summarize content | ✅ **Complete** |
| 5️⃣ | Store everything in folders by village name | ✅ **Complete** |
| 6️⃣ | (Optional) Add a viewer page to read summaries and see uploads | 🔜 **Coming Soon** |

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with Drive and Sheets APIs enabled
- Google Service Account credentials

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd festfusion2.o

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Services Setup

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Drive API and Google Sheets API

2. **Create Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Create a new service account
   - Download the JSON credentials file
   - Rename it to `festfusion-project-cc628988dd80.json` and place in project root

3. **Google Drive Setup**:
   - Create a folder in Google Drive for file uploads
   - Share the folder with your service account email
   - Copy the folder ID from the URL

4. **Google Sheets Setup**:
   - Create a new Google Sheet
   - Share it with your service account email
   - Note the sheet name

### 3. Configuration

Update `config.py` with your Google services information:

```python
# Update these values in config.py
GOOGLE_DRIVE_FOLDER_ID = "your_actual_folder_id_here"
GOOGLE_SHEET_NAME = "your_actual_sheet_name_here"
```

### 4. Run the Application

#### Option 1: Use the startup script (Recommended)
```bash
python start_server.py
```

#### Option 2: Run servers separately
```bash
# Terminal 1: Start Flask API
python flask_api.py

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_frontend.py
```

### 5. Access the Application

- **Streamlit Frontend**: http://localhost:8501
- **Flask API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/health` | GET | Health check endpoint |
| `/villages` | GET | Get list of Telangana districts |
| `/upload` | POST | Upload files and generate summaries |
| `/uploads/<filename>` | GET | Serve uploaded files |

### Upload API Usage

```bash
curl -X POST http://localhost:5000/upload \
  -F "village=Hyderabad" \
  -F "story_text=Your festival story here" \
  -F "file=@/path/to/your/file.jpg"
```

## 📁 Project Structure

```
festfusion2.o/
├── app.py                      # Original Streamlit app
├── flask_api.py               # Flask API backend
├── streamlit_frontend.py      # New Streamlit frontend
├── config.py                  # Configuration settings
├── start_server.py            # Startup script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── festfusion-project-cc628988dd80.json  # Google credentials
└── uploads/                   # File upload directory
```

## 🎯 Next Steps

### Step 2: Ngrok Integration
To expose your local Flask API to the internet:

1. **Install Ngrok**:
   ```bash
   # Download from https://ngrok.com/
   # Or use package manager
   ```

2. **Expose Flask API**:
   ```bash
   ngrok http 5000
   ```

3. **Update Frontend**:
   Update `FLASK_API_URL` in `streamlit_frontend.py` with the ngrok URL.

### Step 6: Viewer Page
Create a new page to browse and view submitted stories:

```bash
# Create viewer page
streamlit run viewer_page.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Flask API not starting**:
   - Check if port 5000 is available
   - Ensure all dependencies are installed
   - Check Google credentials file exists

2. **Google Services errors**:
   - Verify service account has proper permissions
   - Check folder and sheet sharing settings
   - Ensure APIs are enabled in Google Cloud Console

3. **File upload issues**:
   - Check file size (max 16MB)
   - Verify file type is allowed
   - Ensure uploads directory exists

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export FLASK_DEBUG=True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for AI models
- Streamlit for the frontend framework
- Flask for the backend API
- Google Cloud Platform for storage services
