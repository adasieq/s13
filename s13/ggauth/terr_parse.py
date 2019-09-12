# -*- coding: utf-8 -*-

import datetime
import re

from s13.ggauth.serv import get_sheet_service, write_data, clear_data


def parset_territory_sheet(spreadsheet_id):
    s = get_sheet_service()

    result = s.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                           range='{row1}:{row2}'.format(row1=1, row2=142)).execute()
    cnt = 0
    terr_list = {}
    for terr_number in result['values']:
        cnt += 1
        print "TEREN =========> ", cnt
        ter1 = terr_number
        x = 0
        re_last_name = re.compile(r'(\D+\s?.+\s?\D+$)|(Grupa\s+\d+)')
        re_is_grupa = re.compile(r'Grupa\s+(\d+)')
        re_assigned_date = re.compile('P\s+(\d+.\d+.\d+)')
        re_report_date = re.compile(r'O\s+(\d+.\d+.\d+)')
        re_release_date = re.compile(r'Z\s+(\d+.\d+.\d+)')
        re_date = re.compile(r'(\d+.\d+.\d+)')
        ind = 1
        assigned_field_indexes = []
        name = None
        start = None
        end = None
        in_progress = False
        for field in ter1[1:]:
            if len(field) == 0:
                ind += 1
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
                print 'end', ind, len(ter1)
                if ind + 1 == len(ter1):
                    if re_report_date.match(field):
                        in_progress = True

            if start and end:
                assigned_field_indexes.append((start, end, name))
                if in_progress:
                    assigned_field_indexes.append((end, None, name))
                start = end
                end = None
            ind += 1

        terr_report = []

        for start, end, who in assigned_field_indexes:
            is_assigned_date = False
            start_s = ""
            end_s = ""
            print who, start, end
            if start is not None:
                start = ter1[start]
                print start
                is_assigned_date = re_assigned_date.match(start)
                start = re_date.findall(start)[0]
            else:
                start = ""

            if end is not None:
                end = ter1[end]
                print end
                if re_release_date.match(end) and not is_assigned_date:
                    end = ""
                    continue
                else:
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
                if diff_d.days < 8:
                    continue

            if len(start) > 0:
                start_d = datetime.datetime.strptime(start, "%d.%m.%y")
                start_s = start_d.strftime("%y-%m-%d")

            if len(end) > 0:
                end_d = datetime.datetime.strptime(end, "%d.%m.%y")
                end_s = end_d.strftime("%y-%m-%d")

            terr_report.append((start_s, end_s, group, who))

        print terr_report
        terr_list[cnt] = terr_report

    for terr_nr, terr_data in terr_list.items():
        print terr_nr, terr_data
        clear_data(spreadsheet_id="1xU4ZVRD7KjataiPoFR4XMFaBP90wY01XcNfoSSTFZeE",
                   cell_range='Teren nr {nr}!A7:E'.format(nr=terr_nr))
        write_data(spreadsheet_id="1xU4ZVRD7KjataiPoFR4XMFaBP90wY01XcNfoSSTFZeE",
                   cell_range='Teren nr {nr}!A7:E'.format(nr=terr_nr),
                   cell_values=terr_data,
                   valueInputOption='USER_ENTERED')


if __name__ == '__main__':
    parset_territory_sheet('11h97D1pRhL8mhfhWee29ppNvBCYMvuslStE0gg4aHck')
