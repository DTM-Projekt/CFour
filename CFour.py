#!/bin/env python3

# Das Spiel "Vier Gewinnt" programmiert in Python.
# Diese Version ist funktional programmiert.

from timeit import default_timer as timer
from random import choice


INF = 1000000
WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = HEIGHT * WIDTH
S1 = H1 * WIDTH
TOP1 = 283691315109952
SIGNS = ('x', 'o', ' ')


def me(count):
    # Spieler am Zug (Vorhand)
    return count & 1


def you(count):
    # Wartender Spieler (Nachhand)
    return (count & 1) ^ 1


def mv(bb, pos):
    # Einen Spielstein
    # an einer bestimmten Position eines Bitboards
    # platzieren oder, wenn vorhanden, entfernen.
    return bb ^ pos


def insert(bbs, bare, count, slot):
    # Einen Spielstein
    # einer bestimmten Farbe
    # in einen bestimmten Slot einwerfen.
    bbs = move(bbs, count, bare[slot])
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


def legal_moves(bare):
    # Liste mit allen möglichen nächsten Spielpositionen.
    return [x for x in bare if not (x & TOP1)]


def legal_inserts(bare):
    # Liste mit allen freien Slots.
    return [x for x in range(WIDTH) if not (bare[x] & TOP1)]


def count_segment(bbs, seg) -> list:
    # Anzahl der jeweiligen Steine beider Farben in einem Gewinnsegment.
    x1 = bbs[0] & seg
    x2 = bbs[1] & seg
    x1 = bin(x1).count("1")
    x2 = bin(x2).count("1")
    return [x1, x2]


def count_slot(bb, slot):
    # Anzahl der Steine eines Bitboards in einem Slot.
    extract = (15 << 7 * slot) & bb
    return bin(extract).count("1")


def evaluate_slots(bbs) -> tuple([float, float]):
    # Bewertung des Inhalts der Slots je nach Lage.
    bb = bbs[0]
    x1 = count_slot(bb, 3) * 4
    x1 += (count_slot(bb, 2) + count_slot(bb, 4)) * 3
    x1 += (count_slot(bb, 1) + count_slot(bb, 5)) * 2
    x1 += (count_slot(bb, 0) + count_slot(bb, 6)) * 1
    bb = bbs[1]
    x2 = count_slot(bb, 3) * 4
    x2 += (count_slot(bb, 2) + count_slot(bb, 4)) * 3
    x2 += (count_slot(bb, 1) + count_slot(bb, 5)) * 2
    x2 += (count_slot(bb, 0) + count_slot(bb, 6)) * 1
    return [x1/8, x2/8]


def evaluate(bbs, color) -> float:
    # Bewertung der Spielposition aus Sicht eines bestimmten Spielers.
    if has_won(bbs[0]):
        return INF
    if has_won(bbs[1]):
        return -INF
    (total_me, total_he) = evaluate_slots(bbs)
    for seg in win_positions:
        a, b = count_segment(bbs, seg)
        if a > 0 and b > 0:
            continue
        if a == b:
            continue
        c = max(a, b)
        temp = 1
        if c == 2:
            temp = 10
        elif c == 3:
            temp = 100
        total_me += temp if a > b else 0
        total_he += temp if b > a else 0
    total = total_me - total_he
    total *= -1 if (color & 1) else 1
    return total


def sign(count):
    # Extrahiert 1 für Spieler A und -1 für Spieler B
    return -1 if (count & 1) else 1


def all_win_positions(bbs) -> list:
    # Bitboard aller gewonnen Spielpositionen
    wp_0, wp_1, bb_0, bb_1 = (0, 0, bbs[0], bbs[1])
    for seg in win_positions:
        wp_0 |= seg if (seg & bb_0) == seg else 0
        wp_1 |= seg if (seg & bb_1) == seg else 0
    return [wp_0, wp_1]


def find_best_insert(bbs, bare, count, depth):
    # Finde den 'besten' Slot für den aktuellen Spieler

    # Ich habe den MiniMax-Algorithmus auf zwei unabhängige,
    # sich gegenseitig rekursiv aufrufende Funktionen aufgeteilt.
    # So wird eine if-Clause während der Laufzeit eingespart.
    # Der Nachteil ist ein (etwas) aufgeblähter Code.
    def maximizing(bbs, bare, count, depth):
        if count > SIZE or depth == 0:
            val = evaluate(bbs, orig_color)
            return val
        best_val = -INF
        for ins in legal_inserts(bare):
            bbs_mem = bbs[:]
            bare_mem = bare[:]
            bbs_mem, bare_mem = insert(bbs_mem, bare_mem, count, ins)
            if has_won(bbs_mem[orig_color]):
                best_val = INF
                continue
            val = minimizing(bbs_mem, bare_mem, count+1, depth-1)
            best_val = max(val, best_val)
        return best_val

    def minimizing(bbs, bare, count, depth):
        if count > SIZE or depth == 0:
            val = evaluate(bbs, orig_color)
            return val
        worst_val = INF
        for ins in legal_inserts(bare):
            bbs_mem = bbs[:]
            bare_mem = bare[:]
            bbs_mem, bare_mem = insert(bbs_mem, bare_mem, count, ins)
            if has_won(bbs_mem[other_color]):
                worst_val = -INF
                continue
            val = maximizing(bbs_mem, bare_mem, count+1, depth-1)
            worst_val = min(val, worst_val)
        return worst_val

    best_ins = -1
    best_val = -INF
    orig_color = (count) & 1
    other_color = int(not orig_color)
    for minus_delta in range(depth-1):
        for ins in legal_inserts(bare):
            bbs_mem = bbs[:]
            bare_mem = bare[:]
            bbs_mem, bare_mem = insert(bbs_mem, bare_mem, count, ins)
            if has_won(bbs_mem[other_color]):
                best_val = INF
                best_ins = ins
                continue
            val = minimizing(bbs_mem, bare_mem, count+1, depth-minus_delta)
            if val > best_val:
                best_val = val
                best_ins = ins
        if best_ins != -1:
            break
    if best_ins == -1:
        best_ins = choice(legal_inserts(bare))
    return best_ins


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
    txt += "\nZug: " + str(count+1)
    txt += "\n"+names[player]+" ("+SIGNS[player]+") ist am Zug."
    txt += "\nSpielauswertung: " + str(evaluate(bbs, 0))
    txt += "\nBitte E für Spiel-ENDE, A für Automatischer Zug "
    txt += "oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables) + ": "
    txt = input(txt)
    if txt in ['e', 'E']:
        break
    if txt in ['a', 'A']:
        print("KI wird gestartet")
        timer_start = timer()
        txt = str(find_best_insert(bbs, bare, count, 5))
        timer_stop = timer()
        timer_diff = timer_stop - timer_start
        print("Rechendauer: " + str(timer_diff))
    if txt in [str(x) for x in playables]:
        slot = int(txt)
        bbs, bare = insert(bbs, bare, player, slot)
        if (has_won(bbs[player])):
            print("\nVIER GEWINNT\n============\n" + grid(bbs))
            print("\nSpielauswertung: " + str(evaluate(bbs, 0)))
            input(names[player] + " hat gewonnen...")
            print(grid(all_win_positions(bbs)))
            break
        timer_diff = 0.0
        count += 1     # switch player
    else:
        input("\nFehleingabe...")
