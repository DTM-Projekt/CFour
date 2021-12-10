from sys import platform
from subprocess import call


class data:
    #
    # Klasse für die Abbildung des Spieles im Speicher
    #

    bitboards = None  # Bitboards
    counter = None    # Anzahl Spielzüge
    player = None     # Aktueller Spieler
    width = None      # Breite des Spielfeldes
    height = None     # Höhe des Spielfeldes
    h1 = None         # plus (imaginäre) Zeile über dem Spielfeld
    h2 = None         # rechter Nachbar
    size = None       # Anzahl der Spielzüge (Felder auf dem Spielfeld)
    s1 = None         # Anzahl der Felder + 1 Zeile
    bare = None       # erster freier Platz in jeder Spalte
    bottom = None     # Bitboard der unteren Zeile
    top = None        # Bitboard der (imaginären) Zeile über dem Spielfeld
    rtop = None       # Bitboard der letzten realen Zeile des Spielfeldes
    playable = None   # alle spielbaren Spalten in einer Liste

    def __init__(self, width=7, height=6):
        self.bitboards = [0, 0]
        self.counter = 0
        self.player = 0
        self.width = width
        self.height = height
        self.h1 = height + 1
        self.h2 = height + 2
        self.size = height * width
        self.s1 = self.h1 * width
        self.bare = list(range(0, self.s1, self.h1))
        self.bottom = 0
        for x in self.bare:
            self.bottom |= 1 << x
        self.top = self.bottom << self.height
        self.rtop = self.top >> 1
        self.playable = list(range(width))


class core:
    #
    # Klasse für die Abbildung von Spielmechanik und Grundregeln
    #

    data = None  # Zeiger auf Datenobjekt

    def __init__(self, data=None):
        self.data = data

    # zeitkritische Methoden

    def switch(self):
        # Seitenwechsel durchführen
        self.data.player = int(not self.data.player)
        return 1

    def isplayable(self, v_row):
        # return self.islegal(color[nplies & 1] | ((bitboard)1 << height[col]))
        pass

    def make_move(self, v_row):
        d = self.data
        x = 1 << d.lowest[v_row]
        d.bitboards[self.player(0)] ^= x  # XOR ?
        d.lowest[v_row] += 1
        d.counter += 1

    # zeitunkritische Methoden


class io:
    #
    # Klasse für Eingaben und Ausgaben
    #
    data = None     # Zeiger auf Datenobjekt
    signs = None    # Die Zeichen für LEER, SPIELER A und SPIELER B
    colors = None   # Die Farben der Spielsteine für SPIELER A und SPIELER B
    topline = None  # imaginäre obere Zeile bei der Ausgabe beachten?

    def __init__(self, data):
        self.data = data
        self.signs = [' ', 'x', 'o']
        self.colors = ['ROT', 'GELB']
        self.topline = False

    def grid(self, topline=False, bitboard=None):
        #
        # Gib das Spielfeld von 'self.data' als Textgrafik zurück
        #
        if (bitboard):
            d = data(self.data.width, self.data.height)
            d.bitboards[0] = bitboard
        else:
            d = self.data
        xgr = range(0, d.width, 1)   # X-Grid
        ygr = range(d.h1, 0, -1) if topline else range(d.height, 0, -1)
        tmp = '┌' + ((d.width-1) * '───┬') + '───┐' + "\n"
        for y in ygr:
            tmp += '│'
            for x in xgr:
                filter = 1 << (x * d.h1) + (y - 1)
                tmp += ' '
                if (d.bitboards[0] & filter):
                    tmp += self.signs[1]
                elif (d.bitboards[1] & filter):
                    tmp += self.signs[2]
                else:
                    tmp += self.signs[0]
                tmp += ' │'
            tmp += "\n"
            if (y > 1):
                tmp += '├' + ((d.width-1) * '───┼') + '───┤' + "\n"
        tmp += '└' + ((d.width-1) * '───┴') + '───┘' + "\n"
        num = range(1, d.width + 1)
        tmp += (str().join(map(lambda x: '   '+str(x), num)))[1::]
        return tmp

    def set_topline(self, topline):
        # True, False
        self.topline = topline
