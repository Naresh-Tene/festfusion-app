#!/usr/bin/env python3
"""
Automated Git Sync Script for FestFusion
This script automatically syncs local changes to GitHub
"""

import subprocess
import sys
import os
from datetime import datetime
import time

def run_command(command, capture_output=True):
    """Run a shell command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip(), result.stderr.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return "", ""
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        return None, e.stderr

def check_git_status():
    """Check if there are any changes to commit"""
    stdout, stderr = run_command("git status --porcelain")
    if stdout:
        return True, stdout
    return False, ""

def get_changed_files():
    """Get list of changed files"""
    stdout, stderr = run_command("git status --porcelain")
    if stdout:
        files = [line.split()[-1] for line in stdout.split('\n') if line.strip()]
        return files
    return []

def create_commit_message():
    """Create a meaningful commit message based on changes"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    changed_files = get_changed_files()
    
    if not changed_files:
        return f"Auto-sync: No changes detected at {timestamp}"
    
    # Categorize changes
    categories = {
        'frontend': [],
        'backend': [],
        'config': [],
        'docs': [],
        'other': []
    }
    
    for file in changed_files:
        if file.endswith('.py') and ('streamlit' in file.lower() or 'frontend' in file.lower()):
            categories['frontend'].append(file)
        elif file.endswith('.py') and ('flask' in file.lower() or 'api' in file.lower()):
            categories['backend'].append(file)
        elif file in ['config.py', 'requirements.txt'] or file.endswith('.json'):
            categories['config'].append(file)
        elif file.endswith('.md') or file.endswith('.txt'):
            categories['docs'].append(file)
        else:
            categories['other'].append(file)
    
    # Build commit message
    message_parts = [f"Auto-sync: {timestamp}"]
    
    for category, files in categories.items():
        if files:
            if category == 'frontend':
                message_parts.append(f"Frontend updates: {', '.join(files)}")
            elif category == 'backend':
                message_parts.append(f"Backend updates: {', '.join(files)}")
            elif category == 'config':
                message_parts.append(f"Config updates: {', '.join(files)}")
            elif category == 'docs':
                message_parts.append(f"Documentation updates: {', '.join(files)}")
            else:
                message_parts.append(f"Other updates: {', '.join(files)}")
    
    return "\n".join(message_parts)

def sync_to_github():
    """Main function to sync changes to GitHub"""
    print("🔄 Checking for changes...")
    
    # Check if we're in a git repository
    stdout, stderr = run_command("git rev-parse --git-dir")
    if stderr:
        print("❌ Not in a Git repository. Please run this script from your project directory.")
        return False
    
    # Check for changes
    has_changes, changes = check_git_status()
    
    if not has_changes:
        print("✅ No changes detected. Repository is up to date!")
        return True
    
    print(f"📝 Found changes:\n{changes}")
    
    # Add all changes
    print("📦 Adding changes to staging...")
    stdout, stderr = run_command("git add .")
    if stderr:
        print(f"❌ Error adding files: {stderr}")
        return False
    
    # Create commit message
    commit_message = create_commit_message()
    print(f"💬 Commit message:\n{commit_message}")
    
    # Commit changes
    print("💾 Committing changes...")
    stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    if stderr:
        print(f"❌ Error committing: {stderr}")
        return False
    
    # Push to GitHub
    print("🚀 Pushing to GitHub...")
    stdout, stderr = run_command("git push origin main")
    if stderr:
        print(f"❌ Error pushing to GitHub: {stderr}")
        return False
    
    print("✅ Successfully synced to GitHub!")
    return True

def setup_auto_sync():
    """Set up automated syncing with a simple script"""
    print("🔧 Setting up automated sync...")
    
    # Create a simple batch script for Windows
    batch_script = """@echo off
cd /d "%~dp0"
call venv\\Scripts\\activate
python auto_sync.py
pause
"""
    
    with open("sync.bat", "w") as f:
        f.write(batch_script)
    
    print("✅ Created sync.bat - you can now double-click this file to sync changes!")
    print("💡 You can also run 'python auto_sync.py' directly from the command line.")

def main():
    """Main function"""
    print("🎯 FestFusion Auto-Sync Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_auto_sync()
        return
    
    success = sync_to_github()
    
    if success:
        print("\n🎉 Sync completed successfully!")
    else:
        print("\n❌ Sync failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 