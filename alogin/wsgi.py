# ============================================================
# PythonAnywhere WSGI configuration
#
# HOW TO USE:
# 1. Go to pythonanywhere.com → Web tab → your app
# 2. Click "WSGI configuration file" link
# 3. Replace ALL content with this file
# 4. Change YOUR_USERNAME below to your PythonAnywhere username
# 5. Click Save, then Reload
# ============================================================

import sys
import os

# ── Change this to your PythonAnywhere username ──────────────
USERNAME = "gsunilkumarreddy23"
# ─────────────────────────────────────────────────────────────

project_home = f"/home/{USERNAME}/alogin"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate the virtualenv
activate_this = f"/home/{USERNAME}/.virtualenvs/flask-webapp-env/bin/activate_this.py"
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {"__file__": activate_this})

from app import app as application