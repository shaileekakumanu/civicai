"""
Production entrypoint for cloud deployment (Render, Railway, Fly.io, Heroku, Hugging Face).
Reads the PORT environment variable assigned by cloud hosting platforms.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    project_root = os.path.abspath(os.path.dirname(__file__))
    backend_dir = os.path.join(project_root, "backend")
    sys.path.insert(0, backend_dir)
    
    print(f"[*] Starting CivicPulse AI on port {port} ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, app_dir=backend_dir)
