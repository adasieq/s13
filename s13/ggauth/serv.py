from httplib2 import Http

from googleapiclient.discovery import build
from oauth2client import file, client, tools
from google.oauth2 import service_account

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

flow = service_account.Credentials.from_service_account_file(
        'S13tools-17aa94075be4.json',
        scopes=[SCOPES])

store = file.Storage('/tmp/token2.json')
creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('S13tools-17aa94075be4.json', SCOPES)
#     creds = tools.run_flow(flow, store)
print flow
service = build('sheets', 'v4', credentials=flow)
print service


SAMPLE_SPREADSHEET_ID = '1mvnafi71D0iNt_PkreBVnWFoq0Ctf6UGDkapwm6TE9s'
SAMPLE_RANGE_NAME = 'Teren nr 1!A2:A5'
result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                             range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])
