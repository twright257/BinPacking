
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
The plan: Set the width of the packing bin so that it can be modified and optimized as desire. Boxes are placed in first come first
serve order with the first box being placed within a level equal to the height of the first box. Boxes are placed on a level from
left to right until one either does not fit the height limit or width space runs out, at which point a new level is created with
the level height corresponding to the height of the box that did not fit the previous level.
This continues until all boxes are placed
"""

def find_solution(rectangles):
    #set bin width boundary
    bin_width = 35000  #Have been tuning this
    # t_width = 0
    # for rectangle in rectangles:
    #     t_width += rectangle[0]
    # print(t_width)


    #begin placement
    level_wide = []         #list of lists to keep track of remaing open width of level
                                #format:[remaining width, level height]
    level_high = []         #list of lists to keep track of openings on top of other rectangles but within same level
                                #format: [width, height, upperLeftX, upperLeftY]
    placement = []
    for rectangle in rectangles:
        if level_wide:                                          #levels not empty
            placement.append(search_levels(rectangle, level_wide, level_high, bin_width))
        elif rectangle[0] <= bin_width:                     #levels empty but width less than bin, initialize first level
            level_wide.insert(0, [ (bin_width - rectangle[0]), rectangle[1]])
            level_high.insert(0, [rectangle[0], 0, 0, 0 - rectangle[1]])
            placement.append((0, 0))

    return placement


def search_levels(rectangle, level_wide, level_high, bin_width):
    y_height = 0
    #search through levels for space where rectangle fits
    # if level_high:
    #     #look through spaces above already placed  rectangles
    #     for space in level_high:
    #         if rectangle[0] <= space[0] and rectangle[1] <= space[1]:
    #             coordinates = (space[2], space[3])
    #             space[0] = rectangle[0]
    #             space[1] -= rectangle[1]
    #             space[3] -= rectangle[1]
    #             if space[1] == 0:
    #                 level_high.remove(space)
    #             return coordinates
    #look through empty level spaces
    for lev in level_wide:
        if rectangle[1] <= lev[1] and rectangle[0] <= lev[0]:   #fits within level height and leftover level width
            upper_left_x = bin_width - lev[0]
            upper_left_y = y_height
            lev[0] -= rectangle[0]                          #subtract rectangle width from remaining level width
            coordinates =  (upper_left_x, upper_left_y)
            if (lev[1] - rectangle[1]) > 0:
                level_high.append([rectangle[0], lev[1] - rectangle[1], upper_left_x, upper_left_y - rectangle[1]])
            return coordinates                              #return placement coordinates
        y_height -= lev[1]                                  #increase y placement coordinate by level height
    #spot not found, create new level
    if rectangle[0] <= bin_width:
        level_wide.append([(bin_width - rectangle[0]), rectangle[1]])
        upper_left_x = 0
        upper_left_y = y_height
        coordinates = (upper_left_x, upper_left_y)
        return coordinates                                  #return placement coordinates
    else:
        print ("rectangle width exceeds bin width!")

