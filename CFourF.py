#!/bin/env python3

"""
Das Spiel "Vier Gewinnt" programmiert in Python
Diese Version ist funktional.
"""


def game():
    WIDTH = 7
    HEIGHT = 6
    H1 = HEIGHT + 1
    H2 = HEIGHT + 2
    SIZE = HEIGHT * WIDTH
    TOP1 = 283691315109952
    SIGNS = ('x', 'o', ' ')

    counter = 0
    player = 0
    bitboards = [0, 0]
    bares = [0, 7, 14, 21, 28, 35, 42]
    playables = [0, 1, 2, 3, 4, 5, 6]

    def switch():
        # Seitenwechsel durchführen
        nonlocal player
        player = int(not player)

    def move(v_row):
        # Einen Spielstein in den Slot 'v_row' einwerfen.
        nonlocal bitboards, bares, counter, playables
        bitboards[player] ^= (1 << bares[v_row])  # XOR
        bares[v_row] += 1
        counter += 1
        if (1 << bares[v_row] & TOP1):
            playables.remove(v_row)

    def is_playable(v_row):
        # Ist der Slot 'v_row' spielbar (frei)?
        return not bool(1 << bares[v_row] & TOP1)

    def has_won():
        # Hat der aktuelle Spieler gewonnen?
        bb = bitboards[player]
        hori = bb & (bb >> H1)
        vert = bb & (bb >> 1)
        diag1 = bb & (bb >> HEIGHT)
        diag2 = bb & (bb >> H2)
        a = (hori & (hori >> 2*H1))
        b = (vert & (vert >> 2))
        c = (diag1 & (diag1 >> 2*HEIGHT))
        d = (diag2 & (diag2 >> 2*H2))
        return a | b | c | d

        a = (bb & (bb >> H1) & (bb & (bb >> H1) >> 2*H1))

    def grid(topline=False):
        # Gib das aktuelle Spielfeld als Textgrafik zurück
        xgr = range(0, WIDTH, 1)   # X-Grid
        tmp = '┌' + ((WIDTH - 1) * '───┬') + '───┐' + "\n"
        for y in range(H1, 0, -1) if topline else range(HEIGHT, 0, -1):
            tmp += '│'
            for x in xgr:
                filter = 1 << (x * H1) + (y - 1)
                sign = SIGNS[2]
                sign = SIGNS[0] if bitboards[0] & filter else sign
                sign = SIGNS[1] if bitboards[1] & filter else sign
                tmp += ' ' + sign + ' │'
            tmp += "\n├"+((WIDTH-1)*'───┼')+'───┤'+"\n" if y > 1 else ''
        tmp += "\n└"+((WIDTH-1)*'───┴')+'───┘'+"\n"
        tmp += (str().join(map(lambda x: '   '+str(x), xgr)))[1::]
        return tmp

    while(counter < SIZE):
        print("\nVIER GEWINNT\n============\n" + grid())
        plr = "\n"+names[player]+" ("+SIGNS[player]+") "
        row = input(plr + "ist am Zug: ")
        row = int(row)
        if is_playable(row):
            move(row)
            if (has_won()):
                print("\nVIER GEWINNT\n============\n" + grid())
                input(plr + "hat gewonnen...")
                return
            switch()
        else:
            input("\nFehleingabe...")


names = [input("Name Spieler A: "), input("Name Spieler B: ")]
while True:
    game()
