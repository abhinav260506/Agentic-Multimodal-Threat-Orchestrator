"""
Test script to simulate file uploads and processing
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:5000"

def login():
    """Login and get session"""
    session = requests.Session()
    
    # Login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code in [302, 200]:
        print("[OK] Login successful")
        return session
    else:
        print(f"[ERROR] Login failed: {response.status_code}")
        return None

def upload_file(session, file_path, file_type):
    """Upload a file"""
    if not Path(file_path).exists():
        print(f"[ERROR] File not found: {file_path}")
        return False
    
    with open(file_path, 'rb') as f:
        files = {'file': (Path(file_path).name, f, 'application/octet-stream')}
        data = {'file_type': file_type}
        
        response = session.post(f"{BASE_URL}/upload", files=files, data=data)
        
        if response.status_code == 200 or 'success' in response.text.lower():
            print(f"[OK] Uploaded: {Path(file_path).name} ({file_type})")
            return True
        else:
            print(f"[ERROR] Upload failed: {response.status_code}")
            print(response.text[:200])
            return False

def main():
    print("="*60)
    print("Testing Dashboard File Upload")
    print("="*60)
    
    # Login
    session = login()
    if not session:
        print("Cannot proceed without login")
        return
    
    # Upload log files
    print("\n[Uploading Log Files]")
    log_files = [
        ("dashboard/sample_data/sample_security_logs.csv", "logs"),
        ("dashboard/sample_data/sample_network_logs.csv", "logs"),
        ("dashboard/uploads/logs/sample_logs.csv", "logs") if Path("dashboard/uploads/logs/sample_logs.csv").exists() else None
    ]
    
    for file_info in log_files:
        if file_info:
            upload_file(session, file_info[0], file_info[1])
    
    # Upload video file
    print("\n[Uploading Video Files]")
    video_file = "dashboard/uploads/videos/sample_video.mp4"
    if Path(video_file).exists():
        upload_file(session, video_file, "videos")
    else:
        print("No video file found to upload")
    
    print("\n" + "="*60)
    print("Upload Test Complete!")
    print("="*60)
    print("\nCheck the dashboard at http://localhost:5000 to see:")
    print("  - Uploaded files")
    print("  - Generated alerts")
    print("  - Processing results")

if __name__ == "__main__":
    main()

