# -*- coding: utf-8 -*-


from django.views.generic import TemplateView

from s13.ggauth.serv import read_data, write_data

SPR_ID = '1YdONL1e6Hv7FjZzu-5QacL95VtRQJsBXbDgAaMLl1SY'
TEREN_NR = 1
TEST_DATA = '12-12-2018'


class AddTeritorryCardData(TemplateView):
    template_name = "add_territory_card_data.html"

    def get_context_data(self):
        data = read_data(SPR_ID, 'Teren nr {teren_nr}!A:A'.format(teren_nr=TEREN_NR))
        print data.values()[1]
        next_pos = len(data.values()[1]) + 1
        print 'next pos: ', next_pos
        context = dict()
        context['data'] = data.values()[1]

        write_data(SPR_ID, 'Teren nr {teren_nr}!A{pos}:A{pos}'.format(teren_nr=TEREN_NR,
                                                                      pos=next_pos), cell_values=[[TEST_DATA], ])

        return context
