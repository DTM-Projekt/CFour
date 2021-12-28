#!/bin/env python3

# Das Spiel "Vier Gewinnt" programmiert in Python.
# Diese Version ist funktional programmiert.

import copy

WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = HEIGHT * WIDTH
TOP1 = 283691315109952
SIGNS = ('x', 'o', ' ')
NAMES = ('GELB', 'ROT')


class Game():

    def __init__(self) -> None:
        self.bitboards: list = [0, 0]
        self.bare:      list = [(1 << x) for x in [0, 7, 14, 21, 28, 35, 42]]
        self.count:      int = 0

    def move(self, pos) -> None:
        # Einen Spielstein an einer bestimmten Position platzieren.
        self.bitboards[self.count & 1] ^= pos  # XOR!?

    def insert(self, slot) -> None:
        # Einen Spielstein in einen Slot einwerfen.
        self.move(self.bare[slot])
        self.bare[slot] <<= 1

    def has_won(self, player) -> bool:
        # Hat der aktuelle Spieler eine Gewinnposition?
        bb = self.bitboards[self.count & player]
        hori = bb & (bb >> H1)
        vert = bb & (bb >> 1)
        diag1 = bb & (bb >> HEIGHT)
        diag2 = bb & (bb >> H2)
        a = (hori & (hori >> 2*H1))
        b = (vert & (vert >> 2))
        c = (diag1 & (diag1 >> 2*HEIGHT))
        d = (diag2 & (diag2 >> 2*H2))
        return a | b | c | d

    def legal_positions(self) -> list:
        # Liste mit allen möglichen Spielpositionen.
        return [x for x in self.bare if not (x & TOP1)]

    def legal_slots(self) -> list:
        # Liste mit allen freien Slots.
        return [x for x in range(WIDTH) if not (self.bare[x] & TOP1)]

    def is_draw(self) -> bool:
        return False

    def evaluate(self, player) -> float:
        return 1000.0

    def switch(self) -> None:
        # anderer Spieler ist an der Reihe!
        self.count += 1

    def player(self) -> int:
        # aktueller Spieler?
        return self.count & 1

    def str(self, topline=False):
        # Gib das aktuelle Spielfeld als Textgrafik zurück
        x_grid = range(0, WIDTH, 1)
        y_grid = range(H1, 0, -1) if topline else range(HEIGHT, 0, -1)
        txt = '┌' + ((WIDTH - 1) * '───┬') + '───┐' + "\n"
        for y in y_grid:
            txt += '│'
            for x in x_grid:
                filter = 1 << (x * H1) + (y - 1)
                sign = SIGNS[2]
                sign = SIGNS[0] if self.bitboards[0] & filter else sign
                sign = SIGNS[1] if self.bitboards[1] & filter else sign
                txt += ' ' + sign + ' │'
            txt += "\n├"+((WIDTH-1)*'───┼')+'───┤'+"\n" if y > 1 else ''
        txt += "\n└"+((WIDTH-1)*'───┴')+'───┘'+"\n"
        txt += (str().join(map(lambda x: '   '+str(x), x_grid)))[1::]
        return txt


class AI():

    def __init__(self, game: Game):
        self.g = Game()
        self.g.bitboards = game.bitboards[:]
        self.g.bare = game.bare[:]
        self.g.count = game.count

    def alphabeta(self, game: Game, maximizing: bool, original_player, depth=3, alpha=float("-inf"), beta=float("+inf")):
        # Base case – terminal position or maximum depth reached
        if self.g.has_won(original_player) or self.g.is_draw() or depth == 0:
            return self.g.evaluate(original_player)

        # Recursive case - maximize your gains or minimize the opponent's gains
        if maximizing:
            for move in self.g.legal_positions():
                result: float = self.alphabeta(self.g.move(move), False, original_player, depth - 1, alpha, beta)
                alpha = max(result, alpha)
                if beta <= alpha:
                    break
            return alpha
        else:  # minimizing
            for move in self.g.legal_positions():
                result = self.alphabeta(self.g.move(move), True, original_player, depth - 1, alpha, beta)
                beta = min(result, beta)
                if beta <= alpha:
                    break
            return beta

    def get_best_move(self, depth: int = 3) -> int:
        best_eval: float = float("-inf")
        best_move: int = -1
        for move in self.g.legal_positions():
            result: float = self.alphabeta(self.g.move(move), False, self.g.player(), depth)
            if result > best_eval:
                best_eval = result
                best_move = move
        return best_move


g = Game()

while(g.count < SIZE):
    playables = g.legal_slots()
    player = g.player()
    txt = "\nVIER GEWINNT\n============\n" + g.str(True)
    txt += "\n"+NAMES[player]+" ("+SIGNS[player]+") ist am Zug."
    txt += "\nBitte E für Spiel-ENDE oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables) + ": "
    txt = input(txt)
    if txt in ['e', 'E']:
        break
    if txt in ['a', 'A']:
        # KI wird "von Hand" gestartet
        print("KI wird gestartet")
        ai = AI(g)
        txt = str(ai.get_best_move())
        del ai
    if txt in [str(x) for x in playables]:
        slot = int(txt)
        g.insert(slot)
        if (g.has_won(player)):
            print("\nVIER GEWINNT\n============\n" + g.str(False))
            input(NAMES[player] + " hat gewonnen...")
            break
        g.switch()
    else:
        input("\nFehleingabe...")
