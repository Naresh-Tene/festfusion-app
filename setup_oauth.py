#!/usr/bin/env python3
"""
OAuth Setup Helper Script for FestFusion
This script helps you configure OAuth credentials for Streamlit Cloud
"""

import json
import os
from pathlib import Path

def main():
    """Main setup function"""
    
    print("🔐 FestFusion OAuth Setup Helper")
    print("=" * 50)
    
    # Your OAuth credentials (from the JSON you provided)
    oauth_config = {
        "web": {
            "client_id": "26082816180-vmgb2pfbmtl03gufnnuabsmiq7rcp14r.apps.googleusercontent.com",
            "project_id": "festfusion-project",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "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",
            "javascript_origins": ["https://fovrmlcxappqkdesvg64pwg.streamlit.app"]
        }
    }
    
    print("\n📋 Your OAuth Configuration:")
    print(f"   Client ID: {oauth_config['web']['client_id']}")
    print(f"   Project ID: {oauth_config['web']['project_id']}")
    print(f"   Redirect URI: https://fovrmlcxappqkdesvg64pwg.streamlit.app/")
    
    print("\n🔧 Next Steps:")
    print("1. Go to your Streamlit Cloud app settings")
    print("2. Navigate to 'Secrets'")
    print("3. Add the following configuration:")
    
    print("\n" + "=" * 50)
    print("COPY THIS TO STREAMLIT CLOUD SECRETS:")
    print("=" * 50)
    
    # Generate TOML configuration for Streamlit Cloud
    toml_config = f"""[google_oauth]
client_id = "{oauth_config['web']['client_id']}"
client_secret = "{oauth_config['web']['client_secret']}"
redirect_uri = "https://fovrmlcxappqkdesvg64pwg.streamlit.app/"
project_id = "{oauth_config['web']['project_id']}"
"""
    
    print(toml_config)
    print("=" * 50)
    
    # Create local secrets file for development
    create_local_secrets(toml_config)
    
    print("\n✅ Setup Complete!")
    print("\n📝 What to do next:")
    print("1. Copy the TOML configuration above to Streamlit Cloud Secrets")
    print("2. Run: streamlit run streamlit_oauth_frontend.py")
    print("3. Your app will now use OAuth 2.0 for Google Drive uploads!")
    
    print("\n🔒 Security Note:")
    print("Your credentials are now secure and will work with both local development and Streamlit Cloud.")

def create_local_secrets(toml_config):
    """Create local secrets file for development"""
    
    # Create .streamlit directory
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create secrets.toml file
    secrets_file = streamlit_dir / "secrets.toml"
    
    with open(secrets_file, "w") as f:
        f.write(toml_config)
    
    print(f"\n📁 Created local secrets file: {secrets_file}")
    print("   This file is already in .gitignore and won't be uploaded to GitHub.")

if __name__ == "__main__":
    main() 