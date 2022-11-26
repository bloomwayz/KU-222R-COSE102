#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 복수의 빈도 파일을 병합하는 프로그램

import sys
import heapq

###############################################################################
def merge_k_sorted_freq(input_files):
    '''
    input_files : list of input filenames (frequency files; 2 column format)
    '''
    fins = [] # list of file objects
    k = len(input_files)
    heap = []
    finished = [False for _ in range(k)] # [False] * k
    
    for fname in input_files:
        f = open(fname)
        fins.append(f)

    for index, fin in enumerate(fins):
        line = fin.readline()
        line = line.strip()
        line = line.split('\t')
        heapq.heappush(heap, (line[0], int(line[1]), index))
        
    prev, freq, i = heapq.heappop(heap)

    while finished != [True for _ in range(k)]:
            
        line = fins[i].readline()
        
        if not line:
            try:
                finished[i] = True
                term, ftemp, j = heapq.heappop(heap)
                
                if finished[j]:
                    continue
                    
                if term == prev:
                    freq += ftemp
                    
                else:
                    print(prev, freq, sep='\t')
                    prev = term
                    freq = ftemp
                    
                i = j
                continue

            except:
                print(prev, freq, sep='\t')
                break
            
        line = line.strip()
        line = line.split('\t')
        heapq.heappush(heap, (line[0], int(line[1]), i))
        
        term, ftemp, j = heapq.heappop(heap)
                
        if finished[j]:
            continue
                    
        if term == prev:
            freq += ftemp
                    
        else:
            print(prev, freq, sep='\t')
            prev = term
            freq = ftemp
                    
        i = j

    for i in range(k):
        fins[i].close()

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    merge_k_sorted_freq(sys.argv[1:])
