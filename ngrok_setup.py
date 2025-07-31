#!/usr/bin/env python3
"""
Ngrok Setup for FestFusion Flask API
This script helps you expose your local Flask API to the internet using ngrok.
"""

import subprocess
import requests
import time
import json
import os
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ngrok is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ngrok is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Ngrok is not installed")
        return False

def install_ngrok():
    """Install ngrok if not present"""
    print("📥 Installing ngrok...")
    
    # For Windows
    if os.name == 'nt':
        print("Please download ngrok from: https://ngrok.com/download")
        print("Extract it to a folder and add that folder to your PATH")
        print("Or run: winget install ngrok")
        return False
    
    # For Linux/Mac
    else:
        try:
            subprocess.run(['curl', '-s', 'https://ngrok-agent.s3.amazonaws.com/ngrok.asc', '|', 'sudo', 'tee', '/etc/apt/trusted.gpg.d/ngrok.asc', '>', '/dev/null'], shell=True)
            subprocess.run(['echo', '"deb https://ngrok-agent.s3.amazonaws.com buster main"', '|', 'sudo', 'tee', '/etc/apt/sources.list.d/ngrok.list'], shell=True)
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', 'ngrok'], check=True)
            print("✅ Ngrok installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install ngrok automatically")
            print("Please install manually from: https://ngrok.com/download")
            return False

def start_ngrok(port=5000):
    """Start ngrok tunnel"""
    print(f"🚀 Starting ngrok tunnel on port {port}...")
    
    try:
        # Start ngrok process
        process = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()['tunnels']
            
            if tunnels:
                public_url = tunnels[0]['public_url']
                print(f"✅ Ngrok tunnel started successfully!")
                print(f"🌐 Public URL: {public_url}")
                print(f"📊 Ngrok dashboard: http://localhost:4040")
                
                # Save the URL to a file for the Streamlit app to use
                with open('ngrok_url.txt', 'w') as f:
                    f.write(public_url)
                
                print(f"💾 URL saved to ngrok_url.txt")
                return public_url, process
            else:
                print("❌ No tunnels found")
                process.terminate()
                return None, None
                
        except requests.exceptions.RequestException:
            print("❌ Could not get ngrok tunnel info")
            process.terminate()
            return None, None
            
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None, None

def stop_ngrok(process):
    """Stop ngrok tunnel"""
    if process:
        print("🛑 Stopping ngrok tunnel...")
        process.terminate()
        process.wait()
        print("✅ Ngrok tunnel stopped")

def main():
    """Main function"""
    print("🏛️ FestFusion - Ngrok Setup")
    print("=" * 50)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        install_choice = input("Would you like to install ngrok? (y/n): ")
        if install_choice.lower() == 'y':
            if not install_ngrok():
                return
        else:
            print("Please install ngrok manually and run this script again")
            return
    
    # Start ngrok tunnel
    public_url, process = start_ngrok(5000)
    
    if public_url:
        print("\n🎉 Setup complete!")
        print(f"Your Flask API is now accessible at: {public_url}")
        print("\n📋 Next steps:")
        print("1. Update your Streamlit app to use this URL")
        print("2. Keep this terminal open to maintain the tunnel")
        print("3. Press Ctrl+C to stop the tunnel when done")
        
        try:
            # Keep the process running
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
            stop_ngrok(process)
    else:
        print("❌ Failed to start ngrok tunnel")

if __name__ == "__main__":
    main() 