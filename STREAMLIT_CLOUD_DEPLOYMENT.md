# Streamlit Cloud Deployment Guide

## Overview
This guide will help you deploy your FestFusion application to Streamlit Cloud with proper Google Cloud credentials configuration.

## Step 1: Prepare Your Repository

1. **Ensure your repository is on GitHub**
   - Push all your code to a GitHub repository
   - Make sure the repository is public (for free Streamlit Cloud deployment)

2. **Verify your file structure**
   ```
   festfusion2.o/
   ├── streamlit_frontend.py
   ├── requirements.txt
   ├── .streamlit/
   │   └── secrets.toml (local only, not committed)
   ├── .gitignore (includes .streamlit/secrets.toml)
   └── festfusion-project-cc628988dd80.json (local only, not committed)
   ```

## Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Configure your app:**
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `streamlit_frontend.py`
   - **App URL**: Choose a unique URL (optional)

## Step 3: Configure Secrets in Streamlit Cloud

**IMPORTANT**: You need to add your Google Cloud service account credentials as secrets.

1. **In your Streamlit Cloud dashboard, go to your app settings**
2. **Click on "Secrets" in the left sidebar**
3. **Add the following configuration:**

```toml
[gcp_service_account]
type = "service_account"
project_id = "festfusion-project"
private_key_id = "cc628988dd800f93275a2f1ee4af6ac7dca629a5"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDHkcUBAaL6Cg3b\niYJGQFZEo7lQ0FqGlnbLMpo9ESIMt+lOOzpdbIQg/hCQFRC2KdVNKcY5arvEBYRx\n9SasyWTpNVw60Hbp5GrVkpLVmkWUrmNwgTfgZYd9NicMMZWZaPwX7SO3vadPPWLv\nzhmJxlrhea6Ss1jyHmURa70ptNhCs2OqFZa7MKXebVXv823L1ynbAiBL51/SUb7m\nOoT64LsVjCfHmiaeZCXiQMQvV7TTYKx3igcPk9RG29Kuvr4MuICd/J0xf+v2YbGk\nYq2r4Sd8PN1FGrQil3l0zL76TwcAudq1s5GAyt46GKKLLLVHYj7fxAY9MxJpD1cD\n8eRvyx51AgMBAAECggEAAbAy64itGAfp6O5KHu2FkqQ+7wHVjjdrea8WfRyYvjpN\nETdw4uBGODWQrs4Fe5ZcLVWvOAZLiy46b1tcpdAOAudhExyh25CDiIXU/lUahcDk\nQEv7jMdXGiumhhTM+ESvg0VN4iH1g8xYEAFyl7GI9x4tfaS3mdQWKfZQc0VKIhBO\nHNIBgk29FW4kBAcIZ/5db2gza2QlDl7dPaiOt6MVIWsjgrRrKHy0xFKWdsSYYTo4\nQCseZQ/QKtwmJ6EUanObhkqOx86K6METXcN/jCmvhIB8fwkqnkLoi6ipmfX2rkqq\nrUdfLGEoGIE8UjTEDnsmkJzOEGHjX/1oqy105JgZEQKBgQDndquopXn7YtplLLoR\n/SdzTzyZuywL9bGjk0bLqCp3tz+WHAD4ynspzn8mJUmiIBm1+p+vPr3I0Op33YGQ\nfMZBDe0DpoLbf1C5lRr9OHAGpFmhJyg3oW07WD7I7rvIVTnuXEiULYA8xF7t3zaV\ncxCSAOamzIzMhXvBwRAxzkH4xQKBgQDcuZLL41iFir8Zx8fWivQpUX1/DtX6sv1T\n/jMAiN4A9AzNxQbyEztnkutPw02v9+qCGj0orDlAwEDYZjyAxxNjvbxgFFzkdk2/\nm8CF7zKh2nbDg5JfN4rp7Vw93ejBpkxqH5ml5pcZhDHDZcY2V0hNvqQcl7pHVJyh\nHH+yrz0J8QKBgBGl/b61J1Dgn7BZMbLPb6OeJgu+tsQOrsW/JAXBQ8OvCD0k03ok\nzjFI2m8JJs0iz3MNsgFFsmjObSJIlGl06hTpv+moV4/u7DPKR62JERmgjGj6OFnN\niCufNeJSOaUzwmAHT01lDsMTYf2XKG1KwbewM+YB8LZjcyU52EdD58nVAoGBANXW\nY0VsJ+KYnLNZPV24mPs+m5pwwRV0OsEY0EiAULQTvCPN8gCsaSzaxWYtDCKiyGrr\nCL1SvNTibPA5e/w24a4Lr2hV0fj0NDahqk8XgbIUeGLKIRBmOwqOjoLRbiHN/tIB\nc1WqpFBwJdXrz6/tt3q6azvYMvvQGT5s4bo206fBAoGBAMeqF46LgF86eyGkWq8m\nQnVGXecQ9rJKfelSFyfEqSPoq2XKZ6PQ2qtj0rBJdYOTjqa8i9XZs+NiElFpD0dN\nwMcChcKTLmwLlBpx+uAUjCEzizx4H5cySzXlqebheMBHa9605YxhDNHXJ0JOJYUV\nLjoJuniY7ClL/2vps6+9GjL7\n-----END PRIVATE KEY-----\n"
client_email = "sheets-editor@festfusion-project.iam.gserviceaccount.com"
client_id = "106783971887321384324"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/sheets-editor%40festfusion-project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

4. **Click "Save"**

## Step 4: Deploy and Test

1. **Click "Deploy!" in Streamlit Cloud**
2. **Wait for the deployment to complete**
3. **Test your application:**
   - Upload a file
   - Process it
   - Try to save to Google Sheets
   - Verify the data appears in your Google Sheet

## Troubleshooting

### Common Issues:

1. **"No such file or directory" error**
   - **Solution**: Make sure you've added the secrets in Streamlit Cloud
   - The application will use `st.secrets["gcp_service_account"]` instead of the local file

2. **Google Sheets access denied**
   - **Solution**: Make sure your Google Sheet "FestFusion Data" is shared with:
     - Email: `sheets-editor@festfusion-project.iam.gserviceaccount.com`
     - Permission: Editor

3. **App fails to deploy**
   - **Solution**: Check that all required packages are in `requirements.txt`
   - Verify your main file path is correct

### Security Notes:

- ✅ The `festfusion-project-cc628988dd80.json` file is excluded from Git
- ✅ The `.streamlit/secrets.toml` file is excluded from Git
- ✅ Credentials are stored securely in Streamlit Cloud secrets
- ✅ The application works both locally and in the cloud

## Local Development

For local development, the app will:
1. First try to use Streamlit secrets (if available)
2. Fall back to the local JSON file if secrets are not available

This ensures the same code works both locally and in Streamlit Cloud.

## Next Steps

After successful deployment:
1. Share your Streamlit Cloud app URL
2. Test all functionality thoroughly
3. Monitor the Google Sheet for new entries
4. Consider setting up monitoring and alerts

Your app should now work perfectly on Streamlit Cloud! 🎉 