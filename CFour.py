from game import *
from random import *

D = data()
C = core(D)
S = screen(D)
K = keyboard()

S.clear()
print(S.grid(True))

for i in range(5000):
    print("Player", D.player, "ist am Zug")
    C.switch() if C.move(choice(D.playable if D.playable else [0])) else None
    print(S.grid(True))
