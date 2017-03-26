# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    letter_distribution.py: Creates a distribution of letters
    Date Created: 3/25/17
"""

__author__ = "Parang Saraf"
__email__ = "parang@vt.edu"


import json
import codecs
import argparse
import string


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', metavar='input', type=str, required=True, help='input')
    args = ap.parse_args()

    letters = {}
    alphabets = set(string.ascii_lowercase)
    print(sorted(alphabets))
    print("\n\n")
    # outfile = open(args.output, "w")
    with codecs.open(args.input, encoding='utf8', mode='r') as infile:
        for line in infile:
            word = line.strip().lower()
            word_list = list(word)
            for ltr in word_list:
                if ltr.strip() == "":
                    continue
                if ltr not in alphabets:
                    continue
                if ltr not in letters:
                    letters[ltr] = 0
                letters[ltr] += 1

    min_val = min(letters.values())
    for ltr in sorted(letters):
        print("%s: %d" % (ltr, letters[ltr]))
    print("\n\n")
    print(min_val)
    print("\n\n")
    for ltr in letters:
        letters[ltr] = letters[ltr]//min_val

    print(json.dumps(sorted(letters.items())))

            # toWrite = {}
            # outfile.write(json.dumps(toWrite, encoding='utf8', ensure_ascii=False).encode('utf8') + "\n")
    # outfile.close()