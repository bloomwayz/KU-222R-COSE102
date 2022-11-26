#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

###############################################################################
def word_count(filename):
    """ 단어 빈도 dictionary를 생성한다. (key: word, value: frequency)
    
    filename: input file
    return value: a sorted list of tuple (word, frequency) 
    """
    
    dic = {}
    res = []
    
    with open(filename) as fin:
    
        for line in fin:
            word = line.strip()
            dic[word] = dic.get(word, 0) + 1

        for word in dic:
            res.append((word, dic[word]))

    return sorted(res)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    result = word_count(sys.argv[1])

    # list of tuples
    for w, freq in result:
        print("%s\t%d" %(w, freq))