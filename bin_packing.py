import numpy as np
# ----------------------------------------------
# CSCI 338, Spring 2016, Bin Packing Assignment
# Author: John Paxton
# Last Modified: January 25, 2016
# ----------------------------------------------
# Modified to include find_naive_solution so that
# driver does not need to be imported.  You may delete
# find_naive_solution from your submission.
# ----------------------------------------------

"""
FIND_NAIVE_SOLUTION:
    Line the the top left corners of the rectangles up along
the y = 0 axis starting with (0,0).
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""

def find_naive_solution (rectangles):
    placement = []
    upper_left_x = 0
    upper_left_y = 0

    for rectangle in rectangles:
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)   # make a tuple
        placement.insert(0, coordinate)             # insert tuple at front of list
        upper_left_x = upper_left_x + width

    placement.reverse()                             # original order
    return placement

# -----------------------------------------------



"""
The plan: Set the width of the strip to pack so that it can be modified and optimized during testing, maybe sqrt(total width)
to begin with. First box is placed on first level and a tuple is placed in a list corresponding to the height of the first box
placed on the level and the remaining width left. If next box fits height constraint of that level, it is placed next to first and
width removed from level tuple. If cannot fit, new level created with height of that box. Level list tuples checked from bottom up
to see if new box will fit. Tuple removed from list when width maximized.

Next: Maybe keep track of vertical space above other rectangles and try to put into those spaces?????????????

FIND_SOLUTION:
    Define this function in bin_packing.py, along with any auxiliary
functions that you need.  Do not change the driver.py file at all.
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""
def find_solution(rectangles):
    #set bin width boundary
    bin_width = 25000                   #Have been tuning this
    # for rectangle in rectangles:
    #     bin_width += rectangle[0]
    # bin_width = round(np.sqrt(bin_width), -1)
    # if bin_width < 1000:
    #     bin_width = 1000

    #begin placement
    levels = []
    placement = []
    for rectangle in rectangles:
        if levels:                                          #levels not empty
            placement.append(search_levels(rectangle, levels, bin_width))
        elif rectangle[0] <= bin_width:                     #levels empty but width less than bin, initialize first level
            levels.insert(0, [ (bin_width - rectangle[0]), rectangle[1]])
            placement.append((0, 0))

    return placement


def search_levels(rectangle, levels, bin_width):
    y_height = 0
    #search through levels for space where rectangle fits
    for lev in levels:
        if rectangle[1] <= lev[1] and rectangle[0] <= lev[0]:   #fits within level height and leftover level width
            upper_left_x = bin_width - lev[0]
            upper_left_y = y_height
            lev[0] -= rectangle[0]                          #subtract rectangle width from remaining level width
            coordinates =  (upper_left_x, upper_left_y)
            return coordinates                              #return placement coordinates
        y_height += lev[1]                                  #increase y placement coordinate by level height
    #spot not found, create new level
    if rectangle[0] <= bin_width:
        levels.append([(bin_width - rectangle[0]), rectangle[1]])
        upper_left_x = 0
        upper_left_y = y_height
        coordinates = (upper_left_x, upper_left_y)
        return coordinates                                  #return placement coordinates
    else:
        print ("rectangle width exceeds bin width!")




