"""
Google OAuth Configuration for FestFusion
This module handles OAuth 2.0 authentication for Google Drive uploads
"""

import streamlit as st
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import pickle
from pathlib import Path

# OAuth 2.0 scopes for Google Drive and Sheets
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_oauth_credentials():
    """
    Get OAuth credentials from Streamlit secrets or create new ones
    Returns: Credentials object for Google Drive API
    """
    creds = None
    
    # Check if we have stored credentials
    if 'google_credentials' in st.session_state:
        creds = st.session_state.google_credentials
        
        # If credentials are expired, refresh them
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                st.session_state.google_credentials = creds
            except Exception as e:
                st.error(f"Error refreshing credentials: {e}")
                creds = None
    
    # If no valid credentials, start OAuth flow
    if not creds:
        try:
            # Get OAuth config from Streamlit secrets
            oauth_config = get_oauth_config_from_secrets()
            
            if oauth_config:
                # Create flow from OAuth config
                flow = InstalledAppFlow.from_client_config(
                    oauth_config, 
                    SCOPES,
                    redirect_uri=oauth_config['web']['redirect_uris'][0]
                )
                
                # Run the OAuth flow
                creds = flow.run_local_server(port=0)
                st.session_state.google_credentials = creds
                
                st.success("✅ Successfully authenticated with Google Drive!")
                
            else:
                st.error("❌ OAuth configuration not found in Streamlit secrets")
                st.info("Please add your Google OAuth credentials to Streamlit Cloud secrets")
                return None
                
        except Exception as e:
            st.error(f"❌ Error during OAuth authentication: {e}")
            return None
    
    return creds

def get_oauth_config_from_secrets():
    """
    Get OAuth configuration from Streamlit secrets
    Returns: OAuth config dictionary or None
    """
    try:
        # Check if secrets are available
        if hasattr(st, 'secrets') and 'google_oauth' in st.secrets:
            oauth_secrets = st.secrets.google_oauth
            
            # Create OAuth config structure
            oauth_config = {
                "web": {
                    "client_id": oauth_secrets.client_id,
                    "client_secret": oauth_secrets.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [oauth_secrets.redirect_uri],
                    "scopes": SCOPES
                }
            }
            
            return oauth_config
        else:
            st.warning("⚠️ OAuth secrets not found. Please configure them in Streamlit Cloud.")
            return None
            
    except Exception as e:
        st.error(f"❌ Error reading OAuth secrets: {e}")
        return None

def upload_file_to_drive(file_path, filename, folder_id=None):
    """
    Upload a file to Google Drive using OAuth credentials
    
    Args:
        file_path (str): Path to the file to upload
        filename (str): Name for the file in Drive
        folder_id (str, optional): ID of the folder to upload to
    
    Returns:
        dict: File information from Google Drive or None if failed
    """
    try:
        # Get OAuth credentials
        creds = get_oauth_credentials()
        if not creds:
            st.error("❌ Could not get OAuth credentials")
            return None
        
        # Build the Drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Prepare file metadata
        file_metadata = {
            'name': filename,
        }
        
        # If folder_id is provided, set it as parent
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Create media upload object
        media = MediaFileUpload(file_path, resumable=True)
        
        # Upload the file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink,webContentLink'
        ).execute()
        
        st.success(f"✅ File uploaded successfully to Google Drive!")
        st.info(f"📁 File ID: {file.get('id')}")
        st.info(f"🔗 View Link: {file.get('webViewLink')}")
        
        return file
        
    except Exception as e:
        st.error(f"❌ Error uploading file to Google Drive: {e}")
        return None

def create_drive_folder(folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive
    
    Args:
        folder_name (str): Name of the folder to create
        parent_folder_id (str, optional): ID of the parent folder
    
    Returns:
        str: Folder ID or None if failed
    """
    try:
        # Get OAuth credentials
        creds = get_oauth_credentials()
        if not creds:
            st.error("❌ Could not get OAuth credentials")
            return None
        
        # Build the Drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Prepare folder metadata
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        # If parent folder is specified, set it
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        # Create the folder
        folder = service.files().create(
            body=folder_metadata,
            fields='id,name'
        ).execute()
        
        st.success(f"✅ Folder '{folder_name}' created successfully!")
        return folder.get('id')
        
    except Exception as e:
        st.error(f"❌ Error creating folder: {e}")
        return None

def list_drive_folders():
    """
    List all folders in Google Drive
    
    Returns:
        list: List of folder dictionaries or empty list if failed
    """
    try:
        # Get OAuth credentials
        creds = get_oauth_credentials()
        if not creds:
            st.error("❌ Could not get OAuth credentials")
            return []
        
        # Build the Drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Query for folders
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id,name,createdTime)"
        ).execute()
        
        folders = results.get('files', [])
        return folders
        
    except Exception as e:
        st.error(f"❌ Error listing folders: {e}")
        return []

def setup_oauth_instructions():
    """
    Display instructions for setting up OAuth in Streamlit Cloud
    """
    st.markdown("""
    ## 🔧 Google OAuth Setup Instructions
    
    ### Step 1: Create Google Cloud Project
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
    2. Create a new project or select existing one
    3. Enable Google Drive API
    
    ### Step 2: Create OAuth 2.0 Credentials
    1. Go to "APIs & Services" > "Credentials"
    2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
    3. Choose "Web application"
    4. Add authorized redirect URIs:
       - `https://your-app-name.streamlit.app/`
       - `http://localhost:8501/` (for local testing)
    5. Download the JSON file
    
    ### Step 3: Configure Streamlit Cloud Secrets
    1. Go to your Streamlit Cloud app settings
    2. Navigate to "Secrets"
    3. Add the following configuration:
    
    ```toml
    [google_oauth]
    client_id = "your_client_id_here"
    client_secret = "your_client_secret_here"
    redirect_uri = "https://your-app-name.streamlit.app/"
    ```
    
    ### Step 4: Deploy and Test
    Your app will now use OAuth 2.0 for Google Drive uploads!
    """) 