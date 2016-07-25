#! /usr/bin/env python
'''
A tool to solve Galaxies puzzles as implemented by Simon Tatham's Collection.
'''

import os
import pyperclip

def startup(board, dotlist):
    print('\n\nEmpty Puzzle')
    print_table(board)
    board = edge_dots(board)

    for rownum in range(3, len(board)-1, 2):
        for colnum in range(3, len(board[rownum])-1, 2):
            board = between_galaxies(rownum, colnum)

    while True:
        previous = [row[:] for row in board]
        for rownum in range(1, len(board)-1, 2):
            for colnum in range(1, len(board[rownum])-1, 2):
                board = mirror_twin(rownum, colnum)
        if previous == board:
            break

    print('\n\nCompleted Startup')
    print_table(board)
    dotlist = curate_dotlist(dotlist)
    print('Dotlist: {}\n'.format(dotlist))

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

def edge_dots(board):
    '''
    Assign cells to dots that are on the edges of each cell.
    '''
    for rownum in range(1, len(board)-1):
        for colnum in range(1, len(board[rownum])-1):
            if board[rownum][colnum][0] == 'o':
                dotlist.append('{}/{}'.format(rownum, colnum))
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
                table[rownum][colnum] = pad(table[rownum][colnum])
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
        print(str(rownum) + '\t' + x)
    print('\n')
    return

def get_twin(row, col, dot=''):
    '''
    Returns a tuple of coordinates pointing to the 'twin' of the cell described
    by the input coordinates.
    '''
    if '/' in dot:
        [dotrow, dotcol] = dot.split('/')
    elif '/' in board[row][col]:
        [dotrow, dotcol] = board[row][col].split('/')
    else:
        [dotrow, dotcol] = [row, col]
    dotrow = int(dotrow)
    dotcol = int(dotcol)
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
    return ('{}/{}'.format(twinrow, twincol))

def mirror_twin(rownum, colnum):
    '''
    Mirror a cell to its twin.
    '''
    rownum = int(rownum)
    colnum = int(colnum)
    if '/' in board[rownum][colnum] or 'o' in board[rownum][colnum]:
        [twinrow, twincol] = get_twin(rownum, colnum).split('/')
        twinrow = int(twinrow)
        twincol = int(twincol)
        board[twinrow][twincol] = board[rownum][colnum]
        if '-' in board[rownum-1][colnum]:
            board[twinrow+1][twincol] = '-----'
            # print('Mirroring {}/{} to {}/{}'.format(rownum, colnum, twinrow, twincol))
            # print('Putting a border at {}/{}'.format(twinrow+1, twincol))
        if '-' in board[rownum+1][colnum]:
            board[twinrow-1][twincol] = '-----'
            # print('Mirroring {}/{} to {}/{}'.format(rownum, colnum, twinrow, twincol))
            # print('Putting a border at {}/{}'.format(twinrow-1, twincol))
        if '|' in board[rownum][colnum-1]:
            board[twinrow][twincol+1] = '|'
            # print('Mirroring {}/{} to {}/{}'.format(rownum, colnum, twinrow, twincol))
            # print('Putting a border at {}/{}'.format(twinrow, twincol+1))
        if '|' in board[rownum][colnum+1]:
            board[twinrow][twincol-1] = '|'
            # print('Mirroring {}/{} to {}/{}'.format(rownum, colnum, twinrow, twincol))
            # print('Putting a border at {}/{}'.format(twinrow, twincol-1))
    return board

def between_galaxies(rownum, colnum):
    '''
    If an adjacent cell has a different
    known parent, places a border between the cells.
    '''
    rownum = int(rownum)
    colnum = int(colnum)
    #For nondot cells adjacent to nondot cells
    if '/' in board[rownum][colnum]:
        if rownum-2 > 0 and '/' in board[rownum-2][colnum] and board[rownum-2][colnum] != board[rownum][colnum]:
            board[rownum-1][colnum] = '-----'
            # print('Putting a border between {}/{} and {}/{}'.format(rownum-2, colnum, rownum, colnum))
        if rownum+2 < len(board) and '/' in board[rownum+2][colnum] and board[rownum+2][colnum] != board[rownum][colnum]:
            board[rownum+1][colnum] = '-----'
            # print('top reads: {}     bottom reads: {}'.format(board[rownum+2][colnum], board[rownum][colnum]))
            # print('Putting a border between {}/{} and {}/{}'.format(rownum+2, colnum, rownum, colnum))
        if colnum-2 > 0 and '/' in board[rownum][colnum-2] and board[rownum][colnum-2] != board[rownum][colnum]:
            board[rownum][colnum-1] = '|'
            # print('Putting a border between {}/{} and {}/{}'.format(rownum, colnum-2, rownum, colnum))
        if colnum+2 < len(board[rownum]) and '/' in board[rownum][colnum+2] and board[rownum][colnum+2] != board[rownum][colnum]:
            board[rownum][colnum+1] = '|'
            # print('Putting a border between {}/{} and {}/{}'.format(rownum, colnum+2, rownum, colnum))
    #for dot cells...x
    if 'o' in board[rownum][colnum]:
        #adject to nondot cells
        if rownum-2 > 0 and '/' in board[rownum-2][colnum] and '{}/{}'.format(rownum, colnum) not in board[rownum-2][colnum]:
            board[rownum-1][colnum] = '-----'
        if rownum+2 < len(board) and '/' in board[rownum+2][colnum] and '{}/{}'.format(rownum, colnum) not in board[rownum+2][colnum]:
            board[rownum+1][colnum] = '-----'
        if colnum-2 > 0 and '/' in board[rownum][colnum-2] and '{}/{}'.format(rownum, colnum) not in board[rownum][colnum-2]:
            board[rownum][colnum-1] = '|'
        if colnum+2 < len(board[rownum]) and '/' in board[rownum][colnum+2] and '{}/{}'.format(rownum, colnum) not in board[rownum][colnum+2]:
            board[rownum][colnum+1] = '|'
        #...adjacent to dot cells
        if rownum-2 > 0 and 'o' in board[rownum-2][colnum]:
            board[rownum-1][colnum] = '-----'
        if rownum+2 < len(board) and 'o' in board[rownum+2][colnum]:
            board[rownum+1][colnum] = '-----'
        if colnum-2 > 0 and 'o' in board[rownum][colnum-2]:
            board[rownum][colnum-1] = '|'
        if colnum+2 < len(board[rownum]) and 'o' in board[rownum][colnum+2]:
            board[rownum][colnum+1] = '|'
    return board

def curate_dotlist(prevlist):
    '''
    Remove completed dots from dotlist.
    1. Iterate through dotlist.
    2. Iterate through each cell that belongs to that dot.
    3. Check that each side of that cell has either a border or another cell
       with the same parent.
    4. If any cell does not meet those conditions, move to the next dot.
    '''
    dotlist = []
    for dot in prevlist:
        for rownum in range(1, len(board)-1, 2):
            for colnum in range(1, len(board[rownum])-1, 2):
                if dot not in board[rownum][colnum] and dot != '{}/{}'.format(rownum, colnum):
                    continue
                if '-' not in board[rownum-1][colnum]:
                    if dot not in board[rownum-2][colnum]:
                        if dot not in dotlist:
                            dotlist.append(dot)
                        continue
                if '-' not in board[rownum+1][colnum]:
                    if dot not in board[rownum+2][colnum]:
                        if dot not in dotlist:
                            dotlist.append(dot)
                        continue
                if '|' not in board[rownum][colnum-1]:
                    if dot not in board[rownum][colnum-2]:
                        if dot not in dotlist:
                            dotlist.append(dot)
                        continue
                if '|' not in board[rownum][colnum+1]:
                    if dot not in board[rownum][colnum+2]:
                        if dot not in dotlist:
                            dotlist.append(dot)
                        continue
    return dotlist

def adjacent_cells(rownum, colnum):
    '''
    input is a cell's coordinates.
    output is a list of all valid adjacent cells.
    '''
    cells = ['{}/{}'.format(rownum, colnum)]
    if rownum-2 > 0:
        cells.append('{}/{}'.format(rownum-2, colnum))
    if rownum+2 < len(board):
        cells.append('{}/{}'.format(rownum+2, colnum))
    if colnum-2 > 0:
        cells.append('{}/{}'.format(rownum, colnum-2))
    if colnum+2 < len(board[0]):
        cells.append('{}/{}'.format(rownum, colnum+2))
    return cells

def adjacent_lines(rownum, colnum):
    '''
    input is a cell's coordinates.
    output is a list of all adjacent lines.
    '''
    lines = []
    if rownum-1 > 0:
        lines.append('{}/{}'.format(rownum-1, colnum))
    if rownum+1 < len(board)-1:
        lines.append('{}/{}'.format(rownum+1, colnum))
    if colnum-1 > 0:
        lines.append('{}/{}'.format(rownum, colnum-1))
    if colnum+1 < len(board[0])-1:
        lines.append('{}/{}'.format(rownum, colnum+1))
    return lines

def update_cells(rownum, colnum):
    '''
    Updates routine aspects of each cell, its twin, and their adjacent cells.
    Input: cell coordinates
    Output: Updated board
    '''
    cells = []
    [cells.append(x) for x in adjacent_cells(rownum, colnum)]
    twin = get_twin(rownum, colnum)
    [twinrow, twincol] = twin.split('/')
    twinrow = int(twinrow)
    twincol = int(twincol)
    [cells.append(x) for x in adjacent_cells(twinrow, twincol)]
    for cell in cells:
        [cellrow, cellcol] = cell.split('/')
        board = between_galaxies(cellrow, cellcol)
        # print_table(board)
        board = mirror_twin(cellrow, cellcol)
    return board

def pad(item, length=5):
    '''
    pads an input string up to 'length' chars.
    '''
    for char in range(length-len(item)):
        item += ' '
    return item

def check_parents(board):
    '''
    Check every cell without a known parent. Check dotlist for the
    potential parents. If there is only one option, label the cell.
    '''
    for rownum in range(1, len(board)-1, 2):
        for colnum in range(1, len(board[rownum])-1, 2):
            if board[rownum][colnum] == '     ':
                parents = []
                for dot in dotlist:
                    twin = get_twin(rownum, colnum, dot)
                    [twinrow, twincol] = twin.split('/')
                    twinrow = int(twinrow)
                    twincol = int(twincol)
                    [dotrow, dotcol] = dot.split('/')
                    dotrow = int(dotrow)
                    dotcol = int(dotcol)
                    invalid = False
                    #Check if twin across dot would be outside board
                    if twinrow >= len(board) or twinrow < 0:
                        continue
                    elif twincol >= len(board[rownum]) or twincol < 0:
                        continue
                    #Check if twin across dot contains another galaxy's dot
                    if 'o' in board[twinrow][twincol]:
                        continue
                    #Check if twin across dot already belongs to a different galaxy
                    if '/' in board[twinrow][twincol] and dot not in board[twinrow][twincol]:
                        continue
                    #Check if cell across border is already assigned to potential parent
                    lines = []
                    [lines.append(x) for x in adjacent_lines(rownum, colnum)]
                    for line in lines:
                        [linerow, linecol] = line.split('/')
                        linerow = int(linerow)
                        linecol = int(linecol)
                        if '-' in board[linerow][linecol] or '|' in board[linerow][linecol]:
                            adjcell = get_twin(rownum, colnum, line)
                            [adjcellrow, adjcellcol] = adjcell.split('/')
                            adjcellrow = int(adjcellrow)
                            adjcellcol = int(adjcellcol)
                            if dot in board[adjcellrow][adjcellcol]:
                                invalid = True

                    if invalid == True:
                        continue

                    #If no condition disqualifies the dot from being a parent,
                    #check to make sure the cell is in the dot's group and if so
                    # add it to the list of potentials
                    if '{}/{}'.format(rownum, colnum) in get_group(dotrow, dotcol):
                        parents.append(dot)

                if len(parents) == 1:
                    board[rownum][colnum] = pad(parents[0])
                    update_cells(rownum, colnum)
                    # print('{}/{} belongs to {}'.format(rownum, colnum, parents[0]))
                # print('{}/{}: {}'.format(rownum , colnum, parents))
    return board

def check_path(startrownum, startcolnum, dot=''):
    '''
    Returns a list of all cells and gridlines a given cell has a path to.
    '''
    return pathlist

def get_group(rownum, colnum):
    '''
    Input is the coordinates of a cell with a known parent.
    Output is a list of all cells that touch the startpoint and are empty or
    confirmed as belonging.
    '''
    if 'o' in board[rownum][colnum]:
        parent = '{}/{}'.format(rownum, colnum)
    elif '/'  in board[rownum][colnum]:
        parent = board[rownum][colnum]

    [parentrow, parentcol] = parent.split('/')
    parentrow = int(parentrow)
    parentcol = int(parentcol)
    if parentrow%2==0 and parentcol%2==1:
        group = ['{}/{}'.format(parentrow-1, parentcol), '{}/{}'.format(parentrow+1, parentcol)]
    elif parentrow%2==1 and parentcol%2==0:
        group = ['{}/{}'.format(parentrow, parentcol-1), '{}/{}'.format(parentrow, parentcol+1)]
    elif parentrow%2==0 and parentcol%2==0:
        group = ['{}/{}'.format(parentrow-1, parentcol-1), '{}/{}'.format(parentrow+1, parentcol+1)]
    else:
        group = [parent]

    for cell in group:
        [cellrow, cellcol] = cell.split('/')
        cellrow = int(cellrow)
        cellcol = int(cellcol)

        #Get state of all directions
        if cellrow-2 >= 0:
            if '     ' in board[cellrow-2][cellcol]:
                if '{}/{}'.format(cellrow-2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow-2, cellcol))
            elif '/' in board[cellrow-2][cellcol] and board[cellrow-2][cellcol] == parent:
                if '{}/{}'.format(cellrow-2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow-2, cellcol))
            elif 'o' in board[cellrow-2][cellcol] and parent == '{}/{}'.format(cellrow-2, cellcol):
                if '{}/{}'.format(cellrow-2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow-2, cellcol))

        if cellrow+2 < len(board):
            if '     ' in board[cellrow+2][cellcol]:
                if '{}/{}'.format(cellrow+2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow+2, cellcol))
            elif '/' in board[cellrow+2][cellcol] and board[cellrow+2][cellcol] == parent:
                if '{}/{}'.format(cellrow+2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow+2, cellcol))
            elif 'o' in board[cellrow+2][cellcol] and parent == '{}/{}'.format(cellrow+2, cellcol):
                if '{}/{}'.format(cellrow+2, cellcol) not in group:
                    group.append('{}/{}'.format(cellrow+2, cellcol))

        if cellcol-2 >= 0:
            if '     ' in board[cellrow][cellcol-2]:
                if '{}/{}'.format(cellrow, cellcol-2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol-2))
            elif '/' in board[cellrow][cellcol-2] and board[cellrow][cellcol-2] == parent:
                if '{}/{}'.format(cellrow, cellcol-2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol-2))
            elif 'o' in board[cellrow][cellcol-2] and parent == '{}/{}'.format(cellrow, cellcol-2):
                if '{}/{}'.format(cellrow, cellcol-2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol-2))

        if cellcol+2 < len(board[0]):
            if '     ' in board[cellrow][cellcol+2]:
                if '{}/{}'.format(cellrow, cellcol+2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol+2))
            elif '/' in board[cellrow][cellcol+2] and board[cellrow][cellcol+2] == parent:
                if '{}/{}'.format(cellrow, cellcol+2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol+2))
            elif 'o' in board[cellrow][cellcol+2] and parent == '{}/{}'.format(cellrow, cellcol+2):
                if '{}/{}'.format(cellrow, cellcol+2) not in group:
                    group.append('{}/{}'.format(cellrow, cellcol+2))

    # print('Group - {}/{}: {}'.format(cellrow, cellcol, group))
    # print('Parent Group - {}/{}: {}'.format(parentrow, parentcol, group))
    return group

def assign_cells(board):
    '''
    Assigns cells using methods other than eliminating all but one dot.
    '''
    for rownum in range(1, len(board)-1, 2):
        for colnum in range(1, len(board[rownum])-1, 2):
            #Projects a cell out by one if it is bordered on 3 sides
            if '/' in board[rownum][colnum]:
                lines = adjacent_lines(rownum, colnum)
                # print('{}/{} has lines: {}'.format(rownum, colnum, lines))
                noline = []
                for line in lines:
                    [linerow, linecol] = line.split('/')
                    linerow = int(linerow)
                    linecol = int(linecol)
                    if '-' not in board[linerow][linecol] and '|' not in board[linerow][linecol]:
                        noline.append(line)
                if len(noline) == 1:
                    line = noline[0]
                    twin = get_twin(rownum, colnum, line)
                    [twinrow, twincol] = twin.split('/')
                    twinrow = int(twinrow)
                    twincol = int(twincol)
                    board[twinrow][twincol] = board[rownum][colnum]
                    update_cells(twinrow, twincol)
                    # print('{}/{} belongs to {}'.format(twinrow, twincol, board[rownum][colnum]))
            #Group empty cells and check their extents. If all extents end in
            #the same galaxy or end in borders, the whole group belongs to that
            #galaxy.
            if '     ' in board[rownum][colnum]:
                potdot = '' #Potential parent
                group = ['{}/{}'.format(rownum, colnum)] #list of all empty cells in the group
                invalid = False
                for cell in group:
                    [cellrow, cellcol] = cell.split('/')
                    cellrow = int(cellrow)
                    cellcol = int(cellcol)
                    north = ''
                    south = ''
                    east = ''
                    west = ''

                    #Get state of all directions
                    if '-' in board[cellrow-1][cellcol]:
                        north = 'border'
                    elif '     ' in board[cellrow-2][cellcol]:
                        north = 'empty'
                        if '{}/{}'.format(cellrow-2, cellcol) not in group:
                            group.append('{}/{}'.format(cellrow-2, cellcol))
                    elif '/' in board[cellrow-2][cellcol]:
                        north = board[cellrow-2][cellcol]
                    elif 'o' in board[cellrow-2][cellcol]:
                        north = '{}/{}'.format(cellrow-2, cellcol)
                    if '-' in board[cellrow+1][cellcol]:
                        south = 'border'
                    elif '     ' in board[cellrow+2][cellcol]:
                        south = 'empty'
                        if '{}/{}'.format(cellrow+2, cellcol) not in group:
                            group.append('{}/{}'.format(cellrow+2, cellcol))
                    elif '/' in board[cellrow+2][cellcol]:
                        south = board[cellrow+2][cellcol]
                    elif 'o' in board[cellrow+2][cellcol]:
                        south = '{}/{}'.format(cellrow+2, cellcol)
                    if '|' in board[cellrow][cellcol-1]:
                        west = 'border'
                    elif '     ' in board[cellrow][cellcol-2]:
                        west = 'empty'
                        if '{}/{}'.format(cellrow, cellcol-2) not in group:
                            group.append('{}/{}'.format(cellrow, cellcol-2))
                    elif '/' in board[cellrow][cellcol-2]:
                        west = board[cellrow][cellcol-2]
                    elif 'o' in board[cellrow][cellcol-2]:
                        west = '{}/{}'.format(cellrow, cellcol-2)
                    if '|' in board[cellrow][cellcol+1]:
                        east = 'border'
                    elif '     ' in board[cellrow][cellcol+2]:
                        east = 'empty'
                        if '{}/{}'.format(cellrow, cellcol+2) not in group:
                            group.append('{}/{}'.format(cellrow, cellcol+2))
                    elif '/' in board[cellrow][cellcol+2]:
                        east = board[cellrow][cellcol+2]
                    elif 'o' in board[cellrow][cellcol+2]:
                        east = '{}/{}'.format(cellrow, cellcol+2)

                    #Determine eligibility based on neighbors
                    for direction in [north, south, east, west]:
                        if '/' in direction and '/' not in potdot:
                            potdot = direction
                        elif '/' in direction and direction != potdot:
                            invalid = True

                #if all empty cells in group have only one potential parent fill 'em
                if invalid == True:
                    continue
                else:
                    for cell in group:
                        [cellrow, cellcol] = cell.split('/')
                        cellrow = int(cellrow)
                        cellcol = int(cellcol)
                        board[cellrow][cellcol] = potdot
                        update_cells(cellrow, cellcol)
    return board

def main():
    global board
    global dotlist
    board = import_text()
    dotlist = []

    startup(board, dotlist)

    # while dotlist:
    while True:
        previous = [row[:] for row in board]
        board = check_parents(board)
        print_table(board)
        dotlist = curate_dotlist(dotlist)
        print('Dotlist: {}\n'.format(dotlist))

        board = assign_cells(board)
        print_table(board)
        dotlist = curate_dotlist(dotlist)
        print('Dotlist: {}\n'.format(dotlist))

        if previous == board:
            break

    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('SOLVED!')
    print_table(board)

if __name__ == '__main__':
    main()
