import csv
from datetime import datetime, date

from otree.api import Currency
from otree.common import RealWorldCurrency
from otree.models.session import Session
from otree.models_concrete import PageCompletion

from django.http import HttpResponse

import vanilla



class CompletedSessionSummaryExport(vanilla.View):

    url_name = 'completed_session_summary_export'
    url_pattern = '^completed_session_summary_export/$'
    display_name = 'Completed Session Summary Export'

    def get(request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'CompletedSessionSummary (accessed {}).csv'.format(
                date.today().isoformat()
            )
        )

        def ParticipantsData(P):
            consent = []
            playing = []
            payoff = {}
            for p in P:
                if p.vars['consent']:
                    consent.append(p.code)
                    payoff[p.code] = p.payoff_plus_participation_fee()
                if p.vars['playing']:
                    playing.append(p.code)
                    
            return consent, playing, payoff
        
        
        def getStartStopTime(P):
            start_time = datetime.now()
            duration = []
            for p in P:
                Times = PageCompletion.objects.filter(participant__code=p).order_by('time_stamp').values_list('time_stamp', flat=True)
                Times = [datetime.fromtimestamp(x) for x in Times]
                start_time = min(start_time, min(Times))
                duration.append((max(Times) - start_time).seconds/60.)

            if len(duration):
                duration = sum(duration)/len(duration)
            else:
                duration = 0

            start_time = start_time.strftime("%m-%d-%Y %H:%M")

            return start_time, duration
        
        S = Session.objects.all()
        
        data = []
        for s in S:
            
            if s.mturk_HITId:
                code = s.code 
                requested_participants = len(s.get_participants())/2

                P = s.get_participants()
                consent, playing, payoff = ParticipantsData(P)

                total_cost = sum(payoff.values())

                start_time, duration = getStartStopTime(playing)

                data.append({
                    'session_code': code,
                    'experiment_type': s.config['display_name'],
                    'n_part_requested': requested_participants,
                    'n_part_consented': len(consent),
                    'n_part_finished': len(playing),
                    'start_time': start_time,
                    'duration': duration,
                    'total_cost': total_cost,
                })

        keys_order = ['session_code', 
                     'experiment_type', 
                     'n_part_requested', 
                     'n_part_consented', 
                     'n_part_finished', 
                     'start_time', 
                     'duration', 
                     'total_cost']
        
        w = csv.DictWriter(response, keys_order)
        w.writeheader()
        
        if data:
            w.writerows(data)

        return response
