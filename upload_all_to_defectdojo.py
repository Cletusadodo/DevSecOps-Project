import os
import requests
from datetime import datetime

#Variables
DEFECTDOJO_URL = "http://34.200.54.199:8080"  
API_KEY = os.getenv("DEFECTDOJO_API_KEY")
ENGAGEMENT_ID = 1
SCAN_DATE = datetime.today().strftime('%Y-%m-%d')

# API key validation
if not API_KEY:
    print("Error: DEFECTDOJO_API_KEY environment variable not set.")
    exit(1)

# files to scan types 
SCAN_REPORTS = {
    "trivyfs.txt": "Trivy Scan",
    "dependency-check-report.xml": "Dependency Check Scan",
    "gitleaks-report.json": "Generic Findings Import"  
}

# Upload Function
def upload_file(file_path, scan_type):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb")),
    }

    data = {
        "scan_type": scan_type,
        "engagement": ENGAGEMENT_ID,
        "scan_date": SCAN_DATE,
        "verified": "true",
        "active": "true",
        "minimum_severity": "Medium"
    }

    print(f"Uploading {file_path} as '{scan_type}'...")
    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code in [200, 201]:
        print(f"Upload successful: {file_path}")
    else:
        print(f"Upload failed: {file_path}")
        print(response.text)

#  Run Uploads
for file, scan_type in SCAN_REPORTS.items():
    upload_file(file, scan_type)
