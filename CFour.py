import sys
import subprocess
import termios
from pynput import keyboard as p_kb


class core():
    #
    # Klasse für die Abbildung des Spieles im Speicher
    # und dessen Manipulation
    #
    bitboards = None  # Bitboards
    counter = None    # Anzahl Spielzüge
    player = None     # Aktueller Spieler
    width = None      # Breite des Spielfeldes
    height = None     # Höhe des Spielfeldes
    h1 = None         # Höhe des Spielfeldes plus eine Zeile
    h2 = None         # rechter Nachbar
    size = None       # Anzahl der Spielzüge, auch Anzahl der Felder
    s1 = None         # Anzahl der Felder plus eine Zeile
    bare = None       # Liste der ersten freien Plätzen jeder Spalte
    bottom = None     # Bitboard der unteren Zeile
    top = None        # Bitboard der Zeile über dem Spielfeld
    rtop = None       # Bitboard der obersten Zeile des Spielfeldes
    btop = None       # Liste aller Bitwerte der obersten Zeile des Spielfeldes

    def __init__(self, width=7, height=6):
        # Konstruktor von Objekten der Klasse 'core'
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

    def switch(self):
        # Seitenwechsel durchführen
        self.player = int(not self.player)

    def move(self, v_row):
        # einen Spielstein einwerfen
        # die Spalte muss regelkonform sein
        self.bitboards[self.player] ^= (1 << self.bare[v_row])  # XOR
        self.bare[v_row] += 1
        self.counter += 1

    def playable(self, v_row):
        # ist ein bestimmter Zug möglich?
        # die Spalte muss im Spielfeld liegen
        return not bool(1 << self.bare[v_row] & self.top)

    def playables(self):
        # Liste aller spielbaren Spalten zurückgeben
        tmp = []
        for i in range(len(self.bare)):
            if self.playable(i):
                tmp.append(i)
        return tmp

    def has_won(self):
        # auf Gewinn prüfen
        bb = self.bitboards[self.player]
        hori = bb & (bb >> self.h1)
        vert = bb & (bb >> 1)
        diag1 = bb & (bb >> self.height)
        diag2 = bb & (bb >> self.h2)
        a = (hori & (hori >> 2*self.h1))
        b = (vert & (vert >> 2))
        c = (diag1 & (diag1 >> 2*self.height))
        d = (diag2 & (diag2 >> 2*self.h2))
        return a | b | c | d


class keyboard:
    #
    # Klasse für Tastatureingaben
    #
    def __init__(self):
        pass

    def read_key(self):
        # ein Tastaturevent lesen
        # https://stackoverflow.com/questions/63144507/how-to-clear-keyboard-event-buffer-pynput-keyboard
        # https://pypi.org/project/pynput/
        # https://www.delftstack.com/de/howto/python/python-detect-keypress/
        with p_kb.Events() as events:
            for event in events:
                print('Received event {}'.format(event))
                break
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


class screen:
    #
    # Klasse für Bildschirmausgaben
    #
    core = None     # Zeiger auf Datenobjekt
    signs = None    # Die Zeichen für LEER, SPIELER A und SPIELER B
    colors = None   # Die Farben der Spielsteine für SPIELER A und SPIELER B

    def __init__(self, core):
        # Konstruktor von Objekten der Klasse 'screen'
        self.core = core
        self.signs = [' ', 'x', 'o']
        self.colors = ['ROT', 'GELB']
        self.topline = False

    def clear(self):
        # Bildschirm löschen
        if sys.platform not in ('win32', 'cygwin'):
            command = 'clear'
        else:
            command = 'cls'
        subprocess.call(command, shell=True)

    def headline(self):
        tmp = "VIER GEWINNT\n"
        tmp += "============\n"
        return tmp

    def grid(self, topline=False, bitboard=None):
        # Gib das Spielfeld von 'self.data' als Textgrafik zurück
        if (bitboard):
            c = core(self.core.width, self.core.height)
            c.bitboards[0] = bitboard
        else:
            c = self.core
        xgr = range(0, c.width, 1)   # X-Grid
        ygr = range(c.h1, 0, -1) if topline else range(c.height, 0, -1)
        tmp = '┌' + ((c.width-1) * '───┬') + '───┐' + "\n"
        for y in ygr:
            tmp += '│'
            for x in xgr:
                filter = 1 << (x * c.h1) + (y - 1)
                tmp += ' '
                if (c.bitboards[0] & filter):
                    tmp += self.signs[1]
                elif (c.bitboards[1] & filter):
                    tmp += self.signs[2]
                else:
                    tmp += self.signs[0]
                tmp += ' │'
            tmp += "\n"
            if (y > 1):
                tmp += '├' + ((c.width-1) * '───┼') + '───┤' + "\n"
        tmp += '└' + ((c.width-1) * '───┴') + '───┘' + "\n"
        tmp += (str().join(map(lambda x: '   '+str(x), xgr)))[1::]
        return tmp

    def status(self):
        # gib alle wichtigen Attribute des Spiels als Zeichenkette zurück
        bbs = self.core.bitboards
        s1 = self.core.s1
        c = self.core.counter
        s = self.core.size
        tmp = ""
        for i in range(len(bbs)):
            tmp += "bitboards[" + str(i) + "]      = "
            tmp += format(bbs[i], "#0"+str(s1)+"b")
            tmp += "\n"
        tmp += "Zug               = " + str(c) + "\n"
        tmp += "Züge Rest         = " + str(s-c) + "\n"
        tmp += "Aktueller Spieler = " + str(self.core.player)
        tmp += " (" + self.colors[self.core.player] + ")\n"
        tmp += "Freie Plätze      = " + str(self.core.bare) + "\n"
        tmp += "Spielbare Spalten = " + str(self.core.playables())
        return tmp

    def game_area(self):
        self.clear()
        tmp = self.headline() + "\n"
        tmp += self.status() + "\n"
        tmp += self.grid() + "\n"
        return tmp


class interface(keyboard, screen):
    #
    # Klasse für das Benutzerinterface
    #
    def __init__(self, core):
        keyboard.__init__(self)
        screen.__init__(self, core)

    def game_mode(self):
        while(self.core.counter < self.core.size):
            pcolor = self.colors[self.core.player]
            print(self.game_area())
            out = "Spieler " + pcolor + " ist am Zug: "
            row = input(out)
            row = int(row)
            if self.core.playable(row):
                self.core.move(row)
                if (self.core.has_won()):
                    print(self.game_area())
                    input("Spieler " + pcolor + " hat gewonnen...")
                    break
                self.core.switch()
            else:
                input("Fehleingabe...")


C = core()
I = interface(C)
I.game_mode()
