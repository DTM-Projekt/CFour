# CFour // Connect Four // Vier Gewinnt

Das Spiel __Vier Gewinnt__ programmiert in Python.

## Begriffe

Im Quellcode werden ausschließlich englische Begriffe verwendet.
Desweiteren müssen die Aspekte der Spielmechanik in eindeutigen Begriffen festgesetzt werden,
um die Lesbarkeit des Quellcodes zu sichern.
In der folgenden Tabelle werden solche Definitionen zusammengefasst.
|Englisch|Deutsch|Klärung|im Quellcode|
|-|-|-|-|
|color|Farbe|mögliche Farben eines Spielsteines<br>0 = rot, 1 = gelb|color|
|column,<br>vertical row|Spalte|eine senkrechte Reihe des Spielfeldes|row_v|
|diagonal|Diagonale|eine schräge Reihe des Spielfeldes|slash = '/'<br>bslash = '\\'|
|grid|Gitter|das originale Spielfeld|grid|
|line,<br>horizontal row|Zeile|eine waagerechte Reihe des Spielfeldes|row_h|
|man|Stein|ein Spielstein|man|
|men|Steine|viele Spielsteine|men|
|row|Reihe|eine Reihe von vier Spielsteinen,<br>egal welcher Ausrichtung|row|

## Quellen

Allgemein
* https://de.m.wikipedia.org/wiki/Vier_gewinnt
* https://tromp.github.io/c4/c4.html
* https://blog.gamesolver.org/

Connect Four Solver
* https://github.com/qu1j0t3/fhourstones
* https://github.com/PascalPons/connect4

Andere Projekte
* https://www.mathematik.uni-muenchen.de/~spielth/artikel/VierGewinnt.pdf
* https://www.ke.tu-darmstadt.de/lehre/arbeiten/bachelor/2006/Baier_Hendrik.pdf
* http://www.informatik.uni-trier.de/~fernau/DSL0607/Masterthesis-Viergewinnt.pdf
* https://www.tobiaskohn.ch/jython/students_viergewinnt-de.html
