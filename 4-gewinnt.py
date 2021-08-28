def bit_set(number, position):
    worth = 2 ** (position-1)
    is_set = number & worth
    if is_set:
        return 1
    else:
        return 0

def draw_game(wert):
    x = 42
    y = 1
    while(x > 0):
        if (bit_set(wert,x) == 1):
            print ('X', end='')
        else:
            print ("o", end='')
        if (y >= 7):
            print()
            y = 0
        else:
            print('|', end='')
        x = x - 1
        y = y + 1
        

b = 0b100010001001010100110010010001010101001010
draw_game(b)
