import io

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def search_folder_and_get_latest_file(dataset_id, cat, drive_service):
    folder_id = '1F3Nc-LvW2xWJSycXrsWALQ3q920Zi_eB'

    # Cerca la cartella con il nome specificato
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{dataset_id}'"
    response = drive_service.files().list(q=query).execute()

    if 'files' in response and len(response['files']) > 0:
        subfolder = response['files'][0]
        print(f"Trovata la sottocartella '{dataset_id}' con l'ID: {subfolder['id']}")

        # Cerca il file più recente nella sottocartella che inizia con la stringa specificata
        query = f"'{subfolder['id']}' in parents and name contains '{cat + '-'}'"
        response = drive_service.files().list(q=query, orderBy='createdTime desc', pageSize=1).execute()

        if 'files' in response and len(response['files']) > 0:
            file = response['files'][0]
            print(f"Trovato l'ultimo file '{file['name']}' con l'ID: {file['id']}")
            return file['id']
        else:
            print(f"Nessun file trovato nella sottocartella '{dataset_id}' che inizia con '{cat + '-'}'")
            return None
    else:
        print(f"Nessuna sottocartella trovata con il nome '{dataset_id}' nella cartella principale")
        return None


def  download_file(file_id, drive_service):
    # Imposta le credenziali dell'account di servizio
    credentials = Credentials.from_service_account_file('settings/eufair-392011-74f8c95b8628.json')

    # Crea un'istanza dell'API di Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    # Scarica il file dal suo ID
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO('temp/' + file_id + '.txt', 'wb')
    downloader = drive_service.files().get_media(fileId=file_id)
    downloader_fh = downloader.execute()
    fh.write(downloader_fh)
    fh.close()

    return file_id