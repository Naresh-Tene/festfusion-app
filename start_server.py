#!/usr/bin/env python3
"""
FestFusion Server Startup Script
This script helps you start both the Flask API and Streamlit frontend
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask-cors', 'streamlit', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """Check if configuration is properly set up"""
    config_issues = []
    
    # Check if Google credentials file exists
    if not Path("festfusion-project-cc628988dd80.json").exists():
        config_issues.append("Google credentials file not found")
    
    # Check if config.py has placeholder values
    try:
        from config import GOOGLE_DRIVE_FOLDER_ID, GOOGLE_SHEET_NAME
        if GOOGLE_DRIVE_FOLDER_ID == "YOUR_GOOGLE_DRIVE_FOLDER_ID":
            config_issues.append("Google Drive Folder ID not configured")
        if GOOGLE_SHEET_NAME == "YOUR_GOOGLE_SHEET_NAME":
            config_issues.append("Google Sheet name not configured")
    except ImportError:
        config_issues.append("config.py not found or has errors")
    
    if config_issues:
        print("Configuration issues found:")
        for issue in config_issues:
            print(f"   - {issue}")
        print("\nPlease update config.py with your Google Drive and Sheets information.")
        return False
    
    return True

def wait_for_flask_api(url="http://localhost:5000", timeout=30):
    """Wait for Flask API to be ready"""
    print("Waiting for Flask API to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print("Flask API is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
    
    print("Flask API failed to start within timeout")
    return False

def start_flask_api():
    """Start the Flask API server"""
    print("Starting Flask API server...")
    
    try:
        # Start Flask API in a subprocess
        flask_process = subprocess.Popen([
            sys.executable, "flask_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for API to be ready
        if wait_for_flask_api():
            return flask_process
        else:
            flask_process.terminate()
            return None
            
    except Exception as e:
        print(f"Failed to start Flask API: {e}")
        return None

def start_streamlit():
    """Start the Streamlit frontend"""
    print("Starting Streamlit frontend...")
    
    try:
        # Start Streamlit in a subprocess
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_frontend.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
        print("Streamlit frontend started")
        print("Access the application at: http://localhost:8501")
        return streamlit_process
        
    except Exception as e:
        print(f"Failed to start Streamlit: {e}")
        return None

def main():
    """Main startup function"""
    print("FestFusion Telangana - Server Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        print("\nYou can still run the server, but Google Drive/Sheets features won't work.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Start Flask API
    flask_process = start_flask_api()
    if not flask_process:
        sys.exit(1)
    
    # Start Streamlit frontend
    streamlit_process = start_streamlit()
    if not streamlit_process:
        flask_process.terminate()
        sys.exit(1)
    
    print("\nBoth servers are running")
    print("Available URLs:")
    print("   - Streamlit Frontend: http://localhost:8501")
    print("   - Flask API: http://localhost:5000")
    print("   - API Health Check: http://localhost:5000/health")
    print("\nTo stop the servers, press Ctrl+C")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if flask_process.poll() is not None:
                print("Flask API process stopped unexpectedly")
                break
                
            if streamlit_process.poll() is not None:
                print("Streamlit process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        
        # Terminate processes
        if flask_process:
            flask_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
        
        print("Servers stopped successfully")

if __name__ == "__main__":
    main() 