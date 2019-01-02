import numpy as np
import cairo

#
# Space_invader.py
#
# Fun mini-project that computes all possible invader configurations, sorts them by "rank", then draws them all,
# in a color-coordinated image
# Author: Adam Frewin
# Date: Jan 2, 2019
#

box_width = 1 # Sets pixel size, setting to 1 to minimize image size

def binary_arr(size):
    '''
    :param size: number of binary digits
    :return: np.array of size(size, 2**size) containing all possible binary configurations
    '''
    arr = np.zeros((2**size,size))
    current_loop = np.zeros(size)
    count = 1
    for i in range(2**size):
        arr[i] = current_loop
        for j in range(size):
            if count%2**j==0:
                current_loop[j] = not(current_loop[j])
                # switch the current value if enough iterations

        count = count + 1
    return arr

def generate_sorted_invaders():
    '''
    Creates an array of all 5x5 invader ships, sorted by rank
    rank is defined as the number of active, or filled in squares for an invader. Due to the symetry of the invader,
    this is an integer from 0 - 15. 0 is an empty box, 15 is a fully filled block
    :return: 32768 x 25 array containing all possible invader configs, sorted by rank,  flattened into rows
    '''

    all_invaders = np.zeros((2**15, 25))
    count = 0
    col_options = binary_arr(5) # all possible column configurations
    for mid_col in col_options:
        for L_col in col_options:
            for LL_col in col_options:
                invader = np.array([LL_col, L_col, mid_col, L_col, LL_col]).T
                all_invaders[count] = invader.flatten()
                count = count + 1

    # create second array for sorting, fastest method in this case
    sorted_invaders = np.zeros_like(all_invaders)

    # since we know how many of each rank to expect, we can set the index where each rank should appear the first
    # time. Then by counting how many of each rank we have entered, we can properly order the entire array by rank
    rank_counts = np.zeros(16).astype(int)
    rank_cutoffs = np.array([0, 1, 15, 105, 455, 1365, 3003, 5005, 6435, 6435, 5005, 3003, 1365, 455, 105, 15])
    # number of invaders per rank, adding 0 to start indexing at 0
    rank_cutoffs = np.cumsum(rank_cutoffs) #  sets values of first index of each rank
    for i in range(0, 2 ** 15):
        invader = all_invaders[i]  # select the current row
        rank = int(np.sum(invader.reshape((5, 5))[:, :3]))  # get the rank, int from 0-15

        #  selects the first index possible for the rank, plus as many of that rank that have already been placed
        sorted_invaders[rank_cutoffs[rank] + rank_counts[rank]] = invader
        rank_counts[rank] = rank_counts[rank] + 1

    return sorted_invaders

def draw_invader(invader, xpos, ypos):
    '''
    :param invader: 5x5 array, columns of 0's and 1's corresponding to filled or empty for the desired invader
    :param xpos: x coordinate, top left corner
    :param ypos: y coordinate, top left corner
    :return: none
    '''
    posy = ypos
    for i in range(5):
        posx = xpos
        for j in range(5):
            if invader[i, j] == 1:
                ctx.rectangle(posx, posy, box_width, box_width)  # Rectangle(x0, y0, x1, y1)
                ctx.fill()
            posx = posx + box_width
        posy = posy + box_width


def draw_all_invaders():
    '''
    Draws all possible invader configurations, all 32768 of them
    :return: none
    '''
    count = 0 # used for progress bar
    total = 2**15 # used for progress bar
    xpos = 0
    ypos = 0
    sorted_invaders = generate_sorted_invaders()
    for invader in sorted_invaders:
        invader_draw = invader.reshape((5,5)) # reshape to 5x5
        rank = int(np.sum(invader_draw[:,:3]))  # determine rank
        ctx.set_source(cairo.SolidPattern(*(np.array(color2rgb_int[rank])/255)))  # set color by rank
        draw_invader(invader_draw, xpos, ypos) # draw call
        xpos = xpos + 6 * box_width
        count = count + 1

        perc = round(count/total,4)*100 # Progress bar
        if perc%1==0:
             print('Percent complete: ' + str(perc) + '%')

        if xpos >= WIDTH: # move to next print row, stay within window limits
            xpos = 0
            ypos = ypos + 6 * box_width

color2rgb_int = {
        0: [255, 255, 255], # white
        1: [160, 82, 45], # brown
        2: [0, 0, 255], # dark blue
        3: [0, 100, 0], # dark green
        4: [0, 0, 0], # black
        5: [255, 255, 255], # white
        6: [150, 150, 150], # grey
        7:  [255, 0, 0], # red
        8: [135, 206, 235], # light blue
        9: [255, 0, 255], # pink
        10: [0, 255, 0], # light green
        11: [128, 0, 128], # purple
        12: [255, 255, 0], # yellow
        13: [0,255,255], # cyan
        14:[255,165,0], # orange
        15:[0, 0, 0]  # black
    }

# Initializing graphics context
WIDTH, HEIGHT = 256 * 6 * box_width, 128 * 6 * box_width
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# method call
draw_all_invaders()
# save image
surface.write_to_png("all_invaders_colored.png")

# can check rank colors  on a 16x16
COLOR_TEST = False
if COLOR_TEST:
    xpos = 0
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    for key in color2rgb_int:
        ctx.set_source(cairo.SolidPattern(*(np.array(color2rgb_int[key])/255)))
        ctx.rectangle(xpos, 0, 1, 16)
        ctx.fill()
        xpos = xpos + 1
    surface.write_to_png("color_examples.png")

