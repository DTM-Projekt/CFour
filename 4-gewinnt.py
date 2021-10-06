# Konstanten
COLS = 7  # ANZAHL SPALTEN
ROWS = 6  # ANZAHL ZEILEN
FIELDS = COLS * ROWS  # ANZAHL DER FELDER
FIRST_FIELD = 0  # POSITION RECHTS UNTEN
LAST_FIELD = FIELDS - 1  # POSITION LINKS OBEN
WIN_LENGTH = 4  # WIEVIELE STEINE IN EINER REIHE GEWINNEN?
LETTER_0 = 'X'  # SPIELSTEIN FÜR SPIELER 0
LETTER_1 = 'O'  # SPIELSTEIN FÜR SPIELER 1
LETTER_NONE = ' '  # LEERES SPIELFELD

# Spielfeldparameter prüfen
if (WIN_LENGTH > COLS):
    exit()

if (WIN_LENGTH > ROWS):
    exit()

# Globale Variablen definieren
win_positions = []


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
            if (x in range(cols_lim)):
                win_positions.append(ht)
                if (y in range(rows_lim)):
                    win_positions.append(dl)
                    win_positions.append(dr)
            if (y in range(rows_lim)):
                win_positions.append(vc)
            ht = ht << 1
            vc = vc << 1
            dl = dl << 1
            dr = dr << 1


def draw_game(v0=0, v1=0, side=0):

    # ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼

    top = '┌' + ((COLS-1) * '───┬') + '───┐'
    buttom = '└' + ((COLS-1) * '───┴') + '───┘'
    between = '├' + ((COLS-1) * '───┼') + '───┤'
    x_grid = range(0, COLS, 1)
    y_grid = range(ROWS, 0, -1)

    print(top)

    for y in y_grid:

        col_str = '│'

        for x in x_grid:
            filter = 1 << (COLS - x - 1) + ((y-1) * COLS)
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


# = 0b666666655555554444444333333322222221111111
a = 0b010000000000000000000000000000000000000001
b = 0b100010001001010100110010010001010101001010

draw_game()

""" init()

for game in win_positions:
    draw_game(game)
    print() """
