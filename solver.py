#! /usr/bin/env python
'''
A tool to solve Galaxies puzzles as implemented by Simon Tatham's Collection.
'''

import os
import pyautogui

#Colors of board
BACKGROUND = (213, 211, 206)
BORDER = (0, 0, 0)
GRID = (170, 169, 165)
WHITE = (255, 255, 255)

def find_board():
    '''
    Returns a tuple of the game board region. (top, left, width, height)
    '''
    title = pyautogui.locateOnScreen('title.png')
    if title == None:
        title = pyautogui.locateOnScreen('title_active.png')
    screenshot = pyautogui.screenshot()
    border = [(title[0]+30), (title[1]+title[3]+1), 0, 0]
    while screenshot.getpixel((border[0], border[1])) != BACKGROUND:
        border[1] += 1
    while screenshot.getpixel((border[0], border[1])) != BORDER:
        border[1] += 1
    while screenshot.getpixel((border[0]-1, border[1])) == BORDER:
        border[0] -= 1
    while screenshot.getpixel((border[0]+border[2], border[1])) == BORDER:
        border[2] += 1
    while screenshot.getpixel((border[0], border[1]+border[3])) == BORDER:
        border[3] += 1
    return tuple(border)

def color_width(measure_start):
    screenshot = pyautogui.screenshot()
    width = 0
    start_color = screenshot.getpixel((measure_start))
    while screenshot.getpixel((measure_start[0] + width, measure_start[1])) == start_color:
        width += 1
    return width

def color_height(measure_start):
    screenshot = pyautogui.screenshot()
    height = 0
    start_color = screenshot.getpixel((measure_start))
    while screenshot.getpixel((measure_start[0] + height, measure_start[1])) == start_color:
        height += 1
    return height

def define_board_style():
    global gameboard
    global border_thickness
    global outer_cell_size
    global gridline_thickness
    global inner_cell_size
    gameboard = find_board()
    border_thickness = color_width((gameboard[0], (gameboard[1] + (gameboard[3]/2))))
    outer_cell_size = color_width((gameboard[0]+border_thickness,
                                  gameboard[1]+border_thickness))
    gridline_thickness = color_width((gameboard[0]+border_thickness+outer_cell_size,
                                     gameboard[1]+border_thickness))
    inner_cell_size = color_width((gameboard[0]+border_thickness+
                                  outer_cell_size+gridline_thickness,
                                  gameboard[1]+border_thickness))
    print("Gameboard region: ", gameboard)
    print("Border: ", border_thickness)
    print("Gridline: ", gridline_thickness)
    print("Inner cell: ", inner_cell_size)

def grid_size():
    x_gridlines = list(pyautogui.locateAllOnScreen('x_gridline.png', region=gameboard))
    y_gridlines = list(pyautogui.locateAllOnScreen('y_gridline.png', region=gameboard))
    return (len(x_gridlines), len(y_gridlines))

def main():
    define_board_style()
    (x_cells, y_cells) = grid_size()

if __name__ == '__main__':
    main()
