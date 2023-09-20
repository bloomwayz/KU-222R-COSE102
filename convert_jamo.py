#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

_CHO_ = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
_JUNG_ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
_JONG_ = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # index를 1부터 시작해야 함

# 겹자음 : 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
# 겹모음 : 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ'

_JAMO2ENGKEY_ = {
 'ㄱ': 'r',
 'ㄲ': 'R',
 'ㄴ': 's',
 'ㄷ': 'e',
 'ㄸ': 'E',
 'ㄹ': 'f',
 'ㅁ': 'a',
 'ㅂ': 'q',
 'ㅃ': 'Q',
 'ㅅ': 't',
 'ㅆ': 'T',
 'ㅇ': 'd',
 'ㅈ': 'w',
 'ㅉ': 'W',
 'ㅊ': 'c',
 'ㅋ': 'z',
 'ㅌ': 'x',
 'ㅍ': 'v',
 'ㅎ': 'g',
 'ㅏ': 'k',
 'ㅐ': 'o',
 'ㅑ': 'i',
 'ㅒ': 'O',
 'ㅓ': 'j',
 'ㅔ': 'p',
 'ㅕ': 'u',
 'ㅖ': 'P',
 'ㅗ': 'h',
 'ㅘ': 'hk',
 'ㅙ': 'ho',
 'ㅚ': 'hl',
 'ㅛ': 'y',
 'ㅜ': 'n',
 'ㅝ': 'nj',
 'ㅞ': 'np',
 'ㅟ': 'nl',
 'ㅠ': 'b',
 'ㅡ': 'm',
 'ㅢ': 'ml',
 'ㅣ': 'l',
 'ㄳ': 'rt',
 'ㄵ': 'sw',
 'ㄶ': 'sg',
 'ㄺ': 'fr',
 'ㄻ': 'fa',
 'ㄼ': 'fq',
 'ㄽ': 'ft',
 'ㄾ': 'fx',
 'ㄿ': 'fv',
 'ㅀ': 'fg',
 'ㅄ': 'qt'
}


###############################################################################
def is_hangeul_syllable(ch):
    '''한글 음절인지 검사
    '''
    if not isinstance(ch, str):
        return False
    elif len(ch) > 1:
        ch = ch[0]
    
    return 0xAC00 <= ord(ch) <= 0xD7A3

###############################################################################
def compose(cho, jung, jong):
    '''초성, 중성, 종성을 한글 음절로 조합
    cho : 초성
    jung : 중성
    jong : 종성
    return value: 음절
    '''
    if not (0 <= cho <= 18 and 0 <= jung <= 20 and 0 <= jong <= 27):
        return None
    code = (((cho * 21) + jung) * 28) + jong + 0xAC00

    return chr(code)

###############################################################################
# input: 음절
# return: 초, 중, 종성
def decompose(syll):
    '''한글 음절을 초성, 중성, 종성으로 분해
    syll : 한글 음절
    return value : tuple of integers (초성, 중성, 종성)
    '''
    if not is_hangeul_syllable(syll):
        return (None, None, None)
    
    uindex = ord(syll) - 0xAC00
    
    jong = uindex % 28
    jung = ((uindex - jong) // 28) % 21
    cho = ((uindex - jong) // 28) // 21

    return (cho, jung, jong)

###############################################################################
def str2jamo(str):
    '''문자열을 자모 문자열로 변환
    '''
    jamo = []
    for ch in str:
        if is_hangeul_syllable(ch):
            cho, jung, jong = decompose(ch)
            jamo.append( _CHO_[cho])
            jamo.append( _JUNG_[jung])
            if jong != 0:
                jamo.append( _JONG_[jong-1])
        else:
            jamo.append(ch)
    return ''.join(jamo)

###############################################################################
def jamo2engkey(str):
    res = []
    for ch in str:
        if ch in _JAMO2ENGKEY_:
            res.append(_JAMO2ENGKEY_[ch])
            continue
        res.append(ch)

    return ''.join(res)


def engkey2jamo(str):
    res = []
    for ch in str:
        flag = True
        for k, v in _JAMO2ENGKEY_.items():
            if v == ch:
                res.append(k)
                flag = False
                break
        if flag:
            res.append(ch)

    return ''.join(res)


def jamo2syllable(str):
    res = []
    temp = []
    stat = 0

    for ch in str:
        if stat == 0:
            if ch in _CHO_:
                temp.append(ch)
                stat = 1
            elif ch in _JUNG_:
                temp.append(ch)
                stat = 2
            else:
                res.append(ch)

        elif stat == 1:
            if ch in _CHO_:
                temp.append(ch)
            elif ch in _JUNG_:
                while True:
                    if len(temp) == 2:
                        res.append(temp[0])
                        del temp[0]
                        break
                    if len(temp) == 1:
                        break
                    if join_double(temp[0], temp[1]):
                        res.append(join_double(temp[0], temp[1]))
                        del temp[:2]
                        continue
                    res.append(temp[0])
                    del temp[0]
                temp.append(ch)
                stat = 2
            else:
                while True:
                    if len(temp) == 0:
                        break
                    if join_double(temp[0], temp[1]):
                        res.append(join_double(temp[0], temp[1]))
                        del temp[:2]
                        continue
                    res.append(temp[0])
                    del temp[0]
                res.append(ch)
                stat = 0

        elif stat == 2:
            if ch in _CHO_:
                if len(temp) == 1:
                    res.append(temp[0])
                    temp[0] = ch
                    stat = 1
                elif len(temp) == 2:
                    temp.append(ch)
                    stat = 4
            elif ch in _JUNG_:
                double = join_double(temp[-1], ch)
                if double:
                    temp[-1] = double
                    stat = 3
                else:
                    try:
                        res.append(compose_list(temp))
                    except:
                        res.append(temp[0])
                    res.append(ch)
                    temp = list()
                    stat = 0
            else:
                if len(temp) == 1:
                    res.append(temp[0])
                elif len(temp) == 2:
                    res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 3:
            if ch in _CHO_:
                if len(temp) == 1:
                    res.append(temp[0])
                    temp = list(ch)
                    stat = 1
                elif len(temp) == 2:
                    temp.append(ch)
                    stat = 4
            elif ch in _JUNG_:
                res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0
            else:
                if len(temp) == 1:
                    res.append(temp[0])
                elif len(temp) == 2:
                    res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 4:
            if ch in _CHO_:
                temp.append(ch)
                stat = 5
            elif ch in _JUNG_:
                res.append(compose_list(temp[:-1]))
                del temp[:-1]
                temp.append(ch)
                stat = 2
            else:
                res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 5:
            if ch in _CHO_:
                double = join_double(temp[-2], temp[-1])
                if double:
                    del temp[-2:]
                    temp.append(double)
                    res.append(compose_list(temp))
                    temp = list(ch)
                    stat = 1
                else:
                    res.append(compose_list(temp[:-1]))
                    res.append(temp[-1])
                    temp = list(ch)
                    stat = 1
            elif ch in _JUNG_:
                res.append(compose_list(temp[:-1]))
                del temp[:-1]
                temp.append(ch)
                stat = 2
            else:
                double = join_double(temp[-2], temp[-1])
                if double:
                    del temp[-2:]
                    temp.append(double)
                    res.append(compose_list(temp))
                else:
                    res.append(compose_list(temp[:-1]))
                    res.append(temp[-1])
                res.append(ch)
                temp = list()
                stat = 0
    
    if len(temp) > 0:
        compose_list(temp)

    return ''.join(res)

def jamo2syllable(str):
    res = []
    temp = []
    stat = 0

    for ch in str:
        if stat == 0:
            if ch in _CHO_:
                temp.append(ch)
                stat = 1
            elif ch in _JUNG_:
                temp.append(ch)
                stat = 2
            else:
                res.append(ch)

        elif stat == 1:
            if ch in _CHO_:
                temp.append(ch)
            elif ch in _JUNG_:
                while True:
                    if len(temp) == 2:
                        res.append(temp[0])
                        del temp[0]
                        break
                    if len(temp) == 1:
                        break
                    if join_double(temp[0], temp[1]):
                        res.append(join_double(temp[0], temp[1]))
                        del temp[:2]
                        continue
                    res.append(temp[0])
                    del temp[0]
                temp.append(ch)
                stat = 2
            else:
                while True:
                    if len(temp) == 0:
                        break
                    if len(temp) == 1:
                        res.append(temp[0])
                        temp = list()
                        break
                    if join_double(temp[0], temp[1]):
                        res.append(join_double(temp[0], temp[1]))
                        del temp[:2]
                        continue
                    res.append(temp[0])
                    del temp[0]
                res.append(ch)
                stat = 0

        elif stat == 2:
            if ch in _CHO_:
                if len(temp) == 1:
                    res.append(temp[0])
                    temp[0] = ch
                    stat = 1
                elif len(temp) == 2:
                    temp.append(ch)
                    stat = 4
            elif ch in _JUNG_:
                double = join_double(temp[-1], ch)
                if double:
                    temp[-1] = double
                    stat = 3
                else:
                    try:
                        res.append(compose_list(temp))
                    except:
                        res.append(temp[0])
                    temp = list(ch)
            else:
                if len(temp) == 1:
                    res.append(temp[0])
                elif len(temp) == 2:
                    res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 3:
            if ch in _CHO_:
                if len(temp) == 1:
                    res.append(temp[0])
                    temp = list(ch)
                    stat = 1
                elif len(temp) == 2:
                    temp.append(ch)
                    stat = 4
            elif ch in _JUNG_:
                try:
                    res.append(compose_list(temp))
                except:
                    res.append(temp[0])
                res.append(ch)
                temp = list()
                stat = 0
            else:
                if len(temp) == 1:
                    res.append(temp[0])
                elif len(temp) == 2:
                    res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 4:
            if ch in _CHO_:
                temp.append(ch)
                stat = 5
            elif ch in _JUNG_:
                res.append(compose_list(temp[:-1]))
                del temp[:-1]
                temp.append(ch)
                stat = 2
            else:
                res.append(compose_list(temp))
                res.append(ch)
                temp = list()
                stat = 0

        elif stat == 5:
            if ch in _CHO_:
                double = join_double(temp[-2], temp[-1])
                if double:
                    del temp[-2:]
                    temp.append(double)
                    res.append(compose_list(temp))
                    temp = list(ch)
                    stat = 1
                else:
                    res.append(compose_list(temp[:-1]))
                    if join_double(temp[-1], ch):
                        del temp[:-1]
                        temp.append(ch)
                    else:
                        res.append(temp[-1])
                        temp = list(ch)
                    stat = 1
            elif ch in _JUNG_:
                res.append(compose_list(temp[:-1]))
                del temp[:-1]
                temp.append(ch)
                stat = 2
            else:
                double = join_double(temp[-2], temp[-1])
                if double:
                    del temp[-2:]
                    temp.append(double)
                    res.append(compose_list(temp))
                else:
                    res.append(compose_list(temp[:-1]))
                    res.append(temp[-1])
                res.append(ch)
                temp = list()
                stat = 0
    
    if len(temp) == 1:
        res.append(temp[0])
    elif len(temp) > 1:
        if stat == 1:
            while len(temp) > 0:
                if len(temp) == 1:
                    res.append(temp[0])
                    break
                if join_double(temp[0], temp[1]):
                    res.append(join_double(temp[0], temp[1]))
                    del temp[:2]
                    continue
                res.append(temp[0])
                del temp[0]
        elif stat == 5:
            double = join_double(temp[-2], temp[-1])
            if double:
                del temp[-2:]
                temp.append(double)
                res.append(compose_list(temp))
            else:
                res.append(compose_list(temp[:-1]))
                res.append(temp[-1])
        else:
            res.append(compose_list(temp))

    return ''.join(res)

def join_double(ch1, ch2):
    s = ch1 + ch2
    for k, v in _JAMO2ENGKEY_.items():
        if v == jamo2engkey(s):
            return k
    return False

def compose_list(t):
    onset = _CHO_.index(t[0])
    nucleus = _JUNG_.index(t[1])
    try:
        coda = _JONG_.index(t[2])
        return compose(onset, nucleus, coda+1)
    except:
        try:
            return ''.join(compose(onset, nucleus, 0) + t[2])
        except:
            return compose(onset, nucleus, 0)

###############################################################################
if __name__ == "__main__":
    
    i = 0
    line = sys.stdin.readline()

    while line:
        line = line.rstrip()
        i += 1
        print('[%06d:0]\t%s' %(i, line)) # 원문
    
        # 문자열을 자모 문자열로 변환 ('닭고기' -> 'ㄷㅏㄺㄱㅗㄱㅣ')
        jamo_str = str2jamo(line)
        print('[%06d:1]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 키입력 문자열로 변환 ('ㄷㅏㄺㄱㅗㄱㅣ' -> 'ekfrrhrl')
        key_str = jamo2engkey(jamo_str)
        print('[%06d:2]\t%s' %(i, key_str)) # 키입력 문자열
        
        # 키입력 문자열을 자모 문자열로 변환 ('ekfrrhrl' -> 'ㄷㅏㄹㄱㄱㅗㄱㅣ')
        jamo_str = engkey2jamo(key_str)
        print('[%06d:3]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 음절열로 변환 ('ㄷㅏㄹㄱㄱㅗㄱㅣ' -> '닭고기')
        syllables = jamo2syllable(jamo_str)
        print('[%06d:4]\t%s' %(i, syllables)) # 음절열

        line = sys.stdin.readline()
