# CFour // Connect Four // Vier Gewinnt

Das Spiel __Vier Gewinnt__ programmiert in Python.

## Abhängigkeiten
Für die Ausführung des Programms __Vier Gewinnt__
muss auf dem Zielrechner __Python__ in der __Version 3__ installiert sein.

Dann werden noch einige Python-Bibliotheken installiert:
```
pip3 install pynput
```

## Installation des Spiels
```
git clone git@github.com:DTM-Projekt/CFour.git
```

## Begriffe

Im Quellcode werden englische Bezeichner verwendet.
|Englisch|Deutsch|Klärung|im Quellcode|
|:-|:-|:-|:-|
|color|Farbe|mögliche Farben eines Spielsteines. 0 = rot, 1 = gelb|color|
|diagonal row|Diagonale|eine schräge Reihe des Spielfeldes. / oder \\ |row_d1, row_d2|
|grid|Gitter|das originale Spielfeld|grid|
|height|Höhe|Y-Ausdehnung des Spielfeldes|height|
|horizontal row|Zeile|eine waagerechte Reihe des Spielfeldes|row_h|
|man|Stein|ein Spielstein|man|
|men|Steine|viele Spielsteine|men|
|player|Spieler|es spielen zwei Spieler gegeneinander|player|
|row|Reihe|eine Reihe im Gitter des Spielfeldes, egal welcher Ausrichtung|row|
|side|Seite|Sicht von vorn oder hinten auf das Spielfeld|side|
|vertical row|Spalte|eine senkrechte Reihe des Spielfeldes (auch engl. = column)|row_v|
|width|Breite|X-Ausdehnung des Spielfeldes|width|

## Quellen

Allgemeines über das Spiel 'Vier Gewinnt'
* https://de.m.wikipedia.org/wiki/Vier_gewinnt
* https://tromp.github.io/c4/c4.html
* https://blog.gamesolver.org/

Connect Four Solver (Spieletheorie, Datenhandling)
* https://github.com/qu1j0t3/fhourstones
* https://github.com/PascalPons/connect4

Andere 'Vier Gewinnt' - Projekte
* https://www.mathematik.uni-muenchen.de/~spielth/artikel/VierGewinnt.pdf
* https://www.ke.tu-darmstadt.de/lehre/arbeiten/bachelor/2006/Baier_Hendrik.pdf
* http://www.informatik.uni-trier.de/~fernau/DSL0607/Masterthesis-Viergewinnt.pdf
* https://www.tobiaskohn.ch/jython/students_viergewinnt-de.html
* https://github.com/KeithGalli/Connect4-Python
