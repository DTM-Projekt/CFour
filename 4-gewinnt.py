# Konstanten
COLS = 7  # ANZAHL SPALTEN
ROWS = 6  # ANZAHL ZEILEN
FIELDS = COLS * ROWS  # ANZAHL DER FELDER
FIRST_FIELD = 0  # POSITION RECHTS UNTEN
LAST_FIELD = FIELDS - 1  # POSITION LINKS OBEN
WIN_LENGTH = 4  # WIEVIELE STEINE IN EINER REIHE GEWINNEN?

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


def draw_game(wert):
    for y in range(ROWS, 0, -1):
        for x in range(0, COLS, 1):
            filter = 1 << (COLS - x - 1) + ((y-1) * COLS)
            if (wert & filter):
                print('X', end='')
            else:
                print('o', end='')
            if (x < COLS-1):
                print('|', end='')
            else:
                print()


# = 0b666666655555554444444333333322222221111111
a = 0b100000000000000000000000000000000000000001
b = 0b100010001001010100110010010001010101001010

init()

for game in win_positions:
    draw_game(game)
    print()
