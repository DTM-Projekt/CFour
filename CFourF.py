#!/bin/env python3

"""
Das Spiel "Vier Gewinnt" programmiert in Python
Diese Version ist funktional.
"""

import pygame


WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = HEIGHT * WIDTH
TOP1 = 283691315109952
SIGNS = ('x', 'o', ' ')
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 50


def switch(player):
    # Seitenwechsel durchführen
    player = int(not player)


def move(v_row, bitboards, bares, counter):
    # Einen Spielstein in den Slot 'v_row' einwerfen.
    bitboards[player] ^= (1 << bares[v_row])  # XOR
    bares[v_row] += 1
    counter += 1


def is_playable(v_row):
    # Ist der Slot 'v_row' spielbar (frei)?
    return (1 << bares[v_row] & TOP1) == 0


def bit(player, h_row, v_row):
    # Ist ein bestimmter Platz belegt?
    return bool((bitboards[player] >> h_row + v_row * H1) & 1)


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


def draw_board():
    for c in range(WIDTH):
        for r in range(HEIGHT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), gradius)

    for c in range(HEIGHT):
        for r in range(WIDTH):
            if bit(0, r, c):
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), gheight-int(r*SQUARESIZE+SQUARESIZE/2)), gradius)
            elif bit(1, r, c):
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), gheight-int(r*SQUARESIZE+SQUARESIZE/2)), gradius)
    pygame.display.update()


pygame.init()

gwidth = WIDTH * SQUARESIZE
gheight = (HEIGHT+1) * SQUARESIZE
gsize = (gwidth, gheight)
gradius = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(gsize)

# names = [input("Name Spieler A: "), input("Name Spieler B: ")]
names = ['Tim', 'Ingolf']

while True:
    counter = 0
    player = 0
    bitboards = [0, 0]
    bares = [0, 7, 14, 21, 28, 35, 42]

    while(counter < SIZE):
        print("\nVIER GEWINNT\n============\n" + grid())
        draw_board()
        plr = "\n"+names[player]+" ("+SIGNS[player]+") "
        row = input(plr + "ist am Zug: ")
        row = int(row)
        if is_playable(row):
            move(row, bitboards, bares, counter)
            if (has_won()):
                print("\nVIER GEWINNT\n============\n" + grid())
                draw_board()
                input(plr + "hat gewonnen...")
                break
            switch(player)
        else:
            input("\nFehleingabe...")
