# -*- coding: utf-8 -*-
#! usr/bin/python


class DotsBraille(object):
    def __init__(self):
        self.dots_braille_dict = {
            'a': '1', '1': '2', 'b': '12', "'": '3', 'k': '13', '2': '23', 'l': '123', '`': '4', 'c': '14', 'i': '24',
             'f': '124', '/': '34', 'm': '134', 's': '234', 'p': '1234', '"': '5', 'e': '15', '3': '25', 'h': '125',
             '9': '35', 'o': '135', '6': '235', 'r': '1235', '^': '45', 'd': '145', 'j': '245', 'g': '1245', '>': '345',
             'n': '1345', 't': '2345', 'q': '12345', ',': '6', '*': '16', '5': '26', '<': '126', '-': '36', 'u': '136',
             '8': '236', 'v': '1236', '.': '46', '%': '146', '[': '246', '$': '1246', '+': '346', 'x': '1346',
             '!': '2346', '&': '12346', ';': '56', ':': '156', '4': '256', '\\': '1256', '0': '356', 'z': '1356',
             '7': '2356', '(': '12356', '_': '456', '?': '1456', 'w': '2456', ']': '12456', '#': '3456', 'y': '13456',
             ')': '23456', '=': '123456'
        }
        self.dots = str
        self.braille_sign = str

    def braille2dots(self, string):
        self.braille_sign = string
        if self.braille_sign in self.dots_braille_dict.keys():
            self.dots = self.dots_braille_dict[self.braille_sign]
        return self.dots

    def dots2braille(self, string):
        self.dots = string
        braille_sign_box = []
        dots_box = []
        for braille_sign, dots in self.dots_braille_dict.items():
            braille_sign_box.append(braille_sign)
            dots_box.append(dots)

        self.braille_sign = braille_sign_box[dots_box.index(self.dots)]
        return self.braille_sign


def dots2braille(dots = str):
    d = DotsBraille()
    return d.dots2braille(dots)

def braille2dots(braille = str):
    d = DotsBraille()
    return d.braille2dots(braille)

if __name__ == '__main__':
    print(braille2dots('1'))
