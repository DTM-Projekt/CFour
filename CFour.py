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


def move(bb, pos):
    # Einen Spielstein an einer bestimmten Position platzieren.
    return bb ^ pos  # XOR!?


def insert(bb, bare, slot):
    # Einen Spielstein in einen Slot einwerfen.
    bb = move(bb, bare[slot])
    bare[slot] <<= 1
    return bb, bare


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


def legal_positions(bare):
    # Liste mit allen möglichen Spielpositionen.
    return [x for x in bare if not (x & TOP1)]


def legal_slots(bare):
    # Liste mit allen freien Slots.
    return [x for x in range(WIDTH) if not (bare[x] & TOP1)]


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


"""
# original from https://github.com/davecom/ClassicComputerScienceProblemsInPython/blob/master/Chapter8/minimax.py

def alphabeta(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8, alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    # Base case – terminal position or maximum depth reached
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # Recursive case - maximize your gains or minimize the opponent's gains
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:  # minimizing
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta


# Find the best possible move in the current position
# looking up to max_depth ahead
def find_best_move(board: Board, max_depth: int = 8) -> Move:
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    for move in board.legal_moves:
        result: float = alphabeta(board.move(move), False, board.turn, max_depth)
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move
"""

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
    playables = legal_slots(bare)
    player = count & 1
    txt = LFs + "VIER GEWINNT\n============\n" + grid()
    txt += "\n"+names[player]+" ("+SIGNS[player]+") ist am Zug."
    txt += "\nBitte E für Spiel-ENDE oder die Ziffer unter dem gewünschten Slot eingeben"
    txt += "\nMögliche Slots: " + str(playables) + ": "
    txt = input(txt)
    if txt in ['e', 'E']:
        break
    if txt in ['a', 'A']:
        # KI wird "von Hand" gestartet
        print("KI wird gestartet")
    if txt in [str(x) for x in playables]:
        slot = int(txt)
        bbs[player], bare = insert(bbs[player], bare, slot)
        if (has_won(bbs[player])):
            print(LFs + "VIER GEWINNT\n============\n" + grid())
            input(names[player] + " hat gewonnen...")
            break
        count += 1
    else:
        input("\nFehleingabe...")
