class game:

    bitboards = list()     # Bitboards für zwei Spieler
    counter = int()        # Anzahl der bis jetzt getätigten Spielzüge
    width = int()          # Breite des Spielfeldes
    height = int()         # Höhe des Spielfeldes
    h1 = int()             # imaginäre Zeile über dem Spielfeld
    h2 = int()             # imaginäre zweite Zeile über dem Spielfeld
    size = int()           # Anzahl der Felder auf dem Gitter
    s1 = int()             # Anzahl der Felder einschließlich der ersten imaginären Zeile
    lowest = list()        # Die untersten freien Plätze pro Spalte als Bitwert

    def __init__(self, width, height):
        self.bitboards = [0, 0]
        self.width = width
        self.height = height
        self.h1 = height + 1
        self.h2 = height + 2
        self.size = height * width
        self.s1 = self.h1 * width
        # am Anfang sind die Spielfelder der Zeile '0' leer
        self.lowest = list(range(0, self.size + 1, self.h1))

    def player(self, x):
        # player(0) gibt den Vorhandspieler zurück
        # player(1) den Rückhandspieler
        return (self.counter + x) & 1

    def make_move(self, row):
        x = 1 << self.lowest[row]
        self.bitboards[self.player(0)] |= x  # OR
        self.lowest[row] += 1
        self.counter += 1

    def has_won(self, bitboard):
        diag1 = bitboard & (bitboard >> self.height)
        hori = bitboard & (bitboard >> self.h1)
        diag2 = bitboard & (bitboard >> self.h2)
        vert = bitboard & (bitboard >> 1)
        a = (diag1 & (diag1 >> 2*self.height))
        b = (hori & (hori >> 2*self.h1))
        c = (diag2 & (diag2 >> 2*self.h2))
        d = (vert & (vert >> 2))
        e = a | b | c | d
        return (e)
