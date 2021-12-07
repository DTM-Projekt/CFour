from core import core

# Konstanten
WIDTH = 7
HEIGHT = 6
PLAYERS = ['GELB', 'ROT']

C = core(width=WIDTH, height=HEIGHT)
print(C.grid())


"""
def player_move():
    allowed_signs = [str(x) for x in range(1, WIDTH + 1)]
    allowed_signs.extend(['e', 'E'])
    cont = True
    while(cont):
        print(PLAYERS[C.player(0)], "ist am Zug")
        row = input("Spalte : ")
        if(row not in allowed_signs):
            continue
        if(row in ['e', 'E']):
            exit()
        row = int(row) - 1
        whitelist = range(0, WIDTH)
        if (row in whitelist):
            cont = False

    return(row)

while True:
    draw_game(0)
    row = player_move()
    make_move(row)
    if(has_won(bb[(player(1))])):
        draw_game(0)
        print(PLAYERS[player(1)], "GEWINNT")
        exit()
"""
