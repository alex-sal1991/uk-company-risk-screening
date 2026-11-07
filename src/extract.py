import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CH_API_KEY")

if API_KEY is None:
    raise ValueError("No API Key")