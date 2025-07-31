# 🔐 Secure OAuth Setup Guide for FestFusion

## ⚠️ IMPORTANT: Keep Your Credentials Private!

Your OAuth credentials are **personal and sensitive**. Never upload them to GitHub or share them publicly.

## 📋 Your OAuth Credentials (Keep Private!)

Based on your credentials, here's what you need to configure:

### For Streamlit Cloud (Recommended for Production):

1. **Go to your Streamlit Cloud app settings**
2. **Navigate to "Secrets"**
3. **Add this configuration:**

```toml
[google_oauth]
client_id = "26082816180-vmgb2pfbmtl03gufnnuabsmiq7rcp14r.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "https://fovrmlcxappqkdesvg64pwg.streamlit.app/"
project_id = "festfusion-project"
```

### For Local Development:

1. **Create a `.streamlit/secrets.toml` file** (this is already in .gitignore)
2. **Add the same configuration as above**

## 🔧 Step-by-Step Setup

### Step 1: Enable Google Drive API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `festfusion-project`
3. Go to "APIs & Services" > "Library"
4. Search for "Google Drive API" and enable it

### Step 2: Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in app information:
   - App name: "FestFusion Telangana"
   - User support email: Your email
   - Developer contact information: Your email
4. Add scopes: `https://www.googleapis.com/auth/drive.file`
5. Add test users (your email)

### Step 3: Update OAuth Credentials
1. Go to "APIs & Services" > "Credentials"
2. Edit your OAuth 2.0 Client ID
3. Add these Authorized redirect URIs:
   - `https://fovrmlcxappqkdesvg64pwg.streamlit.app/`
   - `http://localhost:8501/` (for local testing)
4. Save changes

### Step 4: Configure Streamlit Cloud Secrets
1. Go to your Streamlit Cloud app
2. Click "Settings" → "Secrets"
3. Paste the TOML configuration from above
4. Save

## 🚀 Testing Your Setup

### Local Testing:
```bash
# Run the OAuth-enabled frontend
streamlit run streamlit_oauth_frontend.py
```

### Cloud Deployment:
1. Push your code to GitHub (credentials are safe in secrets)
2. Streamlit Cloud will automatically deploy with OAuth

## 🔒 Security Best Practices

✅ **DO:**
- Store credentials in Streamlit Cloud secrets
- Use environment variables for local development
- Keep credentials in `.gitignore`
- Use OAuth 2.0 for user authentication

❌ **DON'T:**
- Upload credentials to GitHub
- Share credentials in public repositories
- Hardcode credentials in your code
- Use service accounts for user-facing apps

## 🛠️ Troubleshooting

### Common Issues:

1. **"Invalid redirect URI"**
   - Check that your redirect URI matches exactly
   - Include trailing slash: `https://your-app.streamlit.app/`

2. **"OAuth consent screen not configured"**
   - Complete the OAuth consent screen setup
   - Add your email as a test user

3. **"API not enabled"**
   - Enable Google Drive API in Google Cloud Console

4. **"Credentials not found"**
   - Check Streamlit Cloud secrets configuration
   - Verify TOML syntax is correct

## 📞 Need Help?

If you encounter issues:
1. Check Google Cloud Console for API quotas
2. Verify OAuth consent screen is published
3. Ensure all redirect URIs are correctly configured
4. Test with local development first

---

**Remember: Your credentials are now secure and will work with both local development and Streamlit Cloud deployment!** 🎉 