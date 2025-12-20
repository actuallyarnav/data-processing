import os

from dotenv import load_dotenv

load_dotenv()
UPLOAD_FOLDER = "./static/uploads/"
MAX_CONTENT_LENGTH = 10 * 1000 * 1000
SECRET_KEY = os.getenv("SECRET_KEY")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
