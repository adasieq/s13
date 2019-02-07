# -*- coding: utf-8 -*-

import datetime
import re

from s13.ggauth.serv import get_sheet_service, write_data


def parset_territory_sheet(spreadsheet_id):
    s = get_sheet_service()

    get_next = True
    row_nr = 1
    # while get_next:
    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A:A').execute()
    # print result['values'], len(result['values'])
    val = result['values']
    real_val = []
    for l in val:
        if not l:
            break
        real_val.append(l)

    # print real_val, len(real_val)
    #    row_nr += 1

    # for r in xrange(1, len(real_val)):
    #     result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='{row}:{row}'.format(row=r)).execute()
    #     print result['values']

    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                           range='{row1}:{row2}'.format(row1=1, row2=142)).execute()
    cnt = 0
    for terr_number in result['values']:
        cnt += 1
        # ter1 = result['values'][105]
        print "TERREENNNNNNN", cnt
        ter1 = terr_number
        x = 0
        re_last_name = re.compile(r'(\D+\s?.+\s?\D+$)|(Grupa\s+\d+)')
        re_is_grupa = re.compile(r'Grupa\s+(\d+)')
        re_assigned = re.compile('P\s+(\d{2}.\d{2}.\d{2})')
        re_report = re.compile(r'O\s+(\d{2}.\d{2}.\d{2})')
        re_release = re.compile(r'Z\s+(\d{2}.\d{2}.\d{2})')
        last_name = None
        last_name2 = None
        assigned_to = None
        reported = None
        released = None
        reported2 = None
        for field in ter1:

            if x == 0:
                address = field
                # print address
            if re_last_name.match(field):
                last_name = field
                # print 'Kto', last_name
            if re_assigned.match(field):
                assigned_to = re_assigned.match(field).groups()[0]
                # print 'Pobrany', assigned_to
            if re_report.match(field):
                reported = re_report.match(field).groups()[0]
            if re_release.match(field):
                released = re_release.match(field).groups()[0]
                # print 'Zdany', released

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
            elif last_name and assigned_to and reported is None and released is None:
                print (assigned_to, None, last_name, 5)
                reported = None
                reported2 = None
                released = None

            # elif last_name and assigned_to:
            #     print (assigned_to, last_name)

            # print field
            x += 1

    # print result['values'][1]
    # sheet_metadata = s.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    # sheets = sheet_metadata.get('sheets', '')
    #
    # print sheets


def parset_territory_sheet2(spreadsheet_id):
    s = get_sheet_service()

    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                           range='{row1}:{row2}'.format(row1=1, row2=142)).execute()
    cnt = 0
    terr_list = {}
    for terr_number in result['values']:
        cnt += 1
        print "TERREENNNNNNN", cnt
        ter1 = terr_number
        x = 0
        re_last_name = re.compile(r'(\D+\s?.+\s?\D+$)|(Grupa\s+\d+)')
        re_is_grupa = re.compile(r'Grupa\s+(\d+)')
        re_date = re.compile(r'(\d+.\d+.\d+)')
        ind = 1
        assigned_field_indexes = []
        name = None
        start = None
        end = None
        for field in ter1[1:]:
            if len(field) == 0:
                ind += 1
                print "SKUPUJE POLE: ", field
                continue

            if re_last_name.match(field):
                name = field
                start = None
                end = None
                ind += 1
                continue

            if name and start is None:
                start = ind
                ind += 1

                if ind == len(ter1):
                    assigned_field_indexes.append((start, None, name))
                continue

            if start:
                end = ind

            if start and end:
                assigned_field_indexes.append((start, end, name))
                start = end
                end = None
            ind += 1

        terr_report = []
        for start, end, who in assigned_field_indexes:
            print who, start, end
            if start is not None:
                start = ter1[start]
                print start
                start = re_date.findall(start)[0]
            else:
                start = ""

            if end is not None:
                end = ter1[end]
                print end
                end = re_date.findall(end)[0]
            else:
                end = ""

            if re_is_grupa.match(who):
                group = re_is_grupa.findall(who)[0]
                who = ""
            else:
                group = ""

            if len(start) > 0 and len(end) > 0:
                start_d = datetime.datetime.strptime(start, "%d.%m.%y")
                end_d = datetime.datetime.strptime(end, "%d.%m.%y")
                diff_d = end_d - start_d
                if diff_d.days < 5:
                    continue

            if len(start) > 0:
                start_d = datetime.datetime.strptime(start, "%d.%m.%y")
                start_s = start_d.strftime("%y-%m-%d")

            if len(end) > 0:
                end_d = datetime.datetime.strptime(end, "%d.%m.%y")
                end_s = end_d.strftime("%y-%m-%d")

            terr_report.append((start_s, end_s, group, who))

        terr_list[cnt] = terr_report

    print terr_list
    #    sheet_metadata = s.spreadsheets().get(spreadsheetId="1ujLVxhSQI8BItXjpuh6gYnhJj7L5AxuKB4r7Vu6oqAA").execute()
    #   sheets = sheet_metadata.get('sheets', '')
    #  print sheets

    for terr_nr, terr_data in terr_list.items():
        print terr_nr, terr_data
        write_data(spreadsheet_id="1ujLVxhSQI8BItXjpuh6gYnhJj7L5AxuKB4r7Vu6oqAA",
                   cell_range='Teren nr {nr}!A7:E'.format(nr=terr_nr),
                   cell_values=terr_data,
                   valueInputOption='USER_ENTERED')
        #break

if __name__ == '__main__':
    parset_territory_sheet2('11h97D1pRhL8mhfhWee29ppNvBCYMvuslStE0gg4aHck')
