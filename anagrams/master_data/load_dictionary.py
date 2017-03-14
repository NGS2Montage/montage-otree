import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ngs2.settings")

import django
django.setup()

import codecs
import argparse

from anagrams.models import Dictionary


def load_dictionary(filename):
    with codecs.open(filename, encoding='utf8', mode='r') as infile:
        for num, line in enumerate(infile):
            if num % 10000 == 0:
                print "\n" + "-"*80 + "\n"
                print num
                print "\n" + "-" * 80 + "\n"
            word = line.strip().lower()
            if word == "":
                continue
            wordObj, created = Dictionary.objects.get_or_create(word=word)
            #print wordObj, created


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-dic', '--dictionary', metavar='dictionary', type=str, required=True, help='dictionary')
    args = ap.parse_args()

    load_dictionary(args.dictionary)
