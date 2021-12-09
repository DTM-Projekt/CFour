class data:
    #
    # Klasse für die Abbildung eines Spieles 'Vier Gewinnt' im Speicher
    #

    bitboards = []  # Bitboards
    counter = 0     # getätigte Spielzüge
    width = 0       # Breite des Spielfeldes
    height = 0      # Höhe des Spielfeldes
    h1 = 0          # imaginäre Zeile über dem Spielfeld
    h2 = 0          # imaginäre zweite Zeile über dem Spielfeld
    size = 0        # Anzahl der Felder auf dem Spielfeld
    s1 = 0          # Anzahl der Felder + 1 Zeile
    lowest = []     # erster freier Platz in jeder Spalte
    maximal = []    # letzter möglicher Platz in jeder Spalte

    def __init__(self, width=7, height=6):
        self.bitboards = [0, 0]
        self.counter = 0
        self.width = width
        self.height = height
        self.h1 = height + 1
        self.h2 = height + 2
        self.size = height * width
        self.s1 = self.h1 * width
        self.lowest = list(range(0, self.size + 1, self.h1))
        self.maximal = list(range(height - 1, self.size + 1, self.h1))

        
class core:
    def player(self, data, x):
        # player(0) gibt den Vorhandspieler zurück
        # player(1) den Rückhandspieler
        return (self.counter + x) & 1

    def make_move(self, data, row):
        x = 1 << self.lowest[row]
        self.bitboards[self.player(0)] ^= x  # WARUM XOR?
        self.lowest[row] += 1
        self.counter += 1

    def has_won(self, data, bitboard):
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
