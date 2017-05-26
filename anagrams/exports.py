import csv
import datetime

from django.http import HttpResponse

import vanilla

from .models import UserLetter, TeamWord, LetterTransaction


class UserLetterExport(vanilla.View):

    url_name = 'anagrams_userletter_export'
    url_pattern = '^anagrams_userletter_export/$'
    display_name = 'Anagrams User Letter export'

    def get(request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'User letters (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )

        column_names = [
            'player__participant__session__code',
            'player__participant__session_id',
            'player__participant__id_in_session',
            'player__participant__code',
            'letter',
        ]

        rows = UserLetter.objects.values_list(*column_names)

        writer = csv.writer(response)
        writer.writerows([column_names])
        writer.writerows(rows)

        return response


class TeamWordExport(vanilla.View):

    url_name = 'anagrams_teamword_export'
    url_pattern = '^anagrams_teamword_export/$'
    display_name = 'Anagrams Team Word export'

    def get(request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'Team words (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )

        column_names = [
            'player__participant__session__code',
            'player__participant__session_id',
            'player__participant__id_in_session',
            'player__participant__code',
            'channel',
            'word',
            'timestamp'
        ]

        rows = TeamWord.objects.order_by('timestamp').values_list(*column_names)

        writer = csv.writer(response)
        writer.writerows([column_names])
        writer.writerows(rows)

        return response


class LetterTransactionExport(vanilla.View):

    url_name = 'anagrams_lettertransaction_export'
    url_pattern = '^anagrams_lettertransaction_export/$'
    display_name = 'Anagrams Letter Transaction export'

    def get(request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'Letter transactions (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )

        column_names = [
            'player__participant__code',
            'letter__player__participant__code',
            'letter__letter',
            'channel',
            'owner_channel',
            'approved',
            'timestamp'
        ]

        rows = LetterTransaction.objects.order_by('timestamp').values_list(*column_names)

        writer = csv.writer(response)
        writer.writerows([column_names])
        writer.writerows(rows)

        return response
