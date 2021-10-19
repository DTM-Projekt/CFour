# Konstanten
WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = WIDTH * HEIGHT
S1 = WIDTH * H1
LENGTH = 4
SIGN = ['X', 'O', '.']

# Spielfeldparameter prüfen
if (LENGTH > WIDTH | LENGTH > HEIGHT):
    exit()

# Globale Variablen definieren
# win_positions = []


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


def draw_game(v0=0, v1=0, side=0, topline=False):

    top = '┌' + ((WIDTH-1) * '───┬') + '───┐'
    buttom = '└' + ((WIDTH-1) * '───┴') + '───┘'
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

            if (v0 & filter):
                string += SIGN[0]
            elif (v1 & filter):
                string += SIGN[1]
            else:
                string += SIGN[2]

            string += ' │'

        if (side == 0):
            print(string)
        else:
            print(string[::-1])

        if (y > 1):
            print(between)

    print(buttom)


# X ..GGGGGGGFFFFFFFEEEEEEEDDDDDDDCCCCCCCBBBBBBBAAAAAAA
# Y ..7654321765432176543217654321765432176543217654321

a = 0b0000000000000000000000000000000000000111110111111


draw_game(a, a, 0, topline=True)
