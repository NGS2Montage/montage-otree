# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    clean_txt_files: 
    Date Created: 3/4/17
"""

__author__ = "Parang Saraf"
__email__ = "parang@vt.edu"

import json
import codecs
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-t1', '--text1', metavar='text1', type=str, required=True, help='text1')
    ap.add_argument('-t2', '--text2', metavar='text2', type=str, required=True, help='text2')
    ap.add_argument('-t3', '--text3', metavar='text3', type=str, required=True, help='text3')
    ap.add_argument('-o', '--output', metavar='output', type=str, required=True, help='output')
    args = ap.parse_args()

    dictionary = set()

    with codecs.open(args.text1, encoding='utf8', mode='r') as infile:
        for line in infile:
            word = line.strip().lower()
            if word == "":
                continue
            dictionary.add(line.strip())

    print "total words read after first file: %d" % len(dictionary)

    count = 0
    with codecs.open(args.text2, encoding='utf8', mode='r') as infile:
        for line in infile:
            word = line.strip().lower()
            if word == "":
                continue
            dictionary.add(line.strip())
            count += 1

    print "total words read after first file: %d\nwords added: %d\nTotal Words: %d" % (count, len(dictionary) - count, len(dictionary))

    count = 0
    with codecs.open(args.text3, encoding='utf8', mode='r') as infile:
        for line in infile:
            word = line.strip().lower()
            if word == "":
                continue
            dictionary.add(line.strip())
            count += 1

    print "total words read after first file: %d\nwords added: %d\nTotal Words: %d" % (count, len(dictionary) - count, len(dictionary))

    outfile = open(args.output, "w")
    sorted_dic = sorted(list(dictionary))
    for word in sorted_dic:
        outfile.write(word.encode('utf8') + "\n")
    outfile.close()
