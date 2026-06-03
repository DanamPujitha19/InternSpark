#!/usr/bin/env python3
"""
File Organizer & Cleaner Automation Script
Author: AI Collaborator
Requirements: OS module, Exception Handling, Logging, User Input
"""

import os
import shutil
import logging
from datetime import datetime

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("file_operations.log"),
        logging.StreamHandler()  # Echoes logs to the terminal
    ]
)

# Extension mapping for sorting
TRACKED_EXTENSIONS = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx', '.csv'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Audio_Video': ['.mp3', '.mp4', '.mkv', '.wav', '.mov'],
    'Scripts': ['.py', '.sh', '.js', '.html', '.css']
}

def setup_directory(path):
    """Validates the target directory."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path '{path}' is not a valid directory.")
    return os.path.abspath(path)

def organize_files(target_dir, rename_prefix=None):
    """Sorts and optionally renames files in the target directory."""
    print(f"\n🚀 Starting automation in: {target_dir}\n" + "="*50)
    logging.info(f"Automation sequence started in directory: {target_dir}")
    
    try:
        files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
        
        if not files:
            logging.info("No files found to process.")
            print("📁 No files found to organize.")
            return

        success_count = 0
        fail_count = 0

        for file_name in files:
            # Skip the log file itself if it's in the same directory
            if file_name == "file_operations.log":
                continue

            old_path = os.path.join(target_dir, file_name)
            name, ext = os.path.splitext(file_name)
            ext = ext.lower()

            # Determine destination folder category
            dest_folder = "Others"
            for category, extensions in TRACKED_EXTENSIONS.items():
                if ext in extensions:
                    dest_folder = category
                    break

            dest_dir = os.path.join(target_dir, dest_folder)

            try:
                # Create category folder if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    logging.info(f"Created category directory: {dest_folder}")

                # Handle optional renaming (Prefix_Timestamp_OriginalName)
                if rename_prefix:
                    timestamp = datetime.now().strftime("%Y%m%d")
                    new_name = f"{rename_prefix}_{timestamp}_{file_name}"
                else:
                    new_name = file_name

                new_path = os.path.join(dest_dir, new_name)

                # Move (and rename) the file safely
                shutil.move(old_path, new_path)
                logging.info(f"Successfully moved: '{file_name}' -> '{dest_folder}/{new_name}'")
                success_count += 1

            except (PermissionError, shutil.Error) as file_err:
                logging.error(f"Failed to process file '{file_name}': {file_err}")
                fail_count += 1
                continue

        print(f"\n✅ Operation Complete! Processed: {success_count} files. Failed: {fail_count} files.")
        logging.info(f"Sequence finished. Success: {success_count}, Failures: {fail_count}")

    except Exception as e:
        logging.critical(f"Critical error during automation: {e}")
        print(f"❌ A critical error occurred: {e}")

if __name__ == "__main__":
    print("🤖 Welcome to the File Automation Assistant 🤖")
    
    # User Input Support
    while True:
        user_path = input("Enter the absolute path of the directory to organize: ").strip()
        try:
            target_directory = setup_directory(user_path)
            break
        except (FileNotFoundError, NotADirectoryError) as err:
            print(f"⚠️  Input Error: {err}. Please try again.\n")

    want_rename = input("Do you want to add a standard prefix to all files? (y/n): ").strip().lower()
    prefix = None
    if want_rename == 'y':
        prefix = input("Enter the file prefix (e.g., 'Archive', 'ProjectX'): ").strip()

    # Trigger automation
    organize_files(target_directory, rename_prefix=prefix)
