from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import environ

env = environ.Env()
environ.Env.read_env()

CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")
REDIRECT_URI = env("REDIRECT_URI")

REFRESH_TOKEN = env("REFRESH_TOKEN")

credentials = service_account.Credentials.from_service_account_info(
    {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
)

drive_service = build("drive", "v3", credentials=credentials)


def upload_file():
    file_metadata = {
        "name": "My Report",
        "mimeType": "application/vnd.google-apps.spreadsheet",
    }
    media = MediaFileUpload("files/report.csv", mimetype="text/csv", resumable=True)
    file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print("File ID: %s" % file.get("id"))
