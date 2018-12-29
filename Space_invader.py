import numpy as np
import turtle as tt

box_width = 6

# all possible column configurations most easily expressed in binary notation
def binary_arr(size):
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

def rand_invader():
    # Generates random 5x5 invader
    num1 = np.random.randint(1,2**5)
    num2 = np.random.randint(1, 2 ** 5)
    num3 = np.random.randint(1, 2 ** 5)
    col1 = col_options[num1]
    col2 = col_options[num2]
    col3 = col_options[num3]
    col4 = col2.copy()
    col5 = col1.copy()
    return np.array([col1, col2, col3, col4, col5]).T

def draw_invader(invader, xpos, ypos):
    '''
    :param invader: 5x5 array, columns of 0's and 1's corresponding to filled or empty
    :param xpos: x coordinate, top left corner
    :param ypos: y coordinate, top left corner
    :return:
    '''
    posx = xpos
    posy = ypos

    posy = ypos
    for i in range(5):
        posx = xpos
        for j in range(5):
            tt.penup()
            tt.setx(posx)
            tt.sety(posy)
            if invader[i, j] == 1:
                tt.pendown()
                tt.begin_fill()
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.end_fill()
            posx = posx + box_width
        posy = posy - box_width

    tt.hideturtle()


def draw_random_invader():
    tt.reset()
    tt.speed(speed=0)
    tt.tracer(0,0)
    invader = rand_invader()
    posy = 2*box_width + box_width/2
    for i in range(5):
        posx= -2*box_width - box_width/2
        for j in range(5):
            tt.penup()
            tt.setx(posx)
            tt.sety(posy)
            if invader[i,j] ==1:
                tt.pendown()
                tt.begin_fill()
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.forward(box_width)
                tt.left(90)
                tt.end_fill()
            posx = posx+box_width
        posy = posy - box_width

    tt.hideturtle()
    tt.update()
    input("Press any key to continue")

def draw_all_invader():
    tt.tracer(0, 0)
    xpos = -(tt.window_width()/2)
    ypos = (tt.window_height()/2)
    for mid_col in col_options:
        for L_col in col_options:
            for LL_col in col_options:
                invader = np.array([LL_col, L_col, mid_col, L_col, LL_col]).T
                draw_invader(invader, xpos, ypos)
                xpos = xpos + 6 * box_width
                if(xpos>(2560/2-5*box_width)):
                    xpos = -2560/2
                    ypos = ypos - 6* box_width
                tt.update()

    tt.update()


col_options = binary_arr(5) # 5x5 grid, all possible column configs
tt.setup(1600, 1600)
draw_all_invader()
ts = tt.getscreen()
ts.getcanvas().postscript(file='space_invader.eps')
tt.done()
