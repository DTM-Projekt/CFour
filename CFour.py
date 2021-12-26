#!/bin/env python3

"""
Das Spiel "Vier Gewinnt" programmiert in Python
Diese Version ist funktional programmiert.
"""

WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = HEIGHT * WIDTH
TOP1 = 283691315109952
SIGNS = ('x', 'o', ' ')
LFs = 40 * "\n"


def move(v_row):
    # Einen Spielstein in den Slot 'v_row' einwerfen.
    bitboards[counter & 1] ^= (1 << bares[v_row])  # XOR
    bares[v_row] += 1


def is_playable(v_row):
    # Ist der Slot 'v_row' spielbar (frei)?
    return (1 << bares[v_row] & TOP1) == 0


def playables():
    # Gib eine Liste aller spielbaren Slots zurück
    return [x for x in range(WIDTH) if is_playable(x)]


def has_won():
    # Hat der aktuelle Spieler gewonnen?
    bb = bitboards[counter & 1]
    hori = bb & (bb >> H1)
    vert = bb & (bb >> 1)
    diag1 = bb & (bb >> HEIGHT)
    diag2 = bb & (bb >> H2)
    a = (hori & (hori >> 2*H1))
    b = (vert & (vert >> 2))
    c = (diag1 & (diag1 >> 2*HEIGHT))
    d = (diag2 & (diag2 >> 2*H2))
    return a | b | c | d


def grid(topline=False):
    # Gib das aktuelle Spielfeld als Textgrafik zurück
    x_grid = range(0, WIDTH, 1)
    y_grid = range(H1, 0, -1) if topline else range(HEIGHT, 0, -1)
    txt = '┌' + ((WIDTH - 1) * '───┬') + '───┐' + "\n"
    for y in y_grid:
        txt += '│'
        for x in x_grid:
            filter = 1 << (x * H1) + (y - 1)
            sign = SIGNS[2]
            sign = SIGNS[0] if bitboards[0] & filter else sign
            sign = SIGNS[1] if bitboards[1] & filter else sign
            txt += ' ' + sign + ' │'
        txt += "\n├"+((WIDTH-1)*'───┼')+'───┤'+"\n" if y > 1 else ''
    txt += "\n└"+((WIDTH-1)*'───┴')+'───┘'+"\n"
    txt += (str().join(map(lambda x: '   '+str(x), x_grid)))[1::]
    return txt


names = ["GELB", "ROT"]
counter = 0
bitboards = [0, 0]
bares = [0, 7, 14, 21, 28, 35, 42]
while(counter < SIZE):
    txt = LFs + "VIER GEWINNT\n============\n" + grid()
    txt += "\n"+names[counter & 1]+" ("+SIGNS[counter & 1]+") ist am Zug."
    txt += "\nBitte E für Spiel-ENDE oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables()) + ": "
    i_txt = input(txt)
    if i_txt in ['e', 'E']:
        exit()
    if i_txt in [str(x) for x in playables()]:
        move(int(i_txt))
        if (has_won()):
            print(LFs + "VIER GEWINNT\n============\n" + grid())
            input(names[counter & 1] + " hat gewonnen...")
            break
        counter += 1
    else:
        input("\nFehleingabe...")
