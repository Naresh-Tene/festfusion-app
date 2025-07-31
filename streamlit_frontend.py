import streamlit as st
import os
import tempfile
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import requests
import json
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
# transformers import removed - using template-based summaries instead

# Configuration
# FLASK_API_URL removed - using standalone mode for Streamlit Cloud deployment

# Page configuration
st.set_page_config(
    page_title="FestFusion Telangana - Updated",
    page_icon="",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
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
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API functions removed - using hardcoded data for Streamlit Cloud deployment

# Template-based summary functions (no AI models needed)
def create_english_summary(festival_name, selected_village, story_text):
    """Creates a clean 5-line English summary using templates"""
    return f"""{festival_name} is a traditional festival celebrated in {selected_village} district of Telangana, India.

This festival holds great cultural and religious significance for the local community.

Traditional rituals, prayers, and community participation mark the celebrations.

This festival showcases Telangana's rich cultural heritage and strengthens community bonds.

Local traditions and religious practices are observed during this important celebration."""

def create_telugu_summary(festival_name, selected_village):
    """Creates a clean 5-line Telugu summary using templates"""
    return f"""{festival_name} తెలంగాణలో {selected_village} జిల్లాలో జరుపుకునే సాంప్రదాయ పండుగ.

ఈ పండుగ స్థానిక సమాజానికి గొప్ప సాంస్కృతిక మరియు మత ప్రాముఖ్యతను కలిగి ఉంది.

సాంప్రదాయ ఆచారాలు, ఆరాధనలు మరియు సమాజ పాల్గొనేతో జరుపుకుంటారు.

ఈ పండుగ తెలంగాణ సంపన్న సాంస్కృతిక వారసత్వాన్ని ప్రదర్శిస్తుంది మరియు సమాజ బంధాలను బలపరుస్తుంది.

స్థానిక సంప్రదాయాలు మరియు మత ఆచారాలు ఈ ముఖ్యమైన వేడుకలో పాటించబడతాయి."""

# Comprehensive Telugu translation dictionary for festival terms
TELUGU_TRANSLATIONS = {
    "festival": "పండుగ",
    "celebration": "సంబరం",
    "traditional": "సాంప్రదాయిక",
    "cultural": "సాంస్కృతిక",
    "significance": "ప్రాముఖ్యత",
    "importance": "ముఖ్యత",
    "district": "జిల్లా",
    "village": "గ్రామం",
    "region": "ప్రాంతం",
    "telangana": "తెలంగాణ",
    "india": "భారతదేశం",
    "celebrated": "జరుపుకుంటారు",
    "celebrating": "జరుపుకుంటున్న",
    "traditions": "సంప్రదాయాలు",
    "customs": "ఆచారాలు",
    "religious": "మతపరమైన",
    "spiritual": "ఆధ్యాత్మిక",
    "heritage": "మార్గదర్శకత్వం",
    "culture": "సంస్కృతి",
    "local": "స్థానిక",
    "community": "సమాజం",
    "people": "ప్రజలు",
    "family": "కుటుంబం",
    "temple": "దేవాలయం",
    "god": "దేవుడు",
    "goddess": "దేవి",
    "prayer": "ప్రార్థన",
    "worship": "పూజ",
    "ceremony": "వేడుక",
    "ritual": "కర్మకాండ",
    "offering": "నైవేద్యం",
    "blessing": "ఆశీర్వాదం",
    "auspicious": "శుభకరమైన",
    "sacred": "పవిత్రమైన",
    "holy": "పవిత్రమైన",
    "divine": "దైవికమైన",
    "ancient": "ప్రాచీనమైన",
    "historical": "చారిత్రకమైన",
    "centuries": "శతాబ్దాలు",
    "generations": "తరాలు",
    "ancestors": "పూర్వీకులు",
    "elders": "ముసలివారు",
    "youth": "యువత",
    "children": "పిల్లలు",
    "women": "మహిళలు",
    "men": "పురుషులు",
    "dance": "నృత్యం",
    "music": "సంగీతం",
    "song": "పాట",
    "drum": "డోలు",
    "bell": "గంట",
    "flower": "పువ్వు",
    "incense": "ధూపం",
    "lamp": "దీపం",
    "candle": "మొమ్మ",
    "food": "ఆహారం",
    "sweet": "మిఠాయి",
    "rice": "బియ్యం",
    "milk": "పాలు",
    "honey": "తేనె",
    "coconut": "కొబ్బరి",
    "banana": "అరటి",
    "mango": "మామిడి",
    "color": "రంగు",
    "red": "ఎరుపు",
    "yellow": "పసుపు",
    "orange": "నారింజ",
    "green": "పచ్చ",
    "blue": "నీలం",
    "white": "తెలుపు",
    "gold": "బంగారం",
    "silver": "వెండి",
    "beautiful": "అందమైన",
    "wonderful": "అద్భుతమైన",
    "amazing": "ఆశ్చర్యకరమైన",
    "special": "ప్రత్యేకమైన",
    "unique": "అనూహ్యమైన",
    "famous": "ప్రసిద్ధమైన",
    "popular": "జనాదరణ పొందిన",
    "important": "ముఖ్యమైన",
    "essential": "అవసరమైన",
    "necessary": "అవసరమైన",
    "valuable": "విలువైన",
    "precious": "విలువైన",
    "this": "ఇది",
    "is": "ఉంది",
    "a": "ఒక",
    "in": "లో",
    "of": "యొక్క",
    "the": "",
    "with": "తో",
    "and": "మరియు",
    "or": "లేదా",
    "for": "కోసం",
    "to": "కు",
    "from": "నుండి",
    "by": "ద్వారా",
    "at": "వద్ద",
    "on": "పై",
    "about": "గురించి",
    "detailed": "వివరమైన",
    "summary": "సారాంశం",
    "please": "దయచేసి",
    "provide": "ఇవ్వండి",
    "festival's": "పండుగ యొక్క",
    "traditions and": "సంప్రదాయాలు మరియు",
    "cultural importance": "సాంస్కృతిక ముఖ్యత",
    "hyderabad": "హైదరాబాద్",
    "bonalu": "బోనాలు",
    "bathukamma": "బతుకమ్మ",
    "ugadi": "ఉగాది",
    "sankranti": "సంక్రాంతి",
    "dasara": "దసరా",
    "diwali": "దీపావళి",
    "holi": "హోళీ",
    "ramzan": "రంజాన్",
    "christmas": "క్రిస్మస్"
}

# Translation function removed - using template-based Telugu summaries instead

# Google Services Connection
@st.cache_resource
def get_creds():
    """Gets the credentials to connect to Google services using local JSON files."""
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Try to use local JSON files first (for development)
    try:
        # Check for service account JSON file
        service_account_path = "festfusion-project-cc628988dd80.json"
        if os.path.exists(service_account_path):
            creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
            return creds
    except Exception as e:
        st.warning(f"Local service account file not found: {e}")
    
    # Fallback to Streamlit secrets (for cloud deployment)
    try:
        if 'gcp_service_account' in st.secrets:
            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scope
            )
            return creds
        else:
            st.warning("Service account not configured in Streamlit secrets")
            return None
    except Exception as e:
        st.error(f"Failed to load Google credentials: {e}")
        return None

def save_to_sheets(village, original_filename, saved_filename, file_type, english_summary, telugu_summary, story_text="", language="", festival_name="", google_drive_link=""):
    """Save data to Google Sheets using user-edited summaries"""
    try:
        print(f"Debug - Starting save_to_sheets function")
        creds = get_creds()
        
        if creds is None:
            st.error("Google credentials not available. Please check your Streamlit secrets configuration.")
            return False
            
        client = gspread.authorize(creds)
        
        print(f"Debug - Connected to Google Sheets")
        spreadsheet = client.open("FestFusion Data")
        worksheet = spreadsheet.sheet1
        print(f"Debug - Opened worksheet: {worksheet.title}")
        
        # Check current headers and fix if needed
        try:
            current_headers = worksheet.row_values(1)
            print(f"Debug - Current headers: {current_headers}")
            
            correct_headers = [
                "timestamp",
                "file_name", 
                "district_name",
                "story[english summary]",
                "festival_name",
                "telugu summary"
            ]
            
            # Only fix headers if they're wrong
            if not current_headers or len(current_headers) < 7 or current_headers != correct_headers:
                print(f"Debug - Fixing headers")
                # Delete only the first row and insert correct headers
                worksheet.delete_rows(1)
                worksheet.insert_row(correct_headers, 1)
                print(f"Debug - Headers fixed: {correct_headers}")
            else:
                print(f"Debug - Headers are already correct")
                
        except Exception as e:
            print(f"Debug - Error checking/fixing headers: {e}")
            # If there's an error, reset the sheet completely
            worksheet.clear()
            correct_headers = [
                "timestamp",
                "file_name", 
                "district_name",
                "story[english summary]",
                "festival_name",
                "telugu summary",
                "google_drive_link"
            ]
            worksheet.append_row(correct_headers)
            print(f"Debug - Sheet reset with headers: {correct_headers}")
        
        # Convert to list format to ensure proper column order
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            original_filename,
            village,
            english_summary,
            festival_name,
            telugu_summary,
            google_drive_link
        ]
        
        # Debug: Print the data being saved
        print(f"Debug - Saving to Google Sheets:")
        print(f"Row data: {row_data}")
        
        # Write data to the next row
        try:
            # Get all values to find the next empty row
            all_values = worksheet.get_all_values()
            next_row = len(all_values) + 1
            print(f"Debug - Writing to row {next_row}")
            
            # Insert the row at the correct position
            worksheet.insert_row(row_data, next_row)
            print(f"Debug - Row inserted successfully at row {next_row}")
            
            # Verify the data was written
            try:
                written_row = worksheet.row_values(next_row)
                print(f"Debug - Verified row {next_row}: {written_row}")
            except Exception as e:
                print(f"Debug - Could not verify row: {e}")
            
        except Exception as e:
            print(f"Debug - Error writing data: {e}")
            # Fallback to append
            worksheet.append_row(row_data)
            print(f"Debug - Row appended as fallback")
        
        return True
    except Exception as e:
        print(f"Debug - Error in save_to_sheets: {e}")
        st.error(f"Error saving to Google Sheets: {e}")
        return False

def upload_file(village, file):
    """Handles file upload - saves locally and uploads to Google Drive."""
    try:
        # Prepare file metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.name}"
        file_bytes = file.getvalue()
        
        # Try local storage first (works on local machine)
        file_path = ""
        storage_type = "session"
        storage_message = "File uploaded successfully"
        google_drive_link = ""
        
        try:
            # Create uploads directory if it doesn't exist
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            # Create village-specific subdirectory
            village_dir = upload_dir / village
            village_dir.mkdir(exist_ok=True)
            
            # Save file locally
            file_path = village_dir / filename
            with open(file_path, "wb") as f:
                f.write(file_bytes)
            
            storage_type = "local"
            storage_message = f"File saved locally: {file_path}"
            
        except Exception as local_error:
            # Local storage failed (probably on Streamlit Cloud)
            # Store file in session state for temporary access
            if 'uploaded_files' not in st.session_state:
                st.session_state.uploaded_files = {}
            
            st.session_state.uploaded_files[filename] = {
                'bytes': file_bytes,
                'type': file.type,
                'village': village,
                'timestamp': timestamp
            }
            
            storage_type = "session"
            storage_message = f"File stored in session (temporary): {filename}"
        
        # Try to upload to Google Drive
        try:
            creds = get_creds()
            if creds:
                # Build Drive service
                drive_service = build('drive', 'v3', credentials=creds)
                
                # Create folder structure in Drive
                folder_name = f"FestFusion_Uploads/{village}"
                
                # Check if folder exists, create if not
                folder_query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
                folder_results = drive_service.files().list(q=folder_query).execute()
                
                if folder_results['files']:
                    folder_id = folder_results['files'][0]['id']
                else:
                    # Create folder
                    folder_metadata = {
                        'name': folder_name,
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
                    folder_id = folder['id']
                
                # Upload file to Drive
                file_metadata = {
                    'name': filename,
                    'parents': [folder_id]
                }
                
                media = MediaIoBaseUpload(
                    io.BytesIO(file_bytes),
                    mimetype=file.type,
                    resumable=True
                )
                
                file_drive = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,webViewLink'
                ).execute()
                
                google_drive_link = file_drive.get('webViewLink', '')
                storage_message += f" | Uploaded to Google Drive: {google_drive_link}"
                
        except Exception as drive_error:
            # Google Drive upload failed, but local upload succeeded
            storage_message += f" | Google Drive upload failed: {str(drive_error)}"
        
        return {
            "success": True,
            "saved_filename": filename,
            "original_filename": file.name,
            "file_size": len(file_bytes),
            "file_type": file.type,
            "village": village,
            "file_path": str(file_path) if file_path else "",
            "google_drive_link": google_drive_link,
            "storage_type": storage_type
        }
        
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return {"error": f"Upload error: {str(e)}"}

def translate_english_to_telugu(english_text):
    """Creates Telugu summary based on English text using smart template."""
    try:
        # Extract key information from English text
        lines = english_text.split('\n')
        festival_info = lines[0] if lines else english_text
        
        # Create smart Telugu template based on English content
        telugu_summary = f"""{festival_info.split(' is ')[0] if ' is ' in festival_info else 'పండుగ'} తెలంగాణలో జరుపుకునే సాంప్రదాయ పండుగ.

ఈ పండుగ స్థానిక సమాజానికి గొప్ప సాంస్కృతిక మరియు మత ప్రాముఖ్యతను కలిగి ఉంది.

సాంప్రదాయ ఆచారాలు, ఆరాధనలు మరియు సమాజ పాల్గొనేతో జరుపుకుంటారు.

ఈ పండుగ తెలంగాణ సంపన్న సాంస్కృతిక వారసత్వాన్ని ప్రదర్శిస్తుంది మరియు సమాజ బంధాలను బలపరుస్తుంది.

స్థానిక సంప్రదాయాలు మరియు మత ఆచారాలు ఈ ముఖ్యమైన వేడుకలో పాటించబడతాయి."""
        return telugu_summary
    except Exception as e:
        # Fallback to simple template
        return f"తెలుగు అనువాదం: {english_text}"

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
    if 'form_data_persistent' not in st.session_state:
        st.session_state.form_data_persistent = False
    
    # Header
    st.markdown('<h1 class="main-header">FestFusion Telangana</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Share a story about a local festival from your village</p>', unsafe_allow_html=True)
    
    # Get villages list (hardcoded for Streamlit Cloud deployment)
    villages = [
        "Adilabad", "Bhadradri Kothagudem", "Hanamkonda", "Hyderabad", 
        "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", 
        "Kamareddy", "Karimnagar", "Khammam", "Kumuram Bheem Asifabad", 
        "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", "Medchal–Malkajgiri", 
        "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", 
        "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", 
        "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
        "Warangal", "Yadadri Bhuvanagiri"
    ]
    
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
                help="Describe the festival, its cultural importance, and your connection to it"
            )
            
            # Language preference for summary
            summary_language = st.selectbox(
                "Summary Language:",
                options=["English & Telugu", "English Only", "Telugu Only"],
                help="Choose the language(s) for AI-generated summary"
            )
        
        with col2:
            uploaded_file = st.file_uploader(
                "Upload your file:",
                type=['png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4', 'txt', 'pdf'],
                help="Upload images, audio recordings, videos, or text files related to your festival story"
            )
            
            if uploaded_file:
                st.info(f"File selected: {uploaded_file.name}")
                st.write(f"File type: {uploaded_file.type}")
                st.write(f"File size: {uploaded_file.size / 1024:.1f} KB")
        
        # Submit button
        submit_button = st.form_submit_button(
            "Upload & Process",
            type="primary",
            use_container_width=True
        )
    
    # Process form submission
    if submit_button:
        # Clear previous submission data when starting new submission
        st.session_state.submission_complete = False
        st.session_state.upload_data = None
        st.session_state.form_data_persistent = False
        st.session_state.edited_english = ""
        st.session_state.edited_telugu = ""
        
        if not selected_village:
            st.error("Please select a village/district")
            return
        
        if not festival_name:
            st.error("Please enter the festival name")
            return
        
        if uploaded_file is None:
            st.error("Please upload a file")
            return
        
        # Step 1: Upload file locally
        with st.spinner("Processing file..."):
            result = upload_file(selected_village, uploaded_file)
        
        if not result.get("success"):
            st.error(f"Upload failed: {result.get('error', 'Unknown error')}")
            return
        
        upload_data = result
        # Add festival name and other form data to upload_data
        upload_data["festival_name"] = festival_name
        upload_data["village"] = selected_village
        upload_data["story_text"] = story_text
        upload_data["language"] = summary_language
        st.session_state.upload_data = upload_data
        st.success("File uploaded successfully!")
        
        # Step 2: Generate AI summary
        with st.spinner("Generating AI summary..."):
            try:
                # For text files, read content
                if uploaded_file.type and 'text' in uploaded_file.type:
                    content = uploaded_file.getvalue().decode('utf-8')
                    story_content = f"Festival story from {selected_village} district of Telangana, India: {story_text + ' ' + content if story_text else content}. This is a traditional festival celebrated in the Telangana region with cultural significance and local traditions."
                # For audio files, use story text
                elif uploaded_file.type and 'audio' in uploaded_file.type:
                    story_content = f"Festival story from {selected_village} district of Telangana, India: {story_text if story_text else 'Audio content about traditional festival'}. This is a traditional festival celebrated in the Telangana region with cultural significance and local traditions."
                # For images/videos, use story text or generate description
                else:
                    if story_text:
                        story_content = f"Festival story from {selected_village} district of Telangana, India: {story_text}. This is a traditional festival celebrated in the Telangana region with cultural significance and local traditions."
                    else:
                        story_content = f"Festival content from {selected_village} district of Telangana, India. This region is known for its rich cultural heritage and traditional festivals that celebrate local customs and religious practices."
                
                # Generate summary using template functions
                try:
                    english_summary = create_english_summary(festival_name, selected_village, story_text)
                except Exception as e:
                    # Fallback to a simple summary
                    english_summary = f"{festival_name} is a traditional festival celebrated in {selected_village} district of Telangana, India. This festival holds cultural and religious significance for the local community."
                
                # Handle language preference
                if summary_language == "English Only":
                    summary = english_summary
                elif summary_language == "Telugu Only":
                    try:
                        summary = create_telugu_summary(festival_name, selected_village)
                    except Exception as e:
                        st.warning(f"Translation failed: {e}")
                        summary = english_summary
                else:  # English & Telugu
                    try:
                        # Use the sentence transformer model to translate English to Telugu
                        telugu_summary = translate_english_to_telugu(english_summary)
                        summary = f"English: {english_summary}\n\nతెలుగు: {telugu_summary}"
                    except Exception as e:
                        st.warning(f"Translation failed: {e}")
                        summary = f"English: {english_summary}"
                
            except Exception as e:
                st.warning(f"AI processing failed: {e}")
                summary = "AI summary generation failed"
        
        # Step 3: Extract summaries for editing
        english_summary_edit = ""
        telugu_summary_edit = ""
        
        if "English:" in summary and "తెలుగు:" in summary:
            # Split bilingual summary
            parts = summary.split("English:")
            if len(parts) > 1:
                english_part = parts[1].split("తెలుగు:")[0].strip()
                english_summary_edit = english_part
                
                # Extract Telugu summary
                telugu_parts = summary.split("తెలుగు:")
                if len(telugu_parts) > 1:
                    telugu_summary_edit = telugu_parts[1].strip()
        elif summary_language == "Telugu Only":
            telugu_summary_edit = summary
            english_summary_edit = "Telugu summary only"
        else:
            english_summary_edit = summary
            telugu_summary_edit = "English summary only"
        
        # Store in session state
        st.session_state.edited_english = english_summary_edit
        st.session_state.edited_telugu = telugu_summary_edit
        st.session_state.submission_complete = True
        st.session_state.form_data_persistent = True
        
        # Step 4: Display results with edit options
        st.success("AI Summary Generated! Please review and edit if needed.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### File Details")
            st.write(f"**Original Name:** {upload_data['original_filename']}")
            st.write(f"**Saved As:** {upload_data['saved_filename']}")
            st.write(f"**File Size:** {upload_data['file_size']} bytes")
            st.write(f"**District:** {upload_data.get('village', selected_village)}")
            st.write(f"**Festival:** {upload_data.get('festival_name', festival_name)}")
            
            if story_text:
                st.markdown("### Story Text")
                st.text_area("Your story:", story_text, height=100, disabled=True)
        
        with col2:
            st.markdown("### Edit Summaries")
            st.markdown("**You can edit the summaries below before saving to Google Sheets:**")
            
            # Editable English Summary
            st.markdown("**English Summary:**")
            edited_english = st.text_area(
                "Edit English Summary:",
                value=english_summary_edit,
                height=120,
                key="english_edit"
            )
            
            # Small update button for English
            if st.button("Update English Summary", type="secondary", key="update_english_btn"):
                st.session_state.edited_english = edited_english
                st.success("English summary updated!")
            
            # Editable Telugu Summary
            st.markdown("**తెలుగు సారాంశం:**")
            edited_telugu = st.text_area(
                "Edit Telugu Summary:",
                value=telugu_summary_edit,
                height=120,
                key="telugu_edit"
            )
            
            # Small update button for Telugu
            if st.button("Update Telugu Summary", type="secondary", key="update_telugu_btn"):
                st.session_state.edited_telugu = edited_telugu
                st.success("Telugu summary updated!")
        
        # Step 5: Confirmation and Save
        st.markdown("---")
        st.markdown("### Save to Google Sheets")
        
        # Show preview of what will be saved
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
            with st.spinner("Saving to database..."):
                # Combine summaries based on language preference
                if summary_language == "English Only":
                    final_summary = edited_english
                elif summary_language == "Telugu Only":
                    final_summary = edited_telugu
                else:  # English & Telugu
                    final_summary = f"English: {edited_english}\n\nతెలుగు: {edited_telugu}"
                
                sheets_success = save_to_sheets(
                    village=upload_data.get('village', selected_village),
                    original_filename=upload_data["original_filename"],
                    saved_filename=upload_data["saved_filename"],
                    file_type=upload_data["file_type"],
                    english_summary=edited_english,
                    telugu_summary=edited_telugu,
                    story_text=upload_data.get('story_text', story_text),
                    language=upload_data.get('language', summary_language),
                    festival_name=upload_data.get('festival_name', festival_name),
                    google_drive_link=upload_data.get('storage_type', 'unknown')
                )
            
            if sheets_success:
                st.success("Successfully saved to Google Sheets!")
                st.markdown("### Database Status")
                st.write(f"**Saved to Sheets:** Success")
                st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Add a button to start new submission instead of auto-resetting
                st.markdown("---")
                if st.button("Start New Submission", type="secondary", use_container_width=True, key="new_submission_btn"):
                    st.session_state.submission_complete = False
                    st.session_state.upload_data = None
                    st.rerun()
            else:
                st.error("Failed to save to Google Sheets. Please try again.")
    
    # Display persistent data if available (outside form to prevent disappearing)
    # Only show if no new submission is being processed
    if st.session_state.form_data_persistent and st.session_state.upload_data and not submit_button:
        st.markdown("---")
        st.markdown("### Previous Submission Results")
        
        upload_data = st.session_state.upload_data
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### File Details")
            st.write(f"**Original Name:** {upload_data['original_filename']}")
            st.write(f"**Saved As:** {upload_data['saved_filename']}")
            st.write(f"**File Size:** {upload_data['file_size']} bytes")
            st.write(f"**District:** {upload_data.get('village', 'N/A')}")
            st.write(f"**Festival:** {upload_data.get('festival_name', 'N/A')}")
            
            # Show file location based on storage type
            storage_type = upload_data.get('storage_type', 'unknown')
            if storage_type == 'local':
                file_path = upload_data.get('file_path', 'Saved locally')
                st.write(f"**File Location:** {file_path}")
                st.success("✅ File saved to your PC")
            elif storage_type == 'session':
                st.write(f"**File Location:** {upload_data.get('google_drive_link', 'File uploaded successfully')}")
                st.info("ℹ️ File stored temporarily in session (Streamlit Cloud)")
            else:
                st.write("**File Location:** File uploaded successfully")
            
            if upload_data.get('story_text'):
                st.markdown("### Story Text")
                st.text_area("Your story:", upload_data['story_text'], height=100, disabled=True, key="persistent_story")
        
        with col2:
            st.markdown("### Edit Summaries")
            st.markdown("**You can edit the summaries below before saving to Google Sheets:**")
            
            # Editable English Summary
            st.markdown("**English Summary:**")
            edited_english = st.text_area(
                "Edit English Summary:",
                value=st.session_state.edited_english,
                height=120,
                key="persistent_english_edit"
            )
            
            # Small update button for English
            if st.button("Update English Summary", type="secondary", key="persistent_update_english_btn"):
                st.session_state.edited_english = edited_english
                st.success("English summary updated!")
            
            # Editable Telugu Summary
            st.markdown("**తెలుగు సారాంశం:**")
            edited_telugu = st.text_area(
                "Edit Telugu Summary:",
                value=st.session_state.edited_telugu,
                height=120,
                key="persistent_telugu_edit"
            )
            
            # Small update button for Telugu
            if st.button("Update Telugu Summary", type="secondary", key="persistent_update_telugu_btn"):
                st.session_state.edited_telugu = edited_telugu
                st.success("Telugu summary updated!")
            
            # Update session state with edits
            st.session_state.edited_english = edited_english
            st.session_state.edited_telugu = edited_telugu
        
        # Confirmation and Save
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
        if st.button("Confirm and Save to Google Sheets", type="primary", use_container_width=True, key="persistent_save_btn"):
            with st.spinner("Saving to database..."):
                sheets_success = save_to_sheets(
                    village=upload_data.get('village', 'Unknown'),
                    original_filename=upload_data["original_filename"],
                    saved_filename=upload_data["saved_filename"],
                    file_type=upload_data["file_type"],
                    english_summary=edited_english,
                    telugu_summary=edited_telugu,
                    story_text=upload_data.get('story_text', ''),
                    language=upload_data.get('language', ''),
                    festival_name=upload_data.get('festival_name', ''),
                    google_drive_link=upload_data.get('storage_type', 'unknown')
                )
            
            if sheets_success:
                st.success("Successfully saved to Google Sheets!")
                st.markdown("### Database Status")
                st.write(f"**Saved to Sheets:** Success")
                st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Add a button to start new submission instead of auto-resetting
                st.markdown("---")
                if st.button("Start New Submission", type="secondary", use_container_width=True, key="persistent_new_submission_btn"):
                    st.session_state.submission_complete = False
                    st.session_state.upload_data = None
                    st.session_state.form_data_persistent = False
                    st.session_state.edited_english = ""
                    st.session_state.edited_telugu = ""
                    st.rerun()
            else:
                st.error("Failed to save to Google Sheets. Please try again.")

if __name__ == "__main__":
    main() 