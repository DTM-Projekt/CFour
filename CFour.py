 # Konstanten
WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = WIDTH * HEIGHT
S1 = WIDTH * H1
LENGTH = 4
SIGNS = ['X', 'O', '.']

# globale Variablen
colors = [0, 0]  # Bitboards für zwei Spieler
heights = []  # Die untersten freien Plätze pro Spalte
nplies = 0  # Anzahl der Spielzüge


def init():

    global colors, nplies

# Spielfeldparameter prüfen
if (LENGTH > WIDTH | LENGTH > HEIGHT):
    exit()

    # heights vorfüllen
    for x in range(0, SIZE + 1, H1):
        heights.append(x)

    colors = [0, 0]
    nplies = 0

    return


""" 
    def init():
    ht = 1
    vc = 1
    dl = 1
    dr = 1
    for i in range(WIN_LENGTH - 1):
        ht = (ht << 1) + 1
        vc = (vc << COLS) + 1
        dl = (dl << (COLS + 1)) + 1
        dr = (dr << (COLS - 1)) + 1
    dr = dr << (WIN_LENGTH-1)
    cols_lim = COLS-WIN_LENGTH+1
    rows_lim = ROWS-WIN_LENGTH+1
    for y in range(ROWS):
        for x in range(COLS):
            if (y in range(rows_lim)):
                win_positions.append(vc)
            if (x in range(cols_lim)):
                win_positions.append(ht)
                if (y in range(rows_lim)):
                    win_positions.append(dl)
                    win_positions.append(dr)
            ht = ht << 1
            vc = vc << 1
            dl = dl << 1
            dr = dr << 1
"""
def make_move(side, row):
    men = color[0] ^ color[1]
    row_bottom = row * H1

    while (True):
        filter = 1 << row_bottom
        x = men & filter
        
    return
    
def draw_game(side=0, topline=False):

    top = '┌' + ((WIDTH-1) * '───┬') + '───┐'
    bottom = '└' + ((WIDTH-1) * '───┴') + '───┘'
    between = '├' + ((WIDTH-1) * '───┼') + '───┤'
    x_grid = range(0, WIDTH, 1)
    y_grid = range(HEIGHT, 0, -1)

    if (topline):
        y_grid = range(H1, 0, -1)

    print(top)

    for y in y_grid:

        string = '│'

        for x in x_grid:

            filter = 1 << (x * H1) + (y - 1)
            string += ' '

            if (color[0] & filter):
                string += SIGNS[0]
            elif (color[1] & filter):
                string += SIGNS[1]
            else:
                string += SIGNS[2]

            string += ' │'

        if (side == 0):
            print(string)
        else:
            print(string[::-1])

        if (y > 1):
            print(between)

    print(bottom)


# X ..GGGGGGGFFFFFFFEEEEEEEDDDDDDDCCCCCCCBBBBBBBAAAAAAA
# Y ..7654321765432176543217654321765432176543217654321

#color[0] = 0b0000000000000000000000000000000000000111110111111
#color[1] = 0b0111010111011010101001011010010101101110110101001

#check = color[0] & color[1]

draw_game(0, topline=True)
make_move(0, 1)
draw_game(0, topline=True)
#draw_game(a, a, 0)