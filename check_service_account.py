#!/usr/bin/env python3
"""
Check Service Account Information and Google Sheets Access
"""

import json
from google.oauth2.service_account import Credentials
import gspread

def check_service_account():
    """Check service account information"""
    try:
        # Load credentials
        with open("festfusion-project-cc628988dd80.json", "r") as f:
            creds_data = json.load(f)
        
        print("🔍 Service Account Information:")
        print("=" * 50)
        print(f"Project ID: {creds_data.get('project_id', 'Not found')}")
        print(f"Client Email: {creds_data.get('client_email', 'Not found')}")
        print(f"Private Key ID: {creds_data.get('private_key_id', 'Not found')[:20]}...")
        print(f"Token URI: {creds_data.get('token_uri', 'Not found')}")
        
        # Test credentials
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file("festfusion-project-cc628988dd80.json", scopes=scope)
        print(f"\n✅ Credentials loaded successfully")
        print(f"Scopes: {creds.scopes}")
        
        return creds_data.get('client_email')
        
    except Exception as e:
        print(f"❌ Error loading service account: {e}")
        return None

def test_google_sheets_access(client_email):
    """Test Google Sheets access"""
    try:
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file("festfusion-project-cc628988dd80.json", scopes=scope)
        client = gspread.authorize(creds)
        
        print(f"\n🔍 Testing Google Sheets Access:")
        print("=" * 50)
        
        # Try to open the sheet
        try:
            spreadsheet = client.open("FestFusion Data")
            print(f"✅ Successfully opened: {spreadsheet.title}")
            print(f"📊 Sheet ID: {spreadsheet.id}")
            print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
            
            # Get worksheet info
            worksheet = spreadsheet.sheet1
            print(f"📋 Worksheet: {worksheet.title}")
            print(f"📏 Rows: {worksheet.row_count}")
            print(f"📐 Columns: {worksheet.col_count}")
            
            # Test writing a row
            test_row = ["TEST", "TEST_VILLAGE", "test_file.txt", "test_saved.txt", "text/plain", "test story", "test summary"]
            worksheet.append_row(test_row)
            print(f"✅ Successfully wrote test row to sheet")
            
            # Clean up test row
            worksheet.delete_rows(worksheet.row_count)
            print(f"✅ Cleaned up test row")
            
            return True
            
        except Exception as e:
            print(f"❌ Error accessing sheet: {e}")
            print(f"\n🔧 To fix this:")
            print(f"1. Open your Google Sheet 'FestFusion Data'")
            print(f"2. Click 'Share' button")
            print(f"3. Add this email: {client_email}")
            print(f"4. Give 'Editor' permissions")
            print(f"5. Click 'Send'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing sheets access: {e}")
        return False

def main():
    """Main function"""
    print("🏛️ FestFusion - Service Account Check")
    print("=" * 60)
    
    # Check service account
    client_email = check_service_account()
    
    if client_email:
        print(f"\n📧 Service Account Email: {client_email}")
        print(f"📝 Use this email to share your Google Sheet")
        
        # Test sheets access
        test_google_sheets_access(client_email)
    else:
        print("❌ Could not load service account information")

if __name__ == "__main__":
    main() 