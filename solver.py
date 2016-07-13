#! /usr/bin/env python
'''
A tool to solve Galaxies puzzles as implemented by Simon Tatham's Collection.
'''

import os
import pyperclip

def import_text():
    '''
    Imports and cleans Galaxies board from clipboard.
    '''
    text = pyperclip.paste()
    text = text.split('\r\n')
    del text[-1]
    for linenum in range(len(text)):
        if linenum == 0 or linenum == len(text)-1:
            continue
        text[linenum] = text[linenum].replace('|', ' ')
        text[linenum] = text[linenum].replace('W', ' ')
        text[linenum] = text[linenum].replace('-', ' ')
        if linenum % 2 == 1:
            text[linenum] = '|{}|'.format(text[linenum][1:-1])
    return text

def main():
    board = import_text

if __name__ == '__main__':
    main()
