import os
from dotenv import load_dotenv

load_dotenv()

scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
interval = 10
email = os.getenv("email")
sound = "sound.wav"
disc_token = os.getenv("disc_token")

creds_path = "credentials/credentials.json"
token_path = "credentials/token.json"