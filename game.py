class core:

    def __init__(self, width=7, height=6):
        self.bitboards = [0, 0]     # Bitboards
        self.counter = 0            # getätigte Spielzüge
        self.width = width          # Breite des Spielfeldes
        self.height = height        # Höhe des Spielfeldes
        self.h1 = height + 1        # imaginäre Zeile über dem Spielfeld
        self.h2 = height + 2        # imaginäre zweite Zeile über dem Spielfeld
        self.size = height * width  # Anzahl der Felder auf dem Spielfeld
        self.s1 = self.h1 * width   # Anzahl der Felder + 1 Zeile
        # erster freier Platz in jeder Spalte
        self.lowest = list(range(0, self.size + 1, self.h1))
        # letzter möglicher Platze in jeder Spalte
        self.maximal = list(range(height - 1, self.size + 1, self.h1))

    def player(self, x):
        # player(0) gibt den Vorhandspieler zurück
        # player(1) den Rückhandspieler
        return (self.counter + x) & 1

    def make_move(self, row):
        if (self.lowest[row] < self.maximal[row]):
            x = 1 << self.lowest[row]
            self.bitboards[self.player(0)] ^= x  # XOR ?
            self.lowest[row] += 1
            self.counter += 1
            return True
        else:
            return False

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


class io:
    #
    # Klasse für Nutzererfahrungen
    #
    signs = [' ', 'x', 'o']
    colors = ['ROT', 'GELB']

    def __init__(self):
        pass

    def grid(self, topline=False):
        #
        # Gib das Spielfeld von self.core als Textgrafik zurück
        #
        xgr = range(0, self.width, 1)   # X-Grid
        ygr = range(self.h1, 0, -1) if topline else range(self.height, 0, -1)
        tmp = '┌' + ((self.width-1) * '───┬') + '───┐' + "\n"
        for y in ygr:
            tmp += '│'
            for x in xgr:
                filter = 1 << (x * self.h1) + (y - 1)
                tmp += ' '
                if (self.bitboards[0] & filter):
                    tmp += self.signs[1]
                elif (self.bitboards[1] & filter):
                    tmp += self.signs[2]
                else:
                    tmp += self.signs[0]
                tmp += ' │'
            tmp += "\n"
            if (y > 1):
                tmp += '├' + ((self.width-1) * '───┼') + '───┤' + "\n"
        tmp += '└' + ((self.width-1) * '───┴') + '───┘' + "\n"
        num = range(1, self.width + 1)
        tmp += (str().join(map(lambda x: '   '+str(x), num)))[1::]
        return tmp

    def instructions(self):
        pass


class game(core, io):
    #
    # Klasse für den Spielablauf
    # 

    def __init__(self, width=7, height=6):
        core.__init__(self, width, height)
        io.__init__(self)
