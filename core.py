class game:

    # globale Variablen
    bb = [0, 0]   # Bitboards für zwei Spieler
    lowest = []  # Die untersten freien Plätze pro Spalte
    counter = 0  # Anzahl der bis jetzt getätigten Spielzüge
    width = 0
    height = 0
    size = 0
    s1 = 0
    h1 = 0
    h2 = 0

    def __init__(self, width, height):
        self.bb = [0, 0]
        self.lowest = []
        self.width = width
        self.height = height
        self.h1 = height + 1
        self.h2 = height + 2
        self.size = height * width
        self.s1 = self.h1 * width
        # lowest vorfüllen
        for x in range(0, self.size + 1, self.h1):
            self.lowest.append(x)

        return

    def make_move(self, row):
        global counter
        x = 1 << self.lowest[row]
        side = self.counter & 1
        self.bb[side] ^= x
        self.lowest[row] += 1
        self.counter += 1

    def has_won(self, newboard):
        diag1 = newboard & (newboard >> self.height)
        hori = newboard & (newboard >> self.h1)
        diag2 = newboard & (newboard >> self.h2)
        vert = newboard & (newboard >> 1)
        a = (diag1 & (diag1 >> 2*self.height))
        b = (hori & (hori >> 2*self.h1))
        c = (diag2 & (diag2 >> 2*self.h2))
        d = (vert & (vert >> 2))
        e = a | b | c | d
        return (e)
