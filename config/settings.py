# config/settings.py
# ------------------
# Responsible for loading all sensitive values from the .env file.
# No hardcoded secrets anywhere in the project — only here.

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is missing. Please add it to your .env file.")