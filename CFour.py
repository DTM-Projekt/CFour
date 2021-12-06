from core import game

# Konstanten
WIDTH = 7
HEIGHT = 6
H1 = HEIGHT + 1
H2 = HEIGHT + 2
SIZE = WIDTH * HEIGHT
S1 = WIDTH * H1
LENGTH = 4
SIGNS = ['x', 'o', ' ']
PLAYERS = ['GELB', 'ROT']


def player(x): return (counter + 1) & 1
# player(0) => Vorhand, player(1) => Rückhand




def draw_game(side=0, topline=False):

    top = '┌' + ((WIDTH-1) * '───┬') + '───┐'
    bottom = '└' + ((WIDTH-1) * '───┴') + '───┘'
    between = '├' + ((WIDTH-1) * '───┼') + '───┤'
    numbers = ("".join(map(lambda x: '   '+str(x), range(1, WIDTH + 1))))[1::]
    x_grid = range(0, WIDTH, 1)
    y_grid = range(HEIGHT, 0, -1)

    if (topline):
        y_grid = range(H1, 0, -1)

    print(top)

    for y in y_grid:

        string = '│'

        for x in x_grid:

            filter = 1 << (x * H1) + (y - 1)
            string += ' '

            if (bb[0] & filter):
                string += SIGNS[0]
            elif (bb[1] & filter):
                string += SIGNS[1]
            else:
                string += SIGNS[2]

            string += ' │'

        if (side == 0):
            print(string)
        else:
            print(string[::-1])

        if (y > 1):
            print(between)

    print(bottom)
    print(numbers)


def player_move():
    allowed_signs = [str(x) for x in range(1, WIDTH + 1)]
    allowed_signs.extend(['e', 'E'])
    cont = True
    while(cont):
        print(PLAYERS[player(0)], "ist am Zug")
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


g = game()
print(g.bb)


init()

conti = True

while(conti):
    draw_game(0)
    row = player_move()
    make_move(row)
    if(has_won(bb[(player(1))])):
        draw_game(0)
        print(PLAYERS[player(1)], "GEWINNT")
        exit()
