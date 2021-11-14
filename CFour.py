# Konstanten
WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = WIDTH * HEIGHT
S1 = WIDTH * H1
LENGTH = 4
SIGNS = ['x', 'o', ' ']
PLAYERS = ['Gelb', 'Rot']


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


def has_won(newboard):
    diag1 = newboard & (newboard >> HEIGHT)
    hori = newboard & (newboard >> H1)
    diag2 = newboard & (newboard >> H2)
    vert = newboard & (newboard >> 1)
    a = (diag1 & (diag1 >> 2*HEIGHT))
    b = (hori & (hori >> 2*H1))
    c = (diag2 & (diag2 >> 2*H2))
    d = (vert & (vert >> 2))
    e = a | b | c | d
    return (e)


def current_player():
    return(nplies & 1)


def make_move(row):
    global nplies
    x = 1 << heights[row]
    side = nplies & 1
    colors[side] ^= x
    heights[row] += 1
    nplies += 1


def draw_game(side=0, topline=False):

    array = range(1, WIDTH + 1)
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

            if (colors[0] & filter):
                string += SIGNS[0]
            elif (colors[1] & filter):
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

    print('  ', end='')
    for x in array:
        print(x, '  ', end='')
    print()


def player_move():
    cont = True
    while(cont):
        print(PLAYERS[current_player()], "ist am Zug")
        row = input("Spalte : ")
        row = int(row) - 1
        whitelist = range(0, WIDTH)
        if (row in whitelist):
            cont = False 

    return(row)

""" Zahlenliste --> Stringliste
>>> a = [1,2,3,4]
>>> a
[1, 2, 3, 4]
>>> f = lambda x: str(x)
>>> list(map(f,a))
['1', '2', '3', '4']
>>>
"""

init()

conti = True

while(conti):
    draw_game(0)
    row = player_move()
    make_move(row)
