#!/usr/bin/env python3
"""
Streamlit Frontend for FestFusion with Ngrok API Integration
This version uses a Flask API exposed via ngrok for file uploads.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="FestFusion Telangana",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    color: #1f77b4;
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
}
.sub-header {
    text-align: center;
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def get_ngrok_url():
    """Get the ngrok URL from file"""
    try:
        with open('ngrok_url.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def upload_file_to_api(village, file, api_url):
    """Upload file to Flask API via ngrok"""
    try:
        # Prepare the file for upload
        files = {'file': (file.name, file.getvalue(), file.type)}
        data = {'village': village}
        
        # Upload to Flask API
        response = requests.post(f"{api_url}/upload", files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "saved_filename": result.get('saved_filename'),
                "original_filename": file.name,
                "file_size": len(file.getvalue()),
                "file_type": file.type,
                "village": village,
                "file_path": result.get('file_path'),
                "api_url": api_url
            }
        else:
            error_data = response.json()
            return {"error": error_data.get('error', 'Upload failed')}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return {"error": f"Upload error: {str(e)}"}

def save_to_sheets(village, original_filename, saved_filename, file_type, english_summary, telugu_summary, story_text="", language="", festival_name="", file_path=""):
    """Save data to Google Sheets"""
    try:
        # Import required modules
        from google.oauth2.service_account import Credentials
        import gspread
        
        # Get credentials
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Use Streamlit secrets for Streamlit Cloud deployment
        try:
            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scope
            )
        except Exception as e:
            # Fallback to local file for development
            try:
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                credentials_path = os.path.join(current_dir, "festfusion-project-cc628988dd80.json")
                creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
            except Exception as e2:
                st.error(f"Failed to load Google credentials: {e2}")
                return False
        
        client = gspread.authorize(creds)
        spreadsheet = client.open("FestFusion Data")
        worksheet = spreadsheet.sheet1
        
        # Check and fix headers
        try:
            current_headers = worksheet.row_values(1)
            correct_headers = [
                "timestamp",
                "file_name", 
                "district_name",
                "story[english summary]",
                "festival_name",
                "telugu summary",
                "file_location"
            ]
            
            if not current_headers or len(current_headers) < 7 or current_headers != correct_headers:
                worksheet.delete_rows(1)
                worksheet.insert_row(correct_headers, 1)
                
        except Exception as e:
            worksheet.clear()
            worksheet.append_row(correct_headers)
        
        # Prepare row data
        file_location = f"Local PC: {file_path}" if file_path else "Uploaded via API"
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            original_filename,
            village,
            english_summary,
            festival_name,
            telugu_summary,
            file_location
        ]
        
        # Write to sheet
        all_values = worksheet.get_all_values()
        next_row = len(all_values) + 1
        worksheet.insert_row(row_data, next_row)
        
        return True
        
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
        return False

def create_english_summary(festival_name, selected_village, story_text):
    """Create English summary using AI"""
    try:
        # Simple template-based summary for now
        summary = f"{festival_name} is a traditional festival celebrated in {selected_village} district of Telangana, India.\n\n"
        summary += "This festival holds great cultural and religious significance for the local community.\n\n"
        summary += "Traditional rituals, prayers, and community participation mark the celebrations.\n\n"
        summary += "This festival showcases Telangana's rich cultural heritage and strengthens community bonds.\n\n"
        summary += "Local traditions and religious practices are observed during this important celebration."
        
        if story_text:
            summary += f"\n\nPersonal story: {story_text[:200]}..."
        
        return summary
    except Exception as e:
        return f"Summary of {festival_name} festival in {selected_village}."

def create_telugu_summary(festival_name, selected_village):
    """Create Telugu summary"""
    try:
        telugu_summary = f"{festival_name} తెలంగాణలో జరుపుకునే సాంప్రదాయ పండుగ.\n\n"
        telugu_summary += "ఈ పండుగ స్థానిక సమాజానికి గొప్ప సాంస్కృతిక మరియు మత ప్రాముఖ్యతను కలిగి ఉంది.\n\n"
        telugu_summary += "సాంప్రదాయ ఆచారాలు, ఆరాధనలు మరియు సమాజ పాల్గొనేతో జరుపుకుంటారు.\n\n"
        telugu_summary += "ఈ పండుగ తెలంగాణ సంపన్న సాంస్కృతిక వారసత్వాన్ని ప్రదర్శిస్తుంది మరియు సమాజ బంధాలను బలపరుస్తుంది.\n\n"
        telugu_summary += "స్థానిక సంప్రదాయాలు మరియు మత ఆచారాలు ఈ ముఖ్యమైన వేడుకలో పాటించబడతాయి."
        
        return telugu_summary
    except Exception as e:
        return f"{festival_name} పండుగ గురించి తెలుగు సారాంశం."

def main():
    # Initialize session state
    if 'submission_complete' not in st.session_state:
        st.session_state.submission_complete = False
    if 'upload_data' not in st.session_state:
        st.session_state.upload_data = None
    if 'edited_english' not in st.session_state:
        st.session_state.edited_english = ""
    if 'edited_telugu' not in st.session_state:
        st.session_state.edited_telugu = ""
    
    # Header
    st.markdown('<h1 class="main-header">FestFusion Telangana</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Share a story about a local festival from your village</p>', unsafe_allow_html=True)
    
    # Check ngrok connection
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        st.error("❌ Ngrok tunnel not found. Please start the Flask API with ngrok first.")
        st.info("Run: `python ngrok_setup.py` to start the tunnel")
        return
    
    # Test API connection
    try:
        response = requests.get(f"{ngrok_url}/health", timeout=5)
        if response.status_code == 200:
            st.success(f"✅ Connected to Flask API via ngrok: {ngrok_url}")
        else:
            st.error("❌ Flask API is not responding")
            return
    except Exception as e:
        st.error(f"❌ Cannot connect to Flask API: {e}")
        st.info("Make sure the Flask API is running on port 5000")
        return
    
    # Get villages from API
    try:
        response = requests.get(f"{ngrok_url}/villages", timeout=5)
        if response.status_code == 200:
            villages = response.json()['villages']
        else:
            st.error("❌ Could not fetch villages from API")
            return
    except Exception as e:
        st.error(f"❌ Error fetching villages: {e}")
        return
    
    # Main form
    with st.form("upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_village = st.selectbox(
                "Select Your District/Village:",
                options=sorted(villages),
                help="Choose the district or village where your festival story takes place"
            )
            
            festival_name = st.text_input(
                "Festival Name:",
                placeholder="e.g., Bonalu, Bathukamma, Ugadi, etc.",
                help="Enter the name of the festival you're sharing about"
            )
            
            story_text = st.text_area(
                "Write your story here (optional):",
                height=150,
                placeholder="Share the details of the festival, its significance, traditions, and your personal experience...",
                help="Describe the festival, its cultural importance, and your personal connection to it"
            )
        
        with col2:
            st.markdown("### Upload Media File")
            st.markdown("**Supported formats:** Images (JPG, PNG), Videos (MP4), Audio (MP3, WAV), Documents (PDF, TXT)")
            
            uploaded_file = st.file_uploader(
                "Choose a file:",
                type=['jpg', 'jpeg', 'png', 'mp4', 'mp3', 'wav', 'pdf', 'txt'],
                help="Upload a photo, video, audio recording, or document related to the festival"
            )
            
            if uploaded_file:
                st.markdown("**File Details:**")
                st.write(f"**File selected:** {uploaded_file.name}")
                st.write(f"**File type:** {uploaded_file.type}")
                st.write(f"**File size:** {uploaded_file.size / 1024:.1f} KB")
        
        # Summary language selection
        summary_language = st.selectbox(
            "Summary Language:",
            options=["English & Telugu", "English Only", "Telugu Only"],
            help="Choose the language(s) for the AI-generated summary"
        )
        
        # Submit button
        submit_button = st.form_submit_button("Upload & Process", type="primary", use_container_width=True)
    
    # Handle form submission
    if submit_button and uploaded_file:
        if not festival_name:
            st.error("Please enter a festival name")
        elif not selected_village:
            st.error("Please select a district/village")
        else:
            with st.spinner("Uploading file to your PC..."):
                # Upload file to Flask API
                upload_result = upload_file_to_api(selected_village, uploaded_file, ngrok_url)
                
                if upload_result.get("success"):
                    st.success("✅ File uploaded successfully to your PC!")
                    
                    # Create summaries
                    english_summary = create_english_summary(festival_name, selected_village, story_text)
                    telugu_summary = create_telugu_summary(festival_name, selected_village)
                    
                    # Store data in session state
                    st.session_state.upload_data = {
                        **upload_result,
                        'festival_name': festival_name,
                        'story_text': story_text,
                        'english_summary': english_summary,
                        'telugu_summary': telugu_summary
                    }
                    st.session_state.edited_english = english_summary
                    st.session_state.edited_telugu = telugu_summary
                    st.session_state.submission_complete = True
                    st.rerun()
                else:
                    st.error(f"❌ Upload failed: {upload_result.get('error', 'Unknown error')}")
    
    # Display results if submission is complete
    if st.session_state.submission_complete and st.session_state.upload_data:
        st.markdown("---")
        st.markdown("### Upload Results")
        
        upload_data = st.session_state.upload_data
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### File Details")
            st.write(f"**Original Name:** {upload_data['original_filename']}")
            st.write(f"**Saved As:** {upload_data['saved_filename']}")
            st.write(f"**File Size:** {upload_data['file_size']} bytes")
            st.write(f"**District:** {upload_data.get('village', 'N/A')}")
            st.write(f"**Festival:** {upload_data.get('festival_name', 'N/A')}")
            st.write(f"**File Location:** {upload_data.get('file_path', 'Saved to your PC')}")
            
            if upload_data.get('story_text'):
                st.markdown("### Story Text")
                st.text_area("Your story:", upload_data['story_text'], height=100, disabled=True)
        
        with col2:
            st.markdown("### Edit Summaries")
            st.markdown("**You can edit the summaries below before saving to Google Sheets:**")
            
            # Editable English Summary
            st.markdown("**English Summary:**")
            edited_english = st.text_area(
                "Edit English Summary:",
                value=st.session_state.edited_english,
                height=120
            )
            
            # Editable Telugu Summary
            st.markdown("**తెలుగు సారాంశం:**")
            edited_telugu = st.text_area(
                "Edit Telugu Summary:",
                value=st.session_state.edited_telugu,
                height=120
            )
        
        # Save to Google Sheets
        st.markdown("---")
        st.markdown("### Save to Google Sheets")
        
        # Show preview
        st.markdown("**Preview of what will be saved:**")
        preview_col1, preview_col2 = st.columns(2)
        
        with preview_col1:
            st.markdown("**English Summary:**")
            st.info(edited_english)
        
        with preview_col2:
            st.markdown("**తెలుగు సారాంశం:**")
            st.success(edited_telugu)
        
        # Confirmation button
        if st.button("Confirm and Save to Google Sheets", type="primary", use_container_width=True):
            with st.spinner("Saving to Google Sheets..."):
                sheets_success = save_to_sheets(
                    village=upload_data.get('village', selected_village),
                    original_filename=upload_data["original_filename"],
                    saved_filename=upload_data["saved_filename"],
                    file_type=upload_data["file_type"],
                    english_summary=edited_english,
                    telugu_summary=edited_telugu,
                    story_text=upload_data.get('story_text', story_text),
                    language=summary_language,
                    festival_name=upload_data.get('festival_name', festival_name),
                    file_path=upload_data.get('file_path', '')
                )
            
            if sheets_success:
                st.success("✅ Successfully saved to Google Sheets!")
                st.markdown("### Database Status")
                st.write(f"**Saved to Sheets:** Success")
                st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Reset for new submission
                if st.button("Start New Submission", type="secondary", use_container_width=True):
                    st.session_state.submission_complete = False
                    st.session_state.upload_data = None
                    st.session_state.edited_english = ""
                    st.session_state.edited_telugu = ""
                    st.rerun()
            else:
                st.error("❌ Failed to save to Google Sheets. Please try again.")

if __name__ == "__main__":
    main() 