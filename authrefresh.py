import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)
    print("✅ New token.pickle generated successfully.")

if __name__ == "__main__":
    # delete old token if it exists
    if os.path.exists("token.pickle"):
        os.remove("token.pickle")
        print("⚠️ Old token.pickle deleted.")
    generate_token()
