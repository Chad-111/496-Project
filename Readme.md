# 🏈 DraftEmpire

Welcome to **DraftEmpire** – a sports fantasy platform focused on **college football**! This repo contains both the **backend (Flask + Gunicorn + PostgreSQL/SQLite)** and the **frontend (React + Vite)**, hosted on a home Ubuntu server with **GitHub Actions for auto-deployment**.

---

## 🚀 Project Overview

- **Backend:** Flask, Gunicorn, Flask-SQLAlchemy, PostgreSQL/SQLite
- **Frontend:** React, Vite
- **Server:** Ubuntu (Mini PC at home), hosted via **NGINX + Gunicorn**
- **Auto Deployment:** GitHub Actions + SSH

---

## 📁 Project Structure

```
496-Project/
│-- backend/  # Flask API
│   │-- server.py  # Main entry point
│   │-- models.py  # Database models
│   │-- routes.py  # API routes
│   │-- requirements.txt  # Python dependencies
│   │-- venv/  # Virtual environment (not in repo)
│
│-- frontend/  # React App
│   │-- src/
│   │-- dist/  # Built frontend (served by NGINX)
│   │-- package.json  # Node dependencies
│
│-- .github/workflows/
│   │-- deploy.yml  # GitHub Actions auto-deploy config
│
│-- README.md  # This file
```

---

## 🔥 How to Run Locally

### **Backend Setup**
1. **Clone the repo:**
   ```bash
   git clone https://github.com/Chad-111/496-Project.git
   # Go into backend ;)
   cd 496-Project/backend
   ```
2. **Create a virtual environment & activate it:**

    *Windows:* 
      ```bash
      py -m venv venv
      # Activate virtual env
      venv/scripts/activate
      ```
   *macOS/Linux:*
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Flask locally:**

   *Windows:*
      ```bash
      flask --app server.py run
      ```
   *macOS/Linux:*
      ```bash
      flask run --host=0.0.0.0 --port=5000
      ```

### **Frontend Setup**
1. **Go to the frontend directory:**
   ```bash
   cd ../frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Run the dev server:**
   ```bash
   npm run dev
   ```
4. **Access the frontend:**
   - Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🌍 Deployment Process
### **Auto Deployment via GitHub Actions**
Every push to `main` triggers the auto-deploy workflow!

1. **Make changes and push to GitHub:**
   ```bash
   git add .
   git commit -m "New feature/update"
   git push origin main
   ```
2. GitHub Actions will:
   - SSH into the Ubuntu server
   - Pull the latest code
   - Restart Flask & rebuild the frontend
   - Restart NGINX

### **Manual Deployment (if needed)**
If something goes wrong with auto-deployment, SSH into the server:
```bash
ssh chad@<SERVER_IP>
cd /home/chad/496-Project
./deploy.sh  # If a deployment script exists
```

---

## 📌 Environment Variables
Create a `.env` file in `backend/` and add:
```
DATABASE_URL=postgresql://username:password@localhost/draftempire
SECRET_KEY=your-secret-key
```
For SQLite (local testing):
```
DATABASE_URL=sqlite:///site.db
```

---

## 🛠️ Troubleshooting
### **1. Flask API Not Working?**
- Check if Flask is running:
  ```bash
  sudo systemctl status flask
  ```
- Restart if needed:
  ```bash
  sudo systemctl restart flask
  ```

### **2. Frontend Not Updating?**
- Check the latest frontend build:
  ```bash
  cd /home/chad/496-Project/frontend
  npm run build
  sudo systemctl restart nginx
  ```

### **3. SSH Issues with GitHub Actions?**
- Ensure the SSH key is correct in GitHub Secrets.
- Check `/home/chad/.ssh/authorized_keys`.

---

🔥 **DraftEmpire FTW!** 🚀🏈

