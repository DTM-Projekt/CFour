#!/bin/env python3

# Das Spiel "Vier Gewinnt" programmiert in Python.
# Diese Version ist funktional programmiert.

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
    bbs[count & 1] ^= bare[v_row]  # XOR
    bare[v_row] <<= 1
    lock[v_row] = bare[v_row] & TOP1


def has_won(bb):
    # Hat bb eine Gewinnposition?
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
            sign = SIGNS[0] if bbs[0] & filter else sign
            sign = SIGNS[1] if bbs[1] & filter else sign
            txt += ' ' + sign + ' │'
        txt += "\n├"+((WIDTH-1)*'───┼')+'───┤'+"\n" if y > 1 else ''
    txt += "\n└"+((WIDTH-1)*'───┴')+'───┘'+"\n"
    txt += (str().join(map(lambda x: '   '+str(x), x_grid)))[1::]
    return txt


bbs = [0, 0]
bare = [(1 << x) for x in [0, 7, 14, 21, 28, 35, 42]]
lock = [0 for x in range(7)]
names = ["GELB", "ROT"]
count = 0
while(count < SIZE):
    playables = [x for x in range(WIDTH) if not lock[x]]
    txt = LFs + "VIER GEWINNT\n============\n" + grid()
    txt += "\n"+names[count & 1]+" ("+SIGNS[count & 1]+") ist am Zug."
    txt += "\nBitte E für Spiel-ENDE oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables) + ": "
    txt = input(txt)
    if txt in ['e', 'E']:
        break
    if txt in [str(x) for x in playables]:
        move(int(txt))
        if (has_won(bbs[count & 1])):
            print(LFs + "VIER GEWINNT\n============\n" + grid())
            input(names[count & 1] + " hat gewonnen...")
            break
        count += 1
    else:
        input("\nFehleingabe...")
