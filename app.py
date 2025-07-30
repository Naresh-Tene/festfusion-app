import streamlit as st
from transformers import pipeline
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import tempfile
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- AI Model Caching ---
@st.cache_resource
def get_summarizer():
    """Loads the summarization model from Hugging Face."""
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@st.cache_resource
def get_transcriber():
    """Loads the audio transcription model (Whisper)."""
    return pipeline("automatic-speech-recognition", model="openai/whisper-base")

# --- Google Services Connection ---
@st.cache_resource
def get_creds():
    """Gets the credentials to connect to Google services."""
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # !!! IMPORTANT !!! 
    # Replace this with the name of your NEW JSON key file.
    creds = Credentials.from_service_account_file("YOUR_NEW_JSON_FILE_NAME.json", scopes=scope)
    return creds

# --- Google Drive Upload Function ---
def upload_to_drive(file_path, file_name):
    """Uploads a file to the specified Google Drive folder."""
    creds = get_creds()
    service = build('drive', 'v3', credentials=creds)
    
    # !!! IMPORTANT !!! 
    # Replace this with your NEW Google Drive Folder ID.
    folder_id = 'YOUR_NEW_GOOGLE_DRIVE_FOLDER_ID' 
    
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    
    # Add supportsAllDrives=True if you are using a Shared Drive
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    return file.get('webViewLink')

# --- UI Configuration ---
st.set_page_config(page_title="FestFusion Telangana", page_icon="🏛️")
st.title("🏛️ FestFusion Telangana")
st.write("Share a story about a local festival from your village.")

telangana_districts = ["Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", "Medchal-Malkajgiri", "Nagarkurnool", "Nalgonda", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Hanamkonda", "Yadadri Bhuvanagiri"]

selected_district = st.selectbox("Select Your District:", options=sorted(telangana_districts))
story_text = st.text_area("Write your story here, or transcribe it from an audio file below:", height=150)
uploaded_file = st.file_uploader("Upload an image, audio, or video file", type=['png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4'])

# --- Main Logic ---
if st.button("Generate Summary & Archive Story"):
    transcribed_text = ""
    file_link = ""
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_filepath = tmp_file.name

        with st.spinner("Uploading your file to our archive..."):
            file_link = upload_to_drive(temp_filepath, uploaded_file.name)
            st.success("File successfully uploaded to archive!")

        if 'audio' in uploaded_file.type:
            with st.spinner("AI is listening to the audio..."):
                transcriber = get_transcriber()
                transcription_result = transcriber(temp_filepath)
                transcribed_text = transcription_result['text']
                st.info("Transcription complete!")
        
        os.remove(temp_filepath)

    final_story = story_text + "\n" + transcribed_text
    
    if final_story.strip():
        with st.spinner("Our AI is crafting a summary..."):
            summarizer = get_summarizer()
            summary = summarizer(final_story, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        st.success("Summary Generated!")

        with st.spinner("Archiving your story in our database..."):
            creds = get_creds()
            client = gspread.authorize(creds)
            # !!! IMPORTANT !!! 
            # Replace this with the name of your NEW Google Sheet.
            spreadsheet = client.open("YOUR_NEW_GOOGLE_SHEET_NAME")
            worksheet = spreadsheet.sheet1
            new_row = pd.DataFrame([{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "village": selected_district, "story": final_story, "summary": summary, "file_link": file_link}])
            worksheet.append_rows(new_row.values.tolist())
        st.success("Story successfully archived!")
        st.balloons()

        st.subheader("Your Full Story:")
        st.write(final_story)
        st.subheader("🤖 AI-Generated Summary:")
        st.write(summary)
        if file_link:
            st.write(f"View your uploaded file [here]({file_link}).")
    else:
        st.warning("Please write a story or upload a file.")