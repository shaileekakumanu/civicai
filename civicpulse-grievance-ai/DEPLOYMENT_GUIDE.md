# 🚀 Deployment Guide: Deploying CivicPulse AI to the Cloud

This guide provides step-by-step instructions to deploy your **CivicPulse AI** project to free cloud hosting platforms (**Render**, **Railway**, or **Hugging Face Spaces**) so you have a live, public URL accessible anywhere in the world.

---

## 📦 What Was Prepared in Your Project

All production deployment files have already been generated, configured, and committed to your local Git repository:

1. **`Dockerfile`**: Container image configured with Python 3.11, dependency caching, and environment variable port binding.
2. **`render.yaml`**: Infrastructure-as-code blueprint for 1-click free deployment on [Render.com](https://render.com).
3. **`Procfile`**: Standard deployment descriptor for Railway, Render, and Heroku (`web: python start.py`).
4. **`start.py`**: Production entrypoint that automatically reads the dynamic `$PORT` provided by cloud hosts.
5. **`.dockerignore` & `.gitignore`**: Excludes temporary files, caches, and test artifacts.
6. **Git Repository**: Initialized with branch `main` and ready to push to GitHub.

---

## 🌟 Method 1: Deploy on Render.com (Recommended - 100% Free)

Render provides free hosting for Python and FastAPI web applications with automated SSL certificates (`https://...onrender.com`).

### Step 1: Push your code to GitHub
1. Open [github.com/new](https://github.com/new) in your browser.
2. Name your repository (e.g., `civicpulse-ai`), set it to **Public** or **Private**, and click **Create repository**.
3. In PowerShell or Terminal, run the following commands (replace `<YOUR_USERNAME>` with your GitHub username):

```bash
cd "C:\Users\Shailee and Neha\.gemini\antigravity\scratch\civicpulse-grievance-ai"
git remote add origin https://github.com/<YOUR_USERNAME>/civicpulse-ai.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [dashboard.render.com](https://dashboard.render.com/) and sign up or log in (you can sign in with GitHub).
2. Click **New +** &rarr; **Web Service**.
3. Select your `civicpulse-ai` GitHub repository.
4. Render will automatically detect the configuration from `render.yaml`:
   - **Name**: `civicpulse-ai`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start.py`
5. Select the **Free** plan.
6. Click **Deploy Web Service**!

Render will build and deploy your application in 2–3 minutes and provide a live public link, e.g.:
👉 `https://civicpulse-ai.onrender.com`

---

## 🐳 Method 2: Deploy on Hugging Face Spaces (Free 24/7 Hosting)

Hugging Face Spaces offers free 24/7 CPU hosting specifically designed for AI and NLP applications:

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Name your Space (e.g., `civicpulse-ai`).
3. Select **Space SDK**: **Docker** &rarr; **Blank**.
4. Set license and visibility (Public).
5. In your local terminal, add the Hugging Face remote and push:
   ```bash
   git remote add hf https://huggingface.co/spaces/<YOUR_HF_USERNAME>/civicpulse-ai
   git push hf main
   ```
6. Hugging Face will automatically detect your `Dockerfile`, build the image, and launch the portal live!

---

## 🚂 Method 3: Deploy on Railway

Railway supports automatic Docker and Procfile deployments:

1. Visit [railway.app](https://railway.app/) and sign in with GitHub.
2. Click **New Project** &rarr; **Deploy from GitHub repo**.
3. Choose your `civicpulse-ai` repository.
4. Railway will automatically detect `Procfile` or `Dockerfile` and deploy the service.
5. In project settings, click **Generate Domain** to get your public `https://...up.railway.app` URL.

---

## 🖥️ Local / On-Premise Docker Deployment

If you want to run the containerized application locally or on a VPS (AWS EC2, DigitalOcean, Azure VM):

```bash
cd "C:\Users\Shailee and Neha\.gemini\antigravity\scratch\civicpulse-grievance-ai"

# Build the Docker image
docker build -t civicpulse-ai .

# Run the container mapping port 8000
docker run -d -p 8000:8000 --name civicpulse civicpulse-ai
```
The application will then be live at `http://localhost:8000`.
