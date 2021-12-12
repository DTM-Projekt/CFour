from game import *
from random import *

D = data()
C = core(D)
I = interface(D)

while(C.is_playable()):
    I.clear()
    print(I.headline())
    print(I.status())
    print(I.grid())


quit()

for i in range(5000):
    print("Player", D.player, "ist am Zug")
    C.switch() if C.move(choice(D.playable if D.playable else [0])) else None
    print(S.grid(True))
