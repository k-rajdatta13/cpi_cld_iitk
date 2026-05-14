# 🎓 IITK CPI Calculator — Deployment Guide

> A modern, mobile-friendly CPI calculator for IIT Kanpur students.
> Built with Streamlit · Plotly · Pandas

---

## 📁 Files You Have

```
app.py            ← the main app (all logic + UI)
requirements.txt  ← Python packages the app needs
README.md         ← this file
```

---

## 🚀 Option A — Deploy FREE on Streamlit Cloud (Recommended for beginners)

**What you need:** a GitHub account (free) + a Google / email account.

### Step 1 — Create a GitHub repository

1. Go to https://github.com and sign in (or sign up, it's free).
2. Click the **+** button (top right) → **New repository**.
3. Name it something like `iitk-cpi-calculator`.
4. Keep it **Public**.
5. Click **Create repository**.

### Step 2 — Upload your files to GitHub

On the new repo page:

1. Click **uploading an existing file** (or drag-and-drop).
2. Upload **app.py** and **requirements.txt** (both files).
3. Click **Commit changes**.

### Step 3 — Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud and sign in with GitHub.
2. Click **New app**.
3. Choose:
   - **Repository** → select `iitk-cpi-calculator`
   - **Branch**     → `main`
   - **Main file**  → `app.py`
4. Click **Deploy!**

✅ That's it! Streamlit will give you a **public URL** like:
`https://yourname-iitk-cpi-calculator-app-xyz.streamlit.app`

You can share this link with anyone. It runs 24/7 for free.

---

## 💻 Option B — Run Locally on Your Own Computer

If you just want to test the app on your laptop before deploying:

### Step 1 — Install Python (if not already installed)

Download Python 3.11+ from https://python.org/downloads/
> During installation on Windows, tick ✅ **Add Python to PATH**

### Step 2 — Install the required packages

Open **Terminal** (Mac/Linux) or **Command Prompt** (Windows) and run:

```bash
pip install streamlit pandas plotly
```

### Step 3 — Run the app

Navigate to the folder containing `app.py`, then run:

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501` 🎉

---

## ✏️ How to Update the App

After deployment, any changes you push to GitHub are automatically
reflected on your Streamlit Cloud app within a minute or two.

1. Edit `app.py` on GitHub (click the file → pencil icon ✏️)
2. Make your changes
3. Click **Commit changes**
4. Streamlit Cloud auto-redeploys ✅

---

## 🎨 Quick Customisation Reference

| What to change             | Where in app.py         |
|----------------------------|-------------------------|
| Colour scheme              | `SECTION 3` → `:root {}` CSS variables |
| Grade scale (A/B/C points) | `SECTION 4` → `GRADE_POINTS` dict |
| Default credits value      | `SECTION 6` → sidebar `number_input` `value=` |
| App title                  | `SECTION 2` → `page_title=` and `SECTION 7` → hero HTML |
| Footer text                | `SECTION 11` |

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit pandas plotly` |
| White page / nothing loads | Hard-refresh browser (Ctrl+Shift+R) |
| Chart not showing | Make sure `plotly` is in requirements.txt |
| App crashed on Streamlit Cloud | Check the logs (click **Manage app** → **Logs**) |

---

*Made with ❤️ · Follows the official IITK grading system*
