
import numpy as np
import cairo

box_width = 1

def binary_arr(size):
    '''
    :param size: number of binary digets
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


def draw_random_invader():
    '''
    Draws a random invader
    :return: None
    '''
    col_options = binary_arr(5)
    num1 = np.random.randint(1, 2 ** 5)
    num2 = np.random.randint(1, 2 ** 5)
    num3 = np.random.randint(1, 2 ** 5)
    col1 = col_options[num1]
    col2 = col_options[num2]
    col3 = col_options[num3]
    col4 = col2.copy()
    col5 = col1.copy()
    invader = np.array([col1, col2, col3, col4, col5]).T
    draw_invader(invader, 0, 0)

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
    WARNING: turtle is very slow, so this function takes a while
    :return: none
    '''

    xpos = 0
    ypos = 0
    count = 0
    total = 2**15
    col_options = binary_arr(5)
    for mid_col in col_options:
        for L_col in col_options:
            for LL_col in col_options:
                invader = np.array([LL_col, L_col, mid_col, L_col, LL_col]).T
                draw_invader(invader, xpos, ypos)
                xpos = xpos + 6 * box_width
                count = count + 1
                perc = round(count/total,4)*100
                if perc%1==0:
                    print('Percent complete: ' + str(perc) + '%')
                if xpos >= WIDTH:
                    xpos = 0
                    ypos = ypos + 6 * box_width


WIDTH, HEIGHT = 256 * 6 * box_width, 128 * 6 * box_width

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

draw_all_invaders()

surface.write_to_png("all_invaders.png")