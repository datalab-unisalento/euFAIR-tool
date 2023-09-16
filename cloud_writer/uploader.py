import datetime
import os
import re

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials


# def upload(file_name):
#     file_path = 'temp/' + file_name + '.txt'
#
#     credentials = Credentials.from_service_account_file('settings/eufair-392011-74f8c95b8628.json')
#
#     drive_service = build('drive', 'v3', credentials=credentials)
#
#     media = MediaFileUpload(file_path, resumable=True)
#
#     body = {'name': file_name, 'parents': [folder_id/file_name]}
#
#     request = drive_service.files().create(body=body, media_body=media)
#     response = None
#     while response is None:
#         status, response = request.next_chunk()
#         if status:
#             print(f"Caricamento in corso: {int(status.progress() * 100)}%")
#     print(f"Caricamento completato. ID del file: {response['id']}")
#
def upload(file_name, dataset_id, drive_service, type='txt'):
    folder_id = '1F3Nc-LvW2xWJSycXrsWALQ3q920Zi_eB'
    file_path = 'temp/' + file_name + '.'+  type

    # Controlla se la sottocartella esiste già nella cartella principale
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{dataset_id}'"
    response = drive_service.files().list(q=query).execute()

    if 'files' in response and len(response['files']) > 0:
        subfolder = response['files'][0]
        print(f"La sottocartella '{dataset_id}' esiste già con l'ID: {subfolder['id']}")
    else:
        # Crea la sottocartella nella cartella principale
        subfolder_metadata = {
            'name': dataset_id,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        subfolder = drive_service.files().create(body=subfolder_metadata, fields='id').execute()
        print(f"Sottocartella '{dataset_id}' creata con l'ID: {subfolder['id']}")

    # Carica il file nella sottocartella
    media = MediaFileUpload(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [subfolder['id']]
    }
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File '{file_name}' caricato nella sottocartella con l'ID: {uploaded_file['id']}")

    return uploaded_file['id']




