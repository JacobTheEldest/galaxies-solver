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
        if linenum != 0 and linenum != len(text)-1: #ignore first and last lines
            text[linenum] = text[linenum].replace('|', ' ')
            text[linenum] = text[linenum].replace('W', ' ')
            text[linenum] = text[linenum].replace('-', ' ')
            if linenum % 2 == 1:
                text[linenum] = '|{}|'.format(text[linenum][1:-1])
        text[linenum] = list(text[linenum])
    return text

def initial_assignment(board):
    '''
    Assign cells to dots that are on the edges of each cell.
    '''
    for rownum in range(1, len(board)-1):
        for colnum in range(1, len(board[rownum])-1):
            if board[rownum][colnum][0] == 'o':
                print('{}/{}'.format(rownum, colnum))
                if rownum%2==0 and colnum%2==0:
                    board[rownum-1][colnum-1] = '{}/{}'.format(rownum, colnum)
                    board[rownum-1][colnum+1] = '{}/{}'.format(rownum, colnum)
                    board[rownum+1][colnum-1] = '{}/{}'.format(rownum, colnum)
                    board[rownum+1][colnum+1] = '{}/{}'.format(rownum, colnum)
                elif rownum%2==0:
                    board[rownum-1][colnum] = '{}/{}'.format(rownum, colnum)
                    board[rownum+1][colnum] = '{}/{}'.format(rownum, colnum)
                elif colnum%2==0:
                    board[rownum][colnum-1] = '{}/{}'.format(rownum, colnum)
                    board[rownum][colnum+1] = '{}/{}'.format(rownum, colnum)
    return board

def print_table(table):
    colname = '\t'
    rowname = ''
    for rownum in range(len(table)):
        for colnum in range(len(table[rownum])):
            if colnum%2 == 1:
                for item in range(5-len(table[rownum][colnum])):
                    table[rownum][colnum] += ' '
    print('\n')
    for i in range(len(table[0])):
        if i%2==0:
            if len(str(i)) == 1:
                colname += str(i) + '  '
            else:
                colname += str(i) + ' '
        else:
            if len(str(i)) == 1:
                colname += str(i) + '      '
            else:
                colname += str(i) + '     '
    print(colname)
    for rownum in range(len(table)):
        x = '  '.join(table[rownum])
        x = x.replace('-    ', '-----')
        #x = x.replace('+    ', '+')
        print(str(rownum) + '\t' + x)
    print('\n')
    return

def get_twin(row, col):
    [dotrow, dotcol] = board[row][col].split('/')
    dotrow = int(dotrow)
    dotcol = int(dotcol)
    print('dot: {},{}'.format(dotrow, dotcol))
    if int(dotrow) > row:
        twinrow = (dotrow-row)+dotrow
    elif int(dotrow) < row:
        twinrow = dotrow-(row-dotrow)
    else:
        twinrow = dotrow
    if int(dotcol) > col:
        twincol = (dotcol-col)+dotcol
    elif int(dotcol) < col:
        twincol = dotcol-(col-dotcol)
    else:
        twincol = dotcol
    return (twinrow, twincol)

def main():
    global board
    board = import_text()
    print_table(board)
    board = initial_assignment(board)
    print_table(board)
    print(get_twin(11, 9))
    print(board)

if __name__ == '__main__':
    main()
