""" TicTacToe """
chars = ['\u2500', '\u2502', '\u253C']
table = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
lose=False

def fancy_table():
    return f""" {table[0]} │ {table[1]} │ {table[2]}\n
───┼───┼───
 {table[3]} │ {table[4]} │ {table[5]}\n
 ───┼───┼───
 {table[6]} │ {table[7]} │ {table[8]}
        """

#   X │ O │ X
#  ───┼───┼───
#   O │ X │ O
#  ───┼───┼───
#   X │ O │ X

dafe=0

fancy_table()

while not lose:
    if dafe%2==0:
        cord = input('X: ')
        table[int(cord[0])][int(cord[1])] = False
    else:
        cord = input('O: ')
        table[int(cord[0])][int(cord[1])] = True
    print(fancy_table())
    dafe+=1

