import os
import requests
from dotenv import load_dotenv
from utils import ensure_dir, save_json, append_csv, utc_now

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
CITY = os.getenv("CITY", "Mumbai")
OUTPUT_DIR = "data/aqi"
