#!/usr/bin/env python3
"""
FestFusion Telangana - OAuth-Enabled Streamlit Frontend
This version uses OAuth 2.0 for secure Google Drive integration
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
from pathlib import Path
import tempfile
from google_oauth_config import (
    get_oauth_credentials, 
    upload_file_to_drive, 
    create_drive_folder,
    setup_oauth_instructions
)

# Page configuration
st.set_page_config(
    page_title="FestFusion Telangana",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎉 FestFusion Telangana</h1>
        <p>Preserving Telangana's Cultural Heritage Through AI-Powered Story Collection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("🔧 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["📤 Upload Stories", "🔐 OAuth Setup", "ℹ️ About"]
        )
    
    if page == "📤 Upload Stories":
        show_upload_page()
    elif page == "🔐 OAuth Setup":
        show_oauth_setup()
    elif page == "ℹ️ About":
        show_about_page()

def show_upload_page():
    """Show the main upload page"""
    
    st.markdown("""
    <div class="upload-section">
        <h2>📤 Upload Your Festival Story</h2>
        <p>Share your Telangana festival memories and help preserve our cultural heritage!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check OAuth status
    oauth_status = check_oauth_status()
    
    if not oauth_status:
        st.warning("⚠️ Google Drive integration not configured. Please set up OAuth in the sidebar.")
        show_basic_upload()
    else:
        show_oauth_upload()

def check_oauth_status():
    """Check if OAuth is properly configured"""
    try:
        # Check if secrets are available
        if hasattr(st, 'secrets') and 'google_oauth' in st.secrets:
            return True
        return False
    except:
        return False

def show_basic_upload():
    """Show basic upload without OAuth"""
    
    with st.form("story_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Village/District selection
            village = st.selectbox(
                "🏘️ Select Village/District:",
                [
                    "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", 
                    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", 
                    "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", 
                    "Mancherial", "Medak", "Medchal-Malkajgiri", "Nagarkurnool", "Nalgonda", 
                    "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", 
                    "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
                    "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri"
                ]
            )
            
            # Festival name
            festival_name = st.text_input("🎊 Festival Name:", placeholder="e.g., Bathukamma, Bonalu, Ugadi")
            
            # Story text
            story_text = st.text_area(
                "📖 Your Story:",
                placeholder="Share your festival memories, traditions, and experiences...",
                height=200
            )
        
        with col2:
            # File upload
            uploaded_file = st.file_uploader(
                "📎 Upload Media Files:",
                type=['jpg', 'jpeg', 'png', 'mp3', 'wav', 'mp4', 'pdf'],
                help="Upload images, audio, video, or documents related to your festival story"
            )
            
            # Contact information
            contact_email = st.text_input("📧 Contact Email (Optional):", placeholder="your.email@example.com")
            
            # Additional notes
            additional_notes = st.text_area(
                "📝 Additional Notes (Optional):",
                placeholder="Any additional information about your story...",
                height=100
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Story", type="primary")
        
        if submitted:
            if not story_text.strip():
                st.error("❌ Please provide a story description.")
                return
            
            if not village:
                st.error("❌ Please select a village/district.")
                return
            
            # Process the submission
            process_story_submission(village, festival_name, story_text, uploaded_file, contact_email, additional_notes)

def show_oauth_upload():
    """Show upload with OAuth Google Drive integration"""
    
    # OAuth status indicator
    st.success("✅ Google Drive integration is configured!")
    
    with st.form("oauth_story_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Village/District selection
            village = st.selectbox(
                "🏘️ Select Village/District:",
                [
                    "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", 
                    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", 
                    "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", 
                    "Mancherial", "Medak", "Medchal-Malkajgiri", "Nagarkurnool", "Nalgonda", 
                    "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", 
                    "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
                    "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri"
                ]
            )
            
            # Festival name
            festival_name = st.text_input("🎊 Festival Name:", placeholder="e.g., Bathukamma, Bonalu, Ugadi")
            
            # Story text
            story_text = st.text_area(
                "📖 Your Story:",
                placeholder="Share your festival memories, traditions, and experiences...",
                height=200
            )
        
        with col2:
            # File upload
            uploaded_file = st.file_uploader(
                "📎 Upload Media Files:",
                type=['jpg', 'jpeg', 'png', 'mp3', 'wav', 'mp4', 'pdf'],
                help="Upload images, audio, video, or documents related to your festival story"
            )
            
            # Contact information
            contact_email = st.text_input("📧 Contact Email (Optional):", placeholder="your.email@example.com")
            
            # Additional notes
            additional_notes = st.text_area(
                "📝 Additional Notes (Optional):",
                placeholder="Any additional information about your story...",
                height=100
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Story & Upload to Drive", type="primary")
        
        if submitted:
            if not story_text.strip():
                st.error("❌ Please provide a story description.")
                return
            
            if not village:
                st.error("❌ Please select a village/district.")
                return
            
            # Process the submission with OAuth
            process_oauth_story_submission(village, festival_name, story_text, uploaded_file, contact_email, additional_notes)

def process_story_submission(village, festival_name, story_text, uploaded_file, contact_email, additional_notes):
    """Process story submission without OAuth"""
    
    with st.spinner("🔄 Processing your story..."):
        try:
            # Create story data
            story_data = {
                "village": village,
                "festival_name": festival_name or "Unnamed Festival",
                "story_text": story_text,
                "contact_email": contact_email,
                "additional_notes": additional_notes,
                "timestamp": datetime.now().isoformat(),
                "file_uploaded": uploaded_file is not None
            }
            
            # Save story data locally
            save_story_locally(story_data, uploaded_file)
            
            st.success("✅ Your story has been submitted successfully!")
            st.info("📝 Story saved locally. Google Drive upload requires OAuth setup.")
            
            # Show summary
            show_story_summary(story_data)
            
        except Exception as e:
            st.error(f"❌ Error processing submission: {e}")

def process_oauth_story_submission(village, festival_name, story_text, uploaded_file, contact_email, additional_notes):
    """Process story submission with OAuth Google Drive upload"""
    
    with st.spinner("🔄 Processing your story and uploading to Google Drive..."):
        try:
            # Create story data
            story_data = {
                "village": village,
                "festival_name": festival_name or "Unnamed Festival",
                "story_text": story_text,
                "contact_email": contact_email,
                "additional_notes": additional_notes,
                "timestamp": datetime.now().isoformat(),
                "file_uploaded": uploaded_file is not None
            }
            
            # Save story data locally
            save_story_locally(story_data, uploaded_file)
            
            # Upload to Google Drive if file is provided
            if uploaded_file:
                upload_to_google_drive(story_data, uploaded_file)
            
            st.success("✅ Your story has been submitted and uploaded to Google Drive!")
            
            # Show summary
            show_story_summary(story_data)
            
        except Exception as e:
            st.error(f"❌ Error processing submission: {e}")

def save_story_locally(story_data, uploaded_file):
    """Save story data and file locally"""
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Save uploaded file if provided
    if uploaded_file:
        file_path = upload_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        story_data["local_file_path"] = str(file_path)
    
    # Save story data as JSON
    story_file = upload_dir / f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(story_file, "w", encoding="utf-8") as f:
        json.dump(story_data, f, indent=2, ensure_ascii=False)

def upload_to_google_drive(story_data, uploaded_file):
    """Upload file to Google Drive using OAuth"""
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Create folder structure in Drive
        village_folder_name = f"FestFusion_{story_data['village']}"
        festival_folder_name = f"{story_data['festival_name']}_{datetime.now().strftime('%Y%m%d')}"
        
        # Upload file to Drive
        filename = f"{festival_folder_name}_{uploaded_file.name}"
        drive_file = upload_file_to_drive(tmp_file_path, filename)
        
        if drive_file:
            st.info(f"📁 File uploaded to Google Drive: {drive_file.get('webViewLink')}")
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
    except Exception as e:
        st.error(f"❌ Error uploading to Google Drive: {e}")

def show_story_summary(story_data):
    """Show a summary of the submitted story"""
    
    st.markdown("### 📋 Story Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**🏘️ Village/District:** {story_data['village']}")
        st.write(f"**🎊 Festival:** {story_data['festival_name']}")
        st.write(f"**📅 Submitted:** {story_data['timestamp']}")
    
    with col2:
        st.write(f"**📧 Contact:** {story_data['contact_email'] or 'Not provided'}")
        st.write(f"**📎 File Uploaded:** {'✅ Yes' if story_data['file_uploaded'] else '❌ No'}")
        st.write(f"**📝 Story Length:** {len(story_data['story_text'])} characters")

def show_oauth_setup():
    """Show OAuth setup instructions"""
    
    st.title("🔐 Google OAuth Setup")
    
    if check_oauth_status():
        st.success("✅ OAuth is already configured!")
        st.info("Your Google Drive integration is ready to use.")
    else:
        st.warning("⚠️ OAuth not configured yet.")
        setup_oauth_instructions()

def show_about_page():
    """Show about page"""
    
    st.title("ℹ️ About FestFusion Telangana")
    
    st.markdown("""
    ## 🎉 Welcome to FestFusion Telangana!
    
    **FestFusion Telangana** is an AI-powered platform dedicated to preserving and celebrating 
    the rich cultural heritage of Telangana's festivals through digital story collection and archiving.
    
    ### 🌟 Our Mission
    
    We believe that every festival story is a precious piece of our cultural tapestry. 
    Our mission is to:
    
    - 📚 **Collect and preserve** festival stories from across Telangana
    - 🤖 **Use AI technology** to summarize and organize cultural content
    - 🌐 **Create a digital archive** accessible to future generations
    - 🎊 **Celebrate diversity** in Telangana's festival traditions
    
    ### 🔧 How It Works
    
    1. **📤 Story Submission**: Users upload festival stories with text and media files
    2. **🎯 AI Processing**: Our AI models summarize and categorize the content
    3. **☁️ Secure Storage**: Files are safely stored in Google Drive
    4. **📊 Data Organization**: Stories are organized by village/district
    5. **🔍 Easy Access**: Searchable archive for researchers and enthusiasts
    
    ### 🛡️ Privacy & Security
    
    - All uploads are secure and private
    - OAuth 2.0 authentication ensures safe Google Drive access
    - User data is protected and never shared without permission
    - Files are stored securely in Google Cloud
    
    ### 🎯 Supported Festivals
    
    We welcome stories from all Telangana festivals, including:
    
    - **Bathukamma** - The flower festival
    - **Bonalu** - The mother goddess festival
    - **Ugadi** - Telugu New Year
    - **Sankranti** - Harvest festival
    - **Vinayaka Chavithi** - Ganesh festival
    - **And many more...**
    
    ### 📞 Contact Us
    
    For questions, suggestions, or support, please reach out to us through the contact form.
    
    ---
    
    **Thank you for helping preserve Telangana's cultural heritage!** 🙏
    """)

if __name__ == "__main__":
    main() 