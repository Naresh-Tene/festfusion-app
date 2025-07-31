# 🔧 Service Account Setup for Streamlit Cloud

## ⚠️ **Quick Fix for Google Sheets Integration**

Since OAuth doesn't work well in Streamlit Cloud, we need to use a service account approach.

## 📋 **Step 1: Get Your Service Account JSON**

1. **Go to Google Cloud Console:** https://console.cloud.google.com/
2. **Select your project:** `festfusion-project`
3. **Navigate to:** IAM & Admin → Service Accounts
4. **Find your service account** (or create one if needed)
5. **Click on the service account** → Keys → Add Key → Create new key
6. **Download the JSON file**

## 📝 **Step 2: Add to Streamlit Cloud Secrets**

1. **Go to Streamlit Cloud:** https://streamlit.io/cloud
2. **Select your app:** `fovrmlcxappqkdesvg64pwg`
3. **Click:** Settings → Secrets
4. **Add this configuration:**

```toml
[gcp_service_account]
type = "service_account"
project_id = "festfusion-project"
private_key_id = "your_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@festfusion-project.iam.gserviceaccount.com"
client_id = "your_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40festfusion-project.iam.gserviceaccount.com"
```

## 🔄 **Step 3: Deploy Changes**

The code changes are already pushed to GitHub. Streamlit Cloud will automatically redeploy.

## ✅ **Step 4: Test**

1. **Visit your app:** https://fovrmlcxappqkdesvg64pwg.streamlit.app/
2. **Try uploading a file**
3. **Check if Google Sheets integration works**

## 🎯 **Expected Result**

- ✅ No more credential errors
- ✅ Google Sheets integration working
- ✅ File uploads working
- ✅ Data saved to your Google Drive and Sheets

---

**This will fix the Google Sheets integration immediately!** 🚀 