# Hosting on PythonAnywhere — Step by Step Guide

## Prerequisites
- Free account at pythonanywhere.com
- Your flask-webapp folder ready

---

## Step 1 — Upload your files

Go to pythonanywhere.com → **Files** tab

Click "Open Bash console here" and run:
```bash
mkdir flask-webapp
```

Then upload all files using the Files tab:
Upload these files into /home/YOUR_USERNAME/flask-webapp/
  - app.py
  - requirements.txt
  - wsgi.py
  - templates/login.html
  - templates/signup.html
  - templates/dashboard.html

---

## Step 2 — Create a virtual environment

In the Bash console:
```bash
mkvirtualenv flask-webapp-env --python=python3.10
pip install flask requests
```

---

## Step 3 — Create the Web App

1. Go to **Web** tab → "Add a new web app"
2. Click Next → Choose "Manual configuration" → Python 3.10 → Next
3. Your app is created at: yourname.pythonanywhere.com

---

## Step 4 — Configure WSGI

1. On the Web tab, click the WSGI configuration file link
   (looks like: /var/www/yourname_pythonanywhere_com_wsgi.py)
2. Delete ALL existing content
3. Paste the contents of wsgi.py
4. Change YOUR_USERNAME to your actual username
5. Click Save

---

## Step 5 — Set virtualenv path

On the Web tab, under "Virtualenv":
Enter: /home/YOUR_USERNAME/.virtualenvs/flask-webapp-env

---

## Step 6 — Reload

Click the big green "Reload" button on the Web tab.

Your app is now live at: https://YOUR_USERNAME.pythonanywhere.com

---

## Step 7 — Connect the rate limiter

The rate limiter runs on YOUR LOCAL PC (localhost:8000).

Since PythonAnywhere can't reach your localhost directly,
the rate limiter is a "soft integration":

OPTION A (Demo mode — recommended):
  The app calls localhost:8000 which will fail on PythonAnywhere,
  so it FAILS OPEN (allows all requests).
  
  To show the rate limiter working:
  - Run the rate limiter on your local PC (python run.py)
  - Run the brute force simulator against YOUR live site:
    python simulator/brute_sim.py https://YOUR_USERNAME.pythonanywhere.com
  - Show the dashboard on your local PC — it captures all the blocks

OPTION B (Fully integrated):
  Use ngrok to expose your local rate limiter to the internet:
  
  1. Download ngrok from ngrok.com (free)
  2. Run: ngrok http 8000
  3. You'll get a URL like: https://abc123.ngrok-free.app
  4. In app.py, change:
     RATE_LIMITER_URL = "https://abc123.ngrok-free.app/api/request"
  5. Re-upload app.py to PythonAnywhere and reload

  Now PythonAnywhere calls your local rate limiter in real time!

---

## Testing your live site

Visit: https://YOUR_USERNAME.pythonanywhere.com

1. Go to /signup and create an account
2. Go to /login and sign in
3. You'll see the dashboard after successful login

---

## Running the brute force simulator against your live site

In your VS Code terminal:
```bash
python simulator/brute_sim.py https://YOUR_USERNAME.pythonanywhere.com
```

Watch the dashboard — it shows blocks happening in real time.