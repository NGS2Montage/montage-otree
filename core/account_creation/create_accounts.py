# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    create_accounts: Creates User Accounts
    Date Created: 3/18/17
"""

__author__ = "Parang Saraf"
__email__ = "parang@vt.edu"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()

from django.contrib.auth.models import User
from core.models import UserParticipantAssociation
from django.contrib.auth.tokens import default_token_generator
from otree.models import Session
from allauth.compat import reverse
from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from allauth.account.adapter import get_adapter

import codecs
import argparse


def get_session_id(session_name):
    for s in Session.objects.all():
        if s.config['name'] == session_name:
            return s
    print("Session: %s not found. Exiting" % session_name)
    exit(0)


def main(emails_file, session_name):

    session_id = get_session_id(session_name)

    with codecs.open(emails_file, encoding='utf8', mode='r') as infile:
        for line in infile:
            email = line.strip()
            try:
                u = User.objects.get(email=email)
                if not u.is_active:
                    user_present = False
                else:
                    user_present = True
            except Exception as err:
                user_present = False
            if user_present:
                print("User: %s is already present and active. Moving on." % email)
                continue
            user, created = User.objects.get_or_create(username=email, email=email, is_active=False)
            user.set_password(User.objects.make_random_password())
            user.save()

            user_association, created = UserParticipantAssociation.objects.get_or_create(user=user, session=session_id)
            user_association.session_name = session_name
            user_association.save()

            temp_key = default_token_generator.make_token(user)
            path = reverse('create_account_from_key', kwargs=dict(uid=user_pk_to_url_str(user), key=temp_key,
                                                                  sid=str(session_id.id)))
            url = build_absolute_uri(None, path)
            print("%s: %s" % (email, url))
            context = {'account_creation_url': url}
            get_adapter(None).send_mail(
                'account/email/account_creation_key',
                email,
                context
            )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-e', '--emails', metavar='emails', type=str, required=True, help='emails')
    ap.add_argument('-s', '--session', metavar='session', type=str, required=True, help='session')
    args = ap.parse_args()

    main(args.emails, args.session)
