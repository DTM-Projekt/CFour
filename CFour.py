from game import *
from random import *

C = core()
I = interface(C)

while(C.is_playable()):
    I.clear()
    print(I.headline())
    print(I.status())
    print(I.grid())
    I.player_next_move()


quit()

for i in range(5000):
    print("Player", C.player, "ist am Zug")
    C.switch() if C.move(choice(D.playable if C.playable else [0])) else None
    print(I.grid(True))
