from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials


def start():
    # Imposta le credenziali dell'account di servizio
    credentials = Credentials.from_service_account_file('settings/eufair-392011-74f8c95b8628.json')

    # Crea un'istanza dell'API di Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    return drive_service