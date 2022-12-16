""" TicTacToe """
from os import system
import sys

table:list = [[None, None, None], [None, None, None], [None, None, None]]
end_game:bool = False

def list_sameitem(lst, eqt):
    """  """
    for i in range(len(lst)):
        if not lst[i] == eqt:
            return False
            break
    else:
        return True

def fancy_table():
    return f"""
┌─1─╥─2─╥─3─┐
1 {table[0][0]} ║ {table[0][1]} ║ {table[0][2]} │
╞═══╬═══╬═══╡
2 {table[1][0]} ║ {table[1][1]} ║ {table[1][2]} │
╞═══╬═══╬═══╡
3 {table[2][0]} ║ {table[2][1]} ║ {table[2][2]} │
└───╨───╨───┘
        """.replace('None', ' ').replace('False', 'X').replace('True', 'O')

def wincheck():
    win_table = [
        [table[0][0], table[1][0], table[2][0]],
        [table[0][1], table[1][1], table[2][1]],
        [table[0][2], table[1][2], table[2][2]],

        [table[0][0], table[0][1], table[0][2]],
        [table[1][0], table[1][1], table[1][2]],
        [table[2][0], table[2][1], table[2][2]],

        [table[0][0], table[1][1], table[2][2]],
        [table[0][2], table[1][1], table[2][0]]
    ]
    global end_game
    for l in win_table:
        if list_sameitem(l, True):
            print('o wins')
            print('Thanks for playing!')
            end_game=True
            break
        if list_sameitem(l, False):
            print('x wins')
            print('Thanks for playing!')
            end_game=True
            break

# ┌─1─╥─2─╥─3─┐
# 1 X ║ O ║ X │
# ╞═══╬═══╬═══╡
# 2 O ║ X ║ O │
# ╞═══╬═══╬═══╡
# 3 X ║ O ║ X │
# └───╨───╨───┘
dafe:int = 0

system('cls')
print(fancy_table())

while not end_game:
    wincheck()
    if end_game: break;
    if dafe%2==0:
        try:
            cord = input('X: ')
        except KeyboardInterrupt:
            system('cls')
            sys.exit()
        table[int(cord[1])-1][int(cord[0])-1] = False
    else:
        try:
            cord = input('O: ')
        except KeyboardInterrupt:
            system('cls')
            sys.exit()
        table[int(cord[1])-1][int(cord[0])-1] = True
    system('cls')
    print(fancy_table())
    dafe+=1
