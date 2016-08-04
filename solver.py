#! /usr/bin/env python
'''
A tool to solve Galaxies puzzles as implemented by Simon Tatham's Collection.
'''

import os
import pyperclip

class game:
    '''
    This class will describe the board and its characteristics.
    '''

    def __init__(self):
        '''
        Call modules to perform initial setup of the board.
        Populate some initial information about the board.
        '''
        # Setup empty board
        self.board = self.import_clean() # The board as a list of lists
        self.width = len(self.board[0]) # The number of columns in the board
        self.height = len(self.board) # The number of rows in the board
        self.dots = []
        self.cells = []
        self.notdots = []
        self.lines = []
        self.intersections = []

        # Generate a list of all Galaxies
        for rownum in range(1, self.height-1, 1):
            for colnum in range(1, self.width-1, 1):
                if 'o' in self.board[rownum][colnum]:
                    self.dots.append(galaxy(rownum, colnum))

        # Generate cell objects at all board cell locations
        for rownum in range(1, self.height-1, 2):
            for colnum in range(1, self.width-1, 2):
                self.board[rownum][colnum] = cell(rownum, colnum, self.board[rownum][colnum])
                self.cells.append(self.board[rownum][colnum])

        for rownum in range(self.height):
            for colnum in range(self.width):
                if rownum%2==0 and colnum%2==1:
                    self.board[rownum][colnum] = line(rownum, colnum, self.board[rownum][colnum])
                    self.lines.append(self.board[rownum][colnum])
                if rownum%2==1 and colnum%2==0:
                    self.board[rownum][colnum] = line(rownum, colnum, self.board[rownum][colnum])
                    self.lines.append(self.board[rownum][colnum])
                if rownum%2==0 and colnum%2==0:
                    self.board[rownum][colnum] = intersection(rownum, colnum, self.board[rownum][colnum])
                    self.intersections.append(self.board[rownum][colnum])
        return

    def import_clean(self):
        '''
        Pulls a Galaxies board (ascii) from the 'text' file in directory or
        clipboard and clean it up
        '''
        # Store the board as list in variable 'test' each item is a line
        # Omits trailing empty line
        if pyperclip.paste() and pyperclip.paste()[0] == '+':
            text = pyperclip.paste().split('\r\n')[:-1]
        elif os.path.isfile('text'):
            text = open('text').read().split('\n')[:-1]
        else:
            print('ERROR')

        # Reset any moves made before copying. Finishes as a fresh puzzle.
        for linenum in range(1, len(text)-1 ): #ignore first and last lines
            text[linenum] = text[linenum].replace('|', ' ').replace('W', ' ').replace('-', ' ')
            if linenum % 2 == 1: # Recreate left and right edge borders
                text[linenum] = '|{}|'.format(text[linenum][1:-1])

        # Make each row is a list of column characters.
        for linenum in range(len(text)):
            text[linenum] = list(text[linenum])
        return text

    def display(self):
        '''
        Neatly display an ascii representation of the board.
        '''
        # Generate Column number labels
        colname = []
        for numdigits in range(len(str(self.width))):
            colname.append('\t')
            for colnum in range(self.width):
                colnum = str(colnum)
                while len(str(self.width)) > len(colnum): # Pad colnum with spaces
                    colnum = ' ' + colnum
                colname[numdigits] += str(colnum)[-1-numdigits] + '  '

        # Print Column number labels
        for x in range(len(colname)-1, -1, -1):
            print(colname[x])

        # Add the row number labels and print the board using a temporary variable
        x = [row[:] for row in self.board]
        for each in self.cells:
            # Display the parent if known
            if each.parent:
                if 'o' in each.contents: # Display the dot if in a cell
                    x[each.row][each.col] = '  o  '
                else: # Pad cells with known parents
                    x[each.row][each.col] = '{}/{}'.format(each.parent[0], each.parent[1])
                    if len(x[each.row][each.col]) == 3:
                        x[each.row][each.col] = ' {} '.format(x[each.row][each.col])
                    if len(x[each.row][each.col]) == 4:
                        x[each.row][each.col] = '{} '.format(x[each.row][each.col])
            else: # If parent unknown display empty cell
                x[each.row][each.col] = '     '

        # Replace lines with their ascii representative contents
        for line in self.lines:
            if line.contents == '':
                x[line.row][line.col] = ' '
            else:
                x[line.row][line.col] = line.contents

        # Replace intersections with their ascii representative contents
        for intersection in self.intersections:
            x[intersection.row][intersection.col] = intersection.contents

        # combine each row list into a single string
        for rownum in range(self.height):
            row = str(rownum) + '\t' + ''.join(x[rownum])
            if rownum%2==0:
                # Space characters appropriately
                print(row.replace('-', '-----').replace(' ', '     ').replace('+o+', '+  o  +').replace('+o+', '+  o  +'))
            else:
                print(row)
        print('\n')
        return

    def edge_dots(self):
        '''
        Assign cells to dots that are on the edges of each cell.
        '''
        for dot in self.dots:
            # Dot is on gridline intersection
            if dot.row%2==0 and dot.col%2==0:
                self.board[dot.row-1][dot.col-1].update_parent([dot.coords])
                self.board[dot.row+1][dot.col-1].update_parent([dot.coords])
                self.board[dot.row-1][dot.col+1].update_parent([dot.coords])
                self.board[dot.row+1][dot.col+1].update_parent([dot.coords])
            # Dot is on line between top and bottom cells
            elif dot.row%2==0 and dot.col%2==1:
                self.board[dot.row-1][dot.col].update_parent([dot.coords])
                self.board[dot.row+1][dot.col].update_parent([dot.coords])
            # Dot is on line between left and right cells
            elif dot.row%2==1 and dot.col%2==0:
                self.board[dot.row][dot.col-1].update_parent([dot.coords])
                self.board[dot.row][dot.col+1].update_parent([dot.coords])

            # Ensure cell attributes are up to date
            for each in self.cells:
                each.update_all()

    def between_galaxies(self):
        '''
        If an adjacent cell has a different known parent,
        places a border between the cells.
        '''
        for each in self.cells:
            if each.north.row%2==1 and each.parent:
                if current.board[each.row-2][each.col].parent and each.parent != current.board[each.north.row][each.north.col].parent:
                    current.board[each.row-1][each.col].is_border()
            if each.south.row%2==1 and each.parent:
                if current.board[each.row+2][each.col].parent and each.parent != current.board[each.south.row][each.south.col].parent:
                    current.board[each.row+1][each.col].is_border()
            if each.west.col%2==1 and each.parent:
                if current.board[each.row][each.col-2].parent and each.parent != current.board[each.west.row][each.west.col].parent:
                    current.board[each.row][each.col-1].is_border()
            if each.east.col%2==1 and each.parent:
                if current.board[each.row][each.col+2].parent and each.parent != current.board[each.east.row][each.east.col].parent:
                    current.board[each.row][each.col+1].is_border()

    def get_twin(self, row, col, centerrow=[], centercol=[]):
        '''
        Returns coords pointing to the 'twin' of the cell described by the
        input coordinates.
        '''
        if centerrow == []:
            centerrow=current.board[row][col].parent[0]
        if centercol == []:
            centercol=current.board[row][col].parent[1]
        twinrow = centerrow - row + centerrow
        twincol = centercol - col + centercol
        return [twinrow, twincol]

    def mirror_twin(self, row, col):
        '''
        Update a cell's twin to match the cell.
        Input is a cell's coords. Its twin will be updated.
        '''
        if current.board[row][col].parent:
            [twinrow, twincol] = self.get_twin(row, col)
            current.board[twinrow][twincol].update_parent([current.board[row][col].parent])

            # If the adjacent in any direction is a line
            if current.board[row][col].north.border:
                current.board[twinrow+1][twincol].is_border()
                # print('Mirroring to {}'.format([twinrow+1, twincol]))
            if current.board[row][col].south.border:
                current.board[twinrow-1][twincol].is_border()
                # print('Mirroring to {}'.format([twinrow-1, twincol]))
            if current.board[row][col].west.border:
                current.board[twinrow][twincol+1].is_border()
                # print('Mirroring to {}'.format([twinrow, twincol+1]))
            if current.board[row][col].east.border:
                current.board[twinrow][twincol-1].is_border()
                # print('Mirroring to {}'.format([twinrow, twincol-1]))

    def update_board(self):
        '''
        Updates all cells on the board
        '''
        done = False
        while not done: # Continue until no changes are being made
            done = True
            previous = [row[:] for row in current.board]
            # Store state before performing update
            for rownum in range(current.height):
                for colnum in range(current.width):
                    previous[rownum][colnum] = current.board[rownum][colnum].contents

            # Actually update the board
            self.between_galaxies()
            for each in self.cells:
                self.mirror_twin(each.row, each.col)
                each.update_all()

            for dot in current.dots:
                dot.check_completion()

            # Check for changes against previous state
            for rownum in range(current.height):
                for colnum in range(current.width):
                    if previous[rownum][colnum] != current.board[rownum][colnum].contents: # Break if no changes are made
                        done = False

class cell:
    '''
    This class will describe all the possible characteristics of a single cell.
    '''
    def __init__(self, row, col, contents=''):
        '''
        Perform an initial scan of the board to initialize all variables
        '''
        self.potdots = [] # List of potential dots the cell could belong to
        self.parent = []
        self.coords = [row, col]
        self.row = row
        self.col = col
        self.contents = contents # If the cell contained a 'o' store it here
        self.twin = [] # If parents is known. This will be the cell's twin
        self.path = [] # List of the cells that could be next in the path
        self.border = False # A cell will never be a border...

        if 'o' in contents:
            self.parent = self.coords

    def update_adjacent(self):
        '''
        Update adjacent directions to be the coordinates of the nearest
        adjacent object in that direction
        '''
        if current.board[self.row-1][self.col].border:
            self.north = current.board[self.row-1][self.col]
        else:
            self.north = current.board[self.row-2][self.col]
        if current.board[self.row+1][self.col].border:
            self.south = current.board[self.row+1][self.col]
        else:
            self.south = current.board[self.row+2][self.col]
        if current.board[self.row][self.col-1].border:
            self.west = current.board[self.row][self.col-1]
        else:
            self.west = current.board[self.row][self.col-2]
        if current.board[self.row][self.col+1].border:
            self.east = current.board[self.row][self.col+1]
        else:
            self.east = current.board[self.row][self.col+2]

        self.nwcorner = [self.row-1, self.col-1]
        self.swcorner = [self.row+1, self.col-1]
        self.necorner = [self.row-1, self.col+1]
        self.secorner = [self.row+1, self.col+1]

        self.adjacent = [self.north.coords, self.south.coords, self.west.coords, self.east.coords]
                        # self.nwcorner, self.swcorner, self.necorner, self.secorner]
        return

    def update_potdots(self):
        '''
        Check other cells to identify all potential parents
        '''
        if self.parent: # if the parent is already known don't bother looking for one
            self.potdots = [self.parent]
        else:
            self.potdots = []
            for dot in current.dots: # Look at each galaxy
                for each in dot.group: # Look at each item of the group in each galaxy
                    # If the dot could potentially parent the cell add it to the list
                    if self.coords == each.coords and dot.coords not in self.potdots:
                        self.potdots.append(dot.coords)

        if len(self.potdots) == 1:
            self.parent = self.potdots[0]

    def update_parent(self, parentlist=[]):
        '''
        If parent is unknown check to see if there is only one potential or use
        the parent supplied by argument.
        '''

        if parentlist == False: # if no argument given
            parentlist = self.potdots # use the list of potential parents
            self.parent = 'xxx'
        if not self.parent and len(parentlist) == 1:
            self.parent = parentlist[0]

        self.twin = current.get_twin(self.row, self.col)
        self.twin = current.board[self.twin[0]][self.twin[1]]

    def update_all(self):
        '''
        Update all attributes of the cell.
        '''
        self.update_adjacent()
        self.update_potdots()
        return

    def print_attr(self):
        print('\nCoordinates: {}'.format(self.coords))
        print('Potential dots: {}'.format(self.potdots))
        print('Parent: {}'.format(self.parent))
        print('Adjacent: {}'.format(self.adjacent))
        return

class galaxy:
    '''
    A class to describe all dots and their galaxies.
    '''
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coords = [row, col]
        self.complete = False
        self.group = []

    def check_completion(self):
        '''
        Checks if the galaxy is completed. If so updates the variable.
        '''
        self.complete = True # Default to true until proven otherwise
        # Select starting points for each group
        self.group = []
        if self.row%2==1 and self.col%2==1:
            self.group.append(current.board[self.row][self.col])
        elif self.row%2==0 and self.col%2==1:
            self.group.append(current.board[self.row-1][self.col])
        elif self.row%2==1 and self.col%2==0:
            self.group.append(current.board[self.row][self.col-1])
        elif self.row%2==0 and self.col%2==0:
            self.group.append(current.board[self.row-1][self.col-1])

        # add appropriate adjacent cells to the group
        for cell in self.group:
            if cell.north.row%2==1: # Ensure the potential is a cell
                if not cell.north.parent or cell.north.parent == self.coords: # Proceed if the potential has no parent or if the parent is the same
                    twin = current.get_twin(cell.north.row, cell.north.col, self.row, self.col)
                    if 0 < twin[0] < current.height and 0 < twin[1] < current.width: # Make sure twin is inside board
                        twin = current.board[twin[0]][twin[1]]
                        if twin.parent == [] or twin.parent == self.coords: # Proceed if the twin is valid
                            if cell.north not in self.group: # Proceed if the potential is not already in the group
                                self.group.append(cell.north)
                else: # If the search encounters a cell that belongs to another galaxy mark this galaxy as incomplete
                    self.complete = False
            if cell.south.row%2==1:
                if not cell.south.parent or cell.south.parent == self.coords:
                    twin = current.get_twin(cell.south.row, cell.south.col, self.row, self.col)
                    if 0 < twin[0] < current.height and 0 < twin[1] < current.width:
                        twin = current.board[twin[0]][twin[1]]
                        if twin.parent == [] or twin.parent == self.coords:
                            if cell.south not in self.group:
                                self.group.append(cell.south)
                else:
                    self.complete = False
            if cell.west.col%2==1:
                if not cell.west.parent or cell.west.parent == self.coords:
                    twin = current.get_twin(cell.west.row, cell.west.col, self.row, self.col)
                    if 0 < twin[0] < current.height and 0 < twin[1] < current.width:
                        twin = current.board[twin[0]][twin[1]]
                        if twin.parent == [] or twin.parent == self.coords:
                            if cell.west not in self.group:
                                self.group.append(cell.west)
                else:
                    self.complete = False
            if cell.east.col%2==1:
                if not cell.east.parent or cell.east.parent == self.coords:
                    twin = current.get_twin(cell.east.row, cell.east.col, self.row, self.col)
                    if 0 < twin[0] < current.height and 0 < twin[1] < current.width:
                        twin = current.board[twin[0]][twin[1]]
                        if twin.parent == [] or twin.parent == self.coords:
                            if cell.east not in self.group:
                                self.group.append(cell.east)
                else:
                    self.complete = False

class line:
    '''
    This class will describe all the possible characteristics of a line.
    '''
    def __init__(self, row, col, contents=''):
        '''
        Perform an initial scan of the board to initialize all variables
        '''
        self.potdots = [] # List of potential dots the cell could belong to
        self.parent = []
        self.coords = [row, col]
        self.row = row
        self.col = col
        self.contents = contents # If the cell contained a '-' or '|' store it here
        self.border = False
        if '-' in contents or '|' in contents:
            self.border = True

    def is_border(self):
        '''
        Sets self.border to True to when called.
        '''
        self.border = True
        if self.row%2==0:
            self.contents = '-'
        if self.col%2==0:
            self.contents = '|'

class intersection:
    '''
    This class will describe all the possible characteristics of a line.
    '''
    def __init__(self, row, col, contents=''):
        '''
        Perform an initial scan of the board to initialize all variables
        '''
        self.potdots = [] # List of potential dots the cell could belong to
        self.parent = []
        self.coords = [row, col]
        self.row = row
        self.col = col
        self.contents = contents # If the cell contained a '+' or 'o' store it here
        self.dot = False
        if 'o' in self.contents:
            self.dot = True

def main():
    global current
    current = game()
    print('\nEmpty board:')
    current.display() #Show empty board

    # Perform obvious assignments
    current.edge_dots()
    current.update_board()
    print('After obvious assignments:')
    current.display()


if __name__ == '__main__':
    main()
