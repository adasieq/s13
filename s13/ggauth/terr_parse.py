# -*- coding: utf-8 -*-

from s13.ggauth.serv import get_sheet_service
from google.oauth2 import service_account
from apiclient import discovery
import re

def parset_territory_sheet(spreadsheet_id):
    s = get_sheet_service()

    get_next = True
    row_nr = 1
    #while get_next:
    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A:A').execute()
    #print result['values'], len(result['values'])
    val = result['values']
    real_val = []
    for l in val:
        if not l:
            break
        real_val.append(l)

    #print real_val, len(real_val)
    #    row_nr += 1

    # for r in xrange(1, len(real_val)):
    #     result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='{row}:{row}'.format(row=r)).execute()
    #     print result['values']

    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='{row1}:{row2}'.format(row1=1, row2=142)).execute()

    ter1 = result['values'][104]
    x = 0
    re_last_name = re.compile('(\D+\s?.+\s?\D+$)|(Grupa\s+\d+)')
    re_assigned = re.compile('P\s+(\d{2}.\d{2}.\d{2})')
    re_report = re.compile('O\s+(\d{2}.\d{2}.\d{2})')
    re_release = re.compile('Z\s+(\d{2}.\d{2}.\d{2})')
    last_name = None
    last_name2 = None
    assigned_to = None
    reported = None
    released = None
    reported2 = None
    for field in ter1:

        if x == 0:
            address = field
            #print address
        if re_last_name.match(field):
            last_name = field
            #print 'Kto', last_name
        if re_assigned.match(field):
            assigned_to = re_assigned.match(field).groups()[0]
            #print 'Pobrany', assigned_to
        if re_report.match(field):
            reported = re_report.match(field).groups()[0]
        if re_release.match(field):
            released = re_release.match(field).groups()[0]
            #print 'Zdany', released
        
        # if reported:
        #     reported2 = reported

        if last_name and assigned_to and reported:
            print (assigned_to, reported, last_name, 1)
            assigned_to = None
            reported2 = reported
            reported = None
        elif last_name and reported2 and reported:
            print (reported2, reported, last_name, 2)
            reported2 = reported
            reported = None
        elif last_name and released and (reported2 or reported):
            if reported2 == released:
                continue
            print (reported2 or reported, released, last_name, 3)
            last_name = None
            released = None
            reported = None
            reported2 = None
        elif last_name and assigned_to and released:
            print (assigned_to, released, last_name, 4)
            last_name = None
            assigned_to = None
            released = None
        # elif last_name and assigned_to:
        #     print (assigned_to, last_name)

        #print field
        x += 1

    #print result['values'][1]
    # sheet_metadata = s.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    # sheets = sheet_metadata.get('sheets', '')
    #
    # print sheets

if __name__ == '__main__':
    parset_territory_sheet('1aTtsVbBK8cUeA6F0Kmv8PD_PlTSAe00mDJ9AftqtChg')
