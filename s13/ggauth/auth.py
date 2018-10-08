from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('/tmp/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('S13tools-17aa94075be4.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    print(service)
    # Call the Sheets API
    SAMPLE_SPREADSHEET_ID = '1mvnafi71D0iNt_PkreBVnWFoq0Ctf6UGDkapwm6TE9s'
    SAMPLE_RANGE_NAME = 'Class Data!A2:E'
    result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                 range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print("No data found.")
    else:
        print("Name, Major:")
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print("%s, %s" % (row[0], row[4]))


if __name__ == '__main__':
    main()
