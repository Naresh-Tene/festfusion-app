# FestFusion Deployment Guide

## 🚀 Deploy to GitHub & Streamlit Cloud

### Step 1: Upload to GitHub

1. **Initialize Git Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial FestFusion app with clean summaries"
   ```

2. **Create New Repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name: `festfusion-app` (or any name you prefer)
   - Make it Public
   - Don't initialize with README (we already have one)

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/Naresh-Tene/festfusion-app.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Repository: Select your `festfusion-app` repository
   - Branch: `main`
   - Main file path: `streamlit_frontend.py`
   - Click "Deploy"

### Step 3: Configure Google Sheets Integration

1. **Add Google Credentials as Secret:**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add the following:
   ```
   GOOGLE_CREDENTIALS = {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-private-key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
     "client_id": "your-client-id",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
   }
   ```

2. **Or Use Environment Variables:**
   - Add `GOOGLE_CREDENTIALS` as environment variable
   - Paste your entire service account JSON content

### Step 4: Access Your App

Your app will be available at:
```
https://YOUR_APP_NAME-YOUR_USERNAME.streamlit.app
```

## 📁 Files Included in Deployment

✅ **Core Application Files:**
- `streamlit_frontend.py` - Main Streamlit application
- `flask_api.py` - Backend API server
- `requirements.txt` - Python dependencies
- `config.py` - Configuration settings
- `README.md` - Project documentation

✅ **Supporting Files:**
- `.gitignore` - Git ignore rules
- `DEPLOYMENT.md` - This deployment guide

❌ **Excluded Files:**
- `venv/` - Virtual environment
- `uploads/` - Uploaded files
- `__pycache__/` - Python cache
- `*.json` - Google credentials (added as secrets)
- Test files

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Make sure all dependencies are in `requirements.txt`
   - Check that all import statements are correct

2. **Google Sheets Connection Failed:**
   - Verify Google credentials are added as secrets
   - Check service account has proper permissions
   - Ensure Google Sheets API is enabled

3. **App Not Loading:**
   - Check main file path is correct (`streamlit_frontend.py`)
   - Verify repository and branch are correct
   - Check Streamlit Cloud logs for errors

## 📞 Support

If you encounter any issues:
1. Check Streamlit Cloud logs
2. Verify all secrets are configured correctly
3. Test locally first to ensure everything works

## 🎉 Success!

Once deployed, you can share your app URL with anyone to use FestFusion! 