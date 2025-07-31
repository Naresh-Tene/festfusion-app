# Ngrok + Flask API Setup Guide

## Overview
This guide will help you set up ngrok to expose your local Flask API to the internet, allowing your Streamlit Cloud app to upload files directly to your PC.

## 🎯 **Benefits of this approach:**
- ✅ **Files saved directly to your PC** - No storage quota limits
- ✅ **Organized by village/district** - Easy file management
- ✅ **Permanent storage** - Files stay on your computer
- ✅ **No Google Drive dependency** - Works independently
- ✅ **Real-time access** - Files available immediately

## 📋 **Prerequisites:**
1. Python 3.7+ installed
2. Flask API running locally
3. ngrok account (free tier available)

## 🚀 **Step 1: Install ngrok**

### **Windows:**
```bash
# Option 1: Using winget
winget install ngrok

# Option 2: Manual download
# 1. Go to https://ngrok.com/download
# 2. Download Windows version
# 3. Extract to a folder
# 4. Add folder to PATH environment variable
```

### **Linux/Mac:**
```bash
# Install via package manager
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

## 🔧 **Step 2: Set up ngrok account**

1. **Sign up at [ngrok.com](https://ngrok.com)** (free tier available)
2. **Get your authtoken** from the dashboard
3. **Authenticate ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
   ```

## 🏃‍♂️ **Step 3: Start the Flask API**

```bash
# Start the Flask API on port 5000
python flask_api.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## 🌐 **Step 4: Start ngrok tunnel**

### **Option A: Using the setup script**
```bash
python ngrok_setup.py
```

### **Option B: Manual ngrok command**
```bash
ngrok http 5000
```

You'll see output like:
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

## 📱 **Step 5: Use the ngrok-enabled Streamlit app**

### **For local development:**
```bash
streamlit run streamlit_ngrok_frontend.py
```

### **For Streamlit Cloud deployment:**
1. Update your Streamlit Cloud app to use `streamlit_ngrok_frontend.py`
2. Make sure the ngrok URL is accessible from Streamlit Cloud

## 🔄 **Step 6: Keep the tunnel running**

**Important:** Keep the ngrok terminal window open to maintain the tunnel.

## 📁 **File Organization**

Files will be saved to your PC in this structure:
```
uploads/
├── Adilabad/
│   ├── 20250130_143022_festival1.jpg
│   └── 20250130_143045_festival2.mp4
├── Hyderabad/
│   └── 20250130_143100_festival3.pdf
└── Hanamkonda/
    └── 20250130_143115_festival4.mp3
```

## 🔍 **Monitoring**

### **Ngrok Dashboard:**
- Visit `http://localhost:4040` to see traffic and requests
- Monitor file uploads in real-time

### **File System:**
- Check the `uploads/` folder for new files
- Files are organized by village/district

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **"Ngrok tunnel not found"**
   - Make sure ngrok is running
   - Check that `ngrok_url.txt` file exists

2. **"Cannot connect to Flask API"**
   - Ensure Flask API is running on port 5000
   - Check firewall settings

3. **"Upload failed"**
   - Check ngrok tunnel status
   - Verify Flask API is responding

4. **"File not saved"**
   - Check `uploads/` folder permissions
   - Ensure village folder can be created

### **Debug Commands:**
```bash
# Test Flask API locally
curl http://localhost:5000/health

# Test ngrok tunnel
curl https://your-ngrok-url.ngrok.io/health

# Check file uploads
ls -la uploads/
```

## 🔒 **Security Considerations**

1. **Ngrok URLs are public** - Anyone with the URL can access your API
2. **Consider authentication** for production use
3. **Monitor ngrok dashboard** for suspicious activity
4. **Use HTTPS** (ngrok provides this automatically)

## 📊 **Performance Tips**

1. **Keep ngrok running** - Restarting creates new URLs
2. **Monitor file sizes** - Large files may timeout
3. **Check disk space** - Files accumulate on your PC
4. **Regular cleanup** - Archive old files as needed

## 🎉 **Success Indicators**

✅ **Ngrok tunnel active** - Shows "online" status
✅ **Flask API responding** - Health check returns 200
✅ **Files appearing** - Check `uploads/` folder
✅ **Google Sheets updated** - Data saved with file paths

## 🔄 **Daily Workflow**

1. **Start Flask API:** `python flask_api.py`
2. **Start ngrok:** `python ngrok_setup.py`
3. **Use Streamlit app** - Files upload to your PC
4. **Monitor uploads** - Check `uploads/` folder
5. **Keep running** - Don't close ngrok terminal

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section
2. Verify all services are running
3. Check ngrok dashboard for errors
4. Monitor Flask API logs

Your setup is complete when files upload successfully to your PC! 🚀 