# Free Deployment Guide

Since your project has a **Python Backend** and an **HTML Frontend**, you need two different hosting strategies to keep it 100% free.

## 1. Prepare your Code for Deployment
To deploy, you should first push your code to **GitHub**.

### Changes needed:
In `frontend/index.html`, you will need to change the `API_BASE` variable from `http://localhost:8000` to your actual backend URL once it's deployed.

---

## 2. Deploy the Backend (Free)
I recommend **Render** or **Railway** for the backend.

### Option A: Render (Easiest)
1. Create a free account on [Render.com](https://render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Use these settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend/main.py` (or `uvicorn backend.main:app --host 0.0.0.0 --port 10000`)
5. Render will give you a URL like `https://your-app.onrender.com`.

> [!NOTE]
> You'll need a `requirements.txt` file in your backend folder. I've generated one for you below.

---

## 3. Deploy the Frontend (Free)
I recommend **Vercel** or **GitHub Pages**.

### Option A: Vercel (Recommended)
1. Go to [Vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New** -> **Project**.
3. Select your GitHub repo.
4. Vercel will automatically detect the static files and deploy them.

---

## 4. Final Step: Connect Them
1. Once your backend is live on Render, copy its URL.
2. Go back to `frontend/index.html` on your local PC.
3. Change this line:
   ```javascript
   const API_BASE = 'https://your-app-name.onrender.com';
   ```
4. Save, commit, and push to GitHub. Both Render and Vercel will automatically update!

---

## Generated Requirements File
I've created a `requirements.txt` file in your `backend` folder to make this even easier for you.
