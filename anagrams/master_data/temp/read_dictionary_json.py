# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    read_dictionary_json: 
    Date Created: 3/4/17
"""

__author__ = "Parang Saraf"
__email__ = "parang@vt.edu"

import json
import codecs
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', metavar='input', type=str, required=True, help='input')
    ap.add_argument('-o', '--output', metavar='output', type=str, required=True, help='output')
    args = ap.parse_args()

    outfile = open(args.output, "w")
    with codecs.open(args.input, encoding='utf8', mode='r') as infile:
        for line in infile:
            event = json.loads(line, encoding='utf8')
            print event.keys()
            toWrite = {}
            outfile.write(json.dumps(toWrite, encoding='utf8', ensure_ascii=False).encode('utf8') + "\n")
    outfile.close()