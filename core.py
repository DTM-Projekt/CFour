class game:

    bbs = list()     # Bitboards für zwei Spieler
    lowest = list()  # Die untersten freien Plätze pro Spalte
    counter = int()  # Anzahl der bis jetzt getätigten Spielzüge
    width = int()    # Breite des Spielfeldes
    height = int()   # Höhe des Spielfeldes
    h1 = int()       # imaginäre Zeile über dem Spielfeld
    h2 = int()       # imaginäre zweite Zeile über dem Spielfeld
    size = int()     # Anzahl der Felder auf dem Gitter
    s1 = int()       # Anzahl der Felder einschließlich der ersten imaginären Zeile

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
