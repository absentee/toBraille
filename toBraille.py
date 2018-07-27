# -*- coding:utf-8 -*-
# !/usr/bin/python

import re
import sys
from xpinyin import Pinyin
from dotsBraille import braille2dots


class KanjiToPinyin(object):
    def __init__(self):
        self.shengmu = None
        self.yunmu = None
        self.tone = None
        self.character = None
        self.pinyin = None
        self.braille = str
        self.break_flag = False

        self.tone_table = [
            (0, u"aoeiuv"),
            (1, u"\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6"),
            (2, u"\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8"),
            (3, u"\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da"),
            (4, u"\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc"),
        ]

        self.yunmu_table = ['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 'ue', 'er', 'an', 'en', 'in', 'un',
         'vn', 'ang', 'eng', 'ing', 'ong', 'ia', 'ian', 'iang', 'iao', 'iong', 'uai', 'ua', 'ue', 'uan', 'uang', 'uo', 'van']

    def get_pinyin(self, character):
        self.__init__()
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, character)
        my_re2 = re.compile(r'[0-9]', re.S)
        res2 = re.findall(my_re2, character)
        if len(res) or len(res2):
            return
        else:
            pass
        self.break_flag = False
        p = Pinyin()
        self.character = Character(character)
        pinyin_with_tone = p.get_pinyin(self.character.string, show_tone_marks=True, convert='lower')
        self.character.pinyin = pinyin_with_tone
        for letter in self.character.pinyin:
            n = 1
            for tones in self.tone_table[1:]:
                if letter in tones[1]:
                    self.character.tone = tones[0]
                    i = self.character.pinyin.index(letter)
                    j = tones[1].index(letter)
                    if i != 0:
                        if i + 1 != len(self.character.pinyin):
                            self.character.pinyin_notone = self.character.pinyin[0:i] + self.tone_table[0][1][j] + self.character.pinyin[i+1:]
                        else:
                            self.character.pinyin_notone = self.character.pinyin[0:i] + self.tone_table[0][1][j]
                    else:
                        if i + 1 != len(self.character.pinyin):
                            self.character.pinyin_notone = self.tone_table[0][1][j] +self.character.pinyin[i+1:]
                        else:
                            self.character.pinyin_notone = self.tone_table[0][1][j]
                    self.pinyin = self.character.pinyin_notone
                    self.break_flag = True

                if self.break_flag:
                    break
                n = n + 1
            if self.break_flag:
                break
        if n == 5:
            self.pinyin = self.character.pinyin
            self.tone = 0
        else:
            self.tone = n

    def divide_pinyin(self):
        if self.pinyin is None:
            return
        else:
            pass
        for letter in self.pinyin:
            if letter in self.yunmu_table:
                pos = self.pinyin.index(letter)
                break
        if pos != 0:
            self.shengmu = self.pinyin[0: pos]
            self.yunmu = self.pinyin[pos:]
        else:
            self.yunmu = self.pinyin

    def get_modified(self):
        if self.pinyin is None:
            return
        else:
            pass
        if self.character.string == '是':
            self.shengmu = 'sh'
            self.yunmu = None
            self.tone = None
        elif self.character.string == '的':
            self.shengmu = 'd'
            self.yunmu = None
            self.tone = None
        if self.shengmu == 'y':
            self.shengmu = None
            if self.yunmu[0] == 'u':
                self.yunmu = 'v'
            elif self.yunmu[0] == 'i':
                pass
            else:
                self.yunmu = 'i' + self.yunmu
        elif self.shengmu == 'w':
            self.shengmu = None
            if self.yunmu[0] == 'u':
                pass
            else:
                self.yunmu = 'u' + self.yunmu

        if self.yunmu in ['iou', 'uei', 'uen']:
            self.yunmu = self.yunmu[0] + self.yunmu[2]

        if self.yunmu == 'u':
            if self.shengmu in ['j', 'q', 'x']:
                self.yunmu = 'v'
            else:
                pass

        try:
            self.pinyin = self.shengmu + self.yunmu
        except:
            if self.shengmu is None:
                self.pinyin = self.yunmu
            elif self.yunmu is None:
                self.pinyin = self.shengmu
            else:
                pass

    def transfer(self, character):
        if character != '':
            self.get_pinyin(character)
            self.divide_pinyin()
            self.get_modified()
        else:
            print('The word in empty!')
            sys.exit()
        return (self.shengmu, self.yunmu, self.tone)


class Pinyin2Braille:
    def __init__(self):
        self.shengmu = None
        self.shengmu_symbol = None
        self.yunmu = None
        self.yunmu_symbol = None
        self.tone = None
        self.tone_symbol = None
        self.braille = None
        self.dots = None

        self.shengmu_trans_table = [
            ('b', 'b'), ('p', 'p'), ('m', 'm'), ('f', 'f'), ('d', 'd'), ('t', 't'), ('n', 'n'), ('l', 'l'), ('g', 'g'),
            ('k', 'k'), ('h', 'h'), ('j', 'g'), ('q', 'k'), ('x', 'h'), ('zh', '/'), ('ch', 'q'), ('sh', ':'),
            ('r', 'j'), ('z', 'z'), ('c', 'c'), ('s', 's'), ('y', 'i'), ('w', 'u'),
        ]

        self.yunmu_trans_table = [
            ('a', '9'), ('o', '5'), ('e', '5'), ('i', 'i'), ('u', 'u'), ('v', '+'), ('ai', '['), ('ei', '!'),
            ('ui', 'w'), ('ao', '6'), ('ou', '('), ('iu', '\\'), ('ie', 'e'), ('ue', ')'), ('er', 'r'), ('an', 'v'),
            ('en', '0'), ('in', '<'), ('un', '3'), ('vn', '_'), ('ang', '8'), ('eng', '#'), ('ing', '*'),
            ('ong', '4'), ('ian', '%'),('ia', '$'), ('iang', 'x'), ('iao', '>'), ('iong', '?'), ('uai', 'y'), ('ua', '='),
            ('uan', ']'), ('uang', '7'), ('uo', 'o'), ('van', '&'),
        ]

        self.tone_trans_table = [(0, ''), (1, 'a'), (2, '1'), (3, '3'), (4, '2')]

        self.figure_dots_table = [
            ('a', '1'), ('1', '2'), ('b', '12'), ("'", '3'), ('k', '13'), ('2', '23'), ('l', '123'), ('`', '4'),
            ('c', '14'), ('i', '24'), ('f', '124'), ('/', '34'), ('m', '134'), ('s', '234'), ('p', '1234'), ('"', '5'),
            ('e', '15'), ('3', '25'), ('h', '125'), ('9', '35'), ('o', '135'), ('6', '235'), ('r', '1235'), ('^', '45'),
            ('d', '145'), ('j', '245'), ('g', '1245'), ('>', '345'), ('n', '1345'), ('t', '2345'), ('q', '12345'),
            (',', '6'), ('*', '16'), ('5', '26'), ('<', '126'), ('-', '36'), ('u', '136'), ('8', '236'), ('v', '1236'),
            ('.', '46'), ('%', '146'), ('[', '246'), ('$', '1246'), ('+', '346'), ('x', '1346'), ('!', '2346'),
            ('&', '12346'), (';', '56'), (':', '156'), ('4', '256'), ('\\', '1256'), ('0', '356'), ('z', '1356'),
            ('7', '2356'), ('(', '12356'), ('_', '456'), ('?', '1456'), ('w', '2456'), (']', '12456'), ('#', '3456'),
            ('y', '13456'), (')', '23456'), ('=', '123456'),
        ]

        self.figure_table = ['a', '1', 'b', "'", 'k', '2', 'l', '`', 'c', 'i', 'f', '/', 'm', 's', 'p', '"', 'e', '3', 'h', '9', 'o', '6', 'r', '^', 'd', 'j', 'g', '>', 'n', 't', 'q', ',', '*', '5', '<', '-', 'u', '8', 'v', '.', '%', '[', '$', '+', 'x', '!', '&', ';', ':', '4', '\\', '0', 'z', '7', '(', '_', '?', 'w', ']', '#', 'y', ')', '=']


    def handle(self):

        shengmu_table = []
        for group in self.shengmu_trans_table:
            shengmu_table.append(group[0])

        yunmu_table = []
        for group in self.yunmu_trans_table:
            yunmu_table.append(group[0])

        if self.shengmu is None and self.yunmu is None:
            self.braille = ''

        elif self.shengmu is None:
            self.shengmu_symbol = ''
            self.yunmu_symbol = self.yunmu_trans_table[yunmu_table.index(self.yunmu)][1]
            self.tone_symbol = self.tone_trans_table[self.tone][1]
            self.braille = self.yunmu_symbol + self.tone_symbol

        elif self.shengmu in shengmu_table:
            if self.yunmu is None:
                self.shengmu_symbol = self.shengmu_trans_table[shengmu_table.index(self.shengmu)][1]
                self.braille = self.shengmu_symbol

            else:
                if (self.shengmu in ['zh', 'ch', 'sh', 'z', 'c', 's']) and (self.yunmu == 'i'):
                    self.shengmu_symbol = self.shengmu_trans_table[shengmu_table.index(self.shengmu)][1]
                    self.tone_symbol = self.tone_trans_table[self.tone][1]
                    self.braille = self.shengmu_symbol + self.tone_symbol
                else:
                    self.shengmu_symbol = self.shengmu_trans_table[shengmu_table.index(self.shengmu)][1]
                    self.yunmu_symbol = self.yunmu_trans_table[yunmu_table.index(self.yunmu)][1]
                    self.braille = self.shengmu_symbol + self.yunmu_symbol

    def set_dots(self):
        self.dots = ''
        for i in self.braille:
            self.dots = self.dots + braille2dots(i) + '-'

    def transfer(self, combination = (None, None, None)):
        self.__init__()
        self.shengmu = combination[0]
        self.yunmu = combination[1]
        self.tone = combination[2]
        self.handle()
        self.set_dots()
        return (self.braille, self.dots)


class Character(object):
    def __init__(self, character):
        self.string = character
        self.pinyin = str
        self.tone = 0
        self.pinyin_notone = str


def toBraille(string=''):
    punctuation_dict = {
        '。': '"2',
        '，': '"',
        '？': '"\'',
        '！': ';1',
        '：': '-',
        '、': '`',
        '；': ';',
        '——': '36',
        '（': ';\'',
        '）': '\';',
        '【': ';2',
        '】': '2;',
        '“': '^',
        '”': '^',
        '’': '^^',
        '‘': '^^',
        '《': '"-',
        '》': '-"',
        '<': '"\'',
        '>': '\'"',
        '.': '"2',
        ',': '"',
        '?': '"\'',
        '!': ';1',
        ':': '-',
        ';': ';',
        '--': '36',
        '(': ';\'',
        ')': '\';',
        '[': ';2',
        ']': '2;',
        '"': '^',
        '': '^^',
    }

    output_string = ''
    output_dots = ''
    k = KanjiToPinyin()
    p = Pinyin2Braille()
    for character in string:
        if character in punctuation_dict.keys():
            output_string += punctuation_dict[character]
            t = punctuation_dict[character]
            for i in t:
                output_dots += braille2dots(i) + '-'

        elif character == ' ':
            output_string += character
            output_dots += 'blank-'
        else:
            output_string += p.transfer(k.transfer(character))[0]
            output_dots += p.transfer(k.transfer(character))[1]
    return output_string, output_dots[0:-1]

def toPinyin(string = ''):
    output_string = []
    k = KanjiToPinyin()
    for character in string:
        if character == ' ':
            output_string.append(character)
        else:
            output_string.append(k.transfer(character))
    return output_string

if __name__ == '__main__':
    print(toBraille('猫2sfaf'))