Squares = [' '] * 9
Players = 'XO'
Board = '''
  0   1   2
  {0} | {1} | {2}
 -----------
3 {3} | {4} | {5} 5
 -----------
  {6} | {7} | {8}
  6   7   8
'''
Win_Conditions = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontals
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # verticals
    (0, 4, 8), (2, 4, 6)  # diagonals
]
def Check_Win(Player):
    for a, b, c in Win_Conditions:
        if {Squares[a], Squares[b], Squares[c]} == {Player}:
            return True
while True:
    print(Board.format(*Squares))
    if Check_Win(Players[1]):
        print(f'{Players[1]} is the winner!')
        break
    if ' ' not in Squares:
        print('Cats game!')
        break
    move = input(f'{Players[0]} to move [0-8] > ')
    if not move.isdigit() or not 0 <= int(move) <= 8 or Squares[int(move)] != ' ':
        print('Invalid move!')
        continue
    Squares[int(move)], Players = Players[0], Players[::-1]