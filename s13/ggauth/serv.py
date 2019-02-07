# -*- coding: utf-8 -*-


import os

from apiclient import discovery
from google.oauth2 import service_account

from s13.settings import BASE_DIR

CREDENTIALS_DIR = 'credentials'
CLIENT_SECRET_FILE = 's13tools-1539004880862-aeb341ef245e.json'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


def get_spreadsheet_credentials():
    credential_path = os.path.join(BASE_DIR, 's13', 'ggauth', CREDENTIALS_DIR, CLIENT_SECRET_FILE)
    credentials = service_account.Credentials.from_service_account_file(credential_path, scopes=[SCOPES])
    # delegated_credentials = credentials.with_subject('agilo-service-account@open-e.com')

    return credentials


def get_sheet_service():
    """
    Gets google spreadsheet service.
    """

    credentials = get_spreadsheet_credentials()
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service


def read_data(spreadsheet_id, cell_range):
    s = get_sheet_service()
    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()

    return result


def write_data(spreadsheet_id, cell_range, cell_values, valueInputOption='RAW'):
    s = get_sheet_service()

    # cell_values = [[value], ]
    body = {'values': cell_values,
            }

    s.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                     range=cell_range,
                                     valueInputOption=valueInputOption,
                                     body=body
                                     ).execute()
