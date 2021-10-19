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


def draw_game(v0=0, v1=0, side=0):

    top = '┌' + ((COLS-1) * '───┬') + '───┐'
    buttom = '└' + ((COLS-1) * '───┴') + '───┘'
    between = '├' + ((COLS-1) * '───┼') + '───┤'
    x_grid = range(0, COLS, 1)
    y_grid = range(ROWS, 0, -1)

    print(top)

    for y in y_grid:

        col_str = '│'

        for x in x_grid:

            # x=0, y=6 COLS=7, ROWS=6

            filter = 1 << y COLS*x

            col_str += ' '

            if (v0 & filter):
                col_str += LETTER_0
            elif (v1 & filter):
                col_str += LETTER_1
            else:
                col_str += LETTER_NONE

            col_str += ' │'

        if (side == 0):
            print(col_str)
        else:
            print(col_str[::-1])
        if (y > 1):
            print(between)

    print(buttom)


# x ..765432176543217654321765432176543217654321
# y ..666666655555554444444333333322222221111111

a = 0b111111


draw_game(a)
