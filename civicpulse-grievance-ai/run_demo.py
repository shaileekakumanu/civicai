"""
CivicPulse AI - One-Click Application Runner.
Launches the FastAPI server and opens the Citizen Grievance Portal in default browser.
"""
import os
import sys
import socket
import webbrowser
import threading
import time
import uvicorn

def find_available_port(start_port=8000, max_attempts=10):
    for p in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return start_port

def open_browser(port):
    time.sleep(1.5)
    url = f"http://127.0.0.1:{port}"
    print(f"\n[+] Opening CivicPulse Citizen Grievance Portal in browser: {url}")
    webbrowser.open(url)

if __name__ == '__main__':
    project_root = os.path.abspath(os.path.dirname(__file__))
    backend_dir = os.path.join(project_root, 'backend')
    sys.path.insert(0, backend_dir)
    
    port = find_available_port(8000)
    
    print("=" * 70)
    print("  🚀 CivicPulse AI: Intelligent Citizen Grievance Classification")
    print("     & Automated Municipal Rapid-Routing Platform")
    print("=" * 70)
    print(f"[*] Starting backend server on http://127.0.0.1:{port} ...")
    print(f"[*] Citizen Portal: http://127.0.0.1:{port}")
    print(f"[*] Municipal Command Center: http://127.0.0.1:{port}/static/admin.html")
    print(f"[*] Interactive API Docs: http://127.0.0.1:{port}/docs")
    print("=" * 70)

    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False, app_dir=backend_dir)

