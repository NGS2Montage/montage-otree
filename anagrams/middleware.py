#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from django.http import HttpResponseServerError

from anagrams.models import Dictionary


class CheckDictionaryMiddleware(object):

    synced = None

    def process_request(self, request):
        if not CheckDictionaryMiddleware.synced:
            db_word_count = Dictionary.objects.all().count()
            if db_word_count == 0:
                msg = (
                    "Your database is not ready. There are zero dictionary "
                    "words loaded for the anagrams game. "
                )
                return HttpResponseServerError(msg)
            else:
                CheckDictionaryMiddleware.synced = True
