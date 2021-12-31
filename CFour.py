#!/bin/env python3

# Das Spiel "Vier Gewinnt" programmiert in Python.
# Diese Version ist funktional programmiert.

from typing import List


WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = HEIGHT * WIDTH
S1 = H1 * WIDTH
TOP1 = 283691315109952
SIGNS = ('x', 'o', ' ')
DEPTH_MAX = 4


def mv(bb, pos):
    # Einen Spielstein
    # an einer bestimmten Position platzieren.
    return bb ^ pos  # XOR!? ON/OFF?


def move(bbs, color, pos):
    # Einen Spielstein
    # einer bestimmten Farbe
    # an einer bestimmten Position platzieren.
    bbs[color] = mv(bbs[color], pos)
    return bbs


def insert(bbs, bare, color, slot):
    # Einen Spielstein
    # einer bestimmten Farbe
    # in einen Slot einwerfen.
    bbs = move(bbs, color, bare[slot])
    bare[slot] <<= 1
    return bbs, bare


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


def bb(bbs, color):
    # Bitboard einer bestimmten Farbe
    return bbs[color]


def legal_moves(bare):
    # Liste mit allen möglichen Spielpositionen.
    return [x for x in bare if not (x & TOP1)]


def legal_inserts(bare):
    # Liste mit allen freien Slots.
    return [x for x in range(WIDTH) if not (bare[x] & TOP1)]


def is_draw(count) -> bool:
    # Ist das Spielfeld voll?
    return count >= SIZE


def count_segment(bbs, seg) -> tuple([int, int]):
    # Anzahl der jeweiligen Steine beider Farben in einer Gewinnposition.
    x1 = bbs[0] & seg
    x2 = bbs[1] & seg
    x1 = [x for x in range(S1) if (x1 << x) & 1]
    x2 = [x for x in range(S1) if (x2 << x) & 1]
    return len(x1), len(x2)


def evaluate_segment(bbs, seg, player) -> float:
    # Bewertung einer möglichen Gewinnposition einer bestimmten Farbe.
    color_0, color_1 = count_segment(bbs, seg)
    if color_0 > 0 and color_1 > 0:
        return 0   # Neutral, wenn beide Farben vorhanden
    count = max(color_0, color_1)
    score: float = 0
    if count == 2:
        score = 1
    elif count == 3:
        score = 100
    elif count == 4:
        score = 1000000
    if player == 0:
        score = -score if color_0 < color_1 else score
    else:
        score = -score if color_1 < color_0 else score
    return score


def evaluate(bbs, player) -> float:
    # Bewertung der Spielposition aus Sicht einer bestimmten Farbe.
    total: float = 0
    for seg in win_positions:
        total += evaluate_segment(bbs, seg, player)
    return total


def player(count) -> int:
    # aktueller Spieler?
    return count & 1


def all_win_positions(bbs) -> list:
    # Bitboard aller gewonnen Spielpositionen
    awp = [0, 0]
    for seg in win_positions:
        awp[0] |= seg if (seg & bbs[0]) == seg else 0
        awp[1] |= seg if (seg & bbs[1]) == seg else 0
    return awp


def get_best_move(bbs, bare, count, depth):
    global best_move
    best_val = int("-10000000000")
    moves = legal_inserts(bare)
    for m in moves:
        bbs_new = bbs[:]
        bare_new = bare[:]
        count_new = count
        bbs_new, bare_new = insert(bbs_new, bare_new, count_new & 1, m)
        worth = evaluate(bbs_new, count_new & 1)
        won = True if worth < -1000000 else False
        lost = True if worth > 1000000 else False
        count_new += 1
        print(grid(bbs_new))
        if (depth < DEPTH_MAX and not won and not lost):
            worth -= get_best_move(bbs_new, bare_new, count_new, depth+1)
        if won:
            if depth == 0:
                best_move = m
                return worth
            else:
                if worth > best_val:
                    best_val = worth
                    if depth == 0:
                        best_move = m
    return best_val


def grid(bbs, topline=False):
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


# INIT
bbs = [0, 0]
bare = [(1 << x) for x in [0, 7, 14, 21, 28, 35, 42]]
names = ["GELB", "ROT"]
count = 0
wp1 = [15 << y*7+x for y in range(7) for x in range(3)]        # |
wp2 = [2113665 << y*7+x for y in range(4) for x in range(6)]   # -
wp3 = [16843009 << y*7+x for y in range(4) for x in range(3)]  # /
wp4 = [2130440 << y*7+x for y in range(4) for x in range(3)]   # \
win_positions = [*wp1, *wp2, *wp3, *wp4]

# MAIN
while(count < SIZE):
    playables = legal_inserts(bare)
    player = count & 1
    txt = "\nVIER GEWINNT\n============\n" + grid(bbs)
    txt += "\n"+names[player]+" ("+SIGNS[player]+") ist am Zug."
    txt += "\nBitte E für Spiel-ENDE oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables) + ": "
    txt = input(txt)
    if txt in ['e', 'E']:
        break
    if txt in ['a', 'A']:
        # KI wird "von Hand" gestartet
        print("KI wird gestartet")
        best_move = 0
        get_best_move(bbs,bare,count,0)
        x = best_move
    if txt in [str(x) for x in playables]:
        slot = int(txt)
        bbs, bare = insert(bbs, bare, player, slot)
        if (has_won(bbs[player])):
            print("\nVIER GEWINNT\n============\n" + grid(bbs))
            input(names[player] + " hat gewonnen...")
            print(grid(all_win_positions(bbs)))
            break
        count += 1     # switch player
    else:
        input("\nFehleingabe...")
