import random
class ConnectGame:
    def __init__(self, n, m, k):
        self.board = self.initialize(m, n)
        self.size = m, n
        self.turn = 1
        self.k = k

    def initialize(self, m, n):
        self.size = m, n
        my_board = []
        for i in range(m):
            row = []
            for j in range(n):
                row.append('-')
            my_board.append(row)
        return my_board

    def convert(self, entry):
        if entry == 1:
            return 'X'
        elif entry == -1:
            return 'O'
        else:
            return '-'

    def render(self):
        m, n = self.size
        print(" ", end=" ")
        for i in range(n):
            print(i, end=" ")
        print()
        for i in range(m):
            print(i, end=" ")
            for j in range(n):
                print(self.board[i][j], end=" ")
            print()

    def get_diagonal(self, row, col):
        lst = []
        m, n = self.size
        shift = (row - col)
        for i in range(m):
            for j in range(n):
                if (i - shift) == j:
                    lst.append(self.board[i][j])
        return lst

    def reverse_diagonal(self, row, col):
        lst = []
        m, n = self.size
        shift = (col - row)
        for i in range(m):
            for j in range(n):
                if (i + j) == shift:
                    lst.append(self.board[i][j])
        return lst

    def get_horizontal(self, row):
        return self.board[row]

    def get_vertical(self, col):
        lst = []
        for row in self.board:
            lst.append(row[col])
        return lst

    def connected(self, lst, symbol):
        count = 0
        for item in lst:
            if item == symbol:
                count += 1
                if count == self.k:
                    return True
            else:
                count = 0
        return False

    def possible_moves(self, lst):
        moves = []
        for i, row in enumerate(lst):
            for j, col in enumerate(row):
                if col == '-':
                    moves.append([i, j])
        return moves

    def make_move(self, col, symbol):
        for row in reversed(self.board):
            if row[col] == '-':
                row[col] = symbol
                return True
        return False

    def random_move(self):
        open_spot = self.possible_moves(self.board)
        if open_spot:
            choice = random.choice(open_spot)
            self.make_move(choice[1], 'O')

    COMPUTER = 'O'
    HUMAN = 'X'
    WIN_SCORE = 1000000
    SEARCH_DEPTH = 7

    def valid_columns(self):
        _, cols = self.size
        order = sorted(range(cols), key=lambda c: abs(c - (cols - 1) / 2))
        return [c for c in order if self.board[0][c] == '-']

    def drop(self, col, symbol):
        for r in range(self.size[0] - 1, -1, -1):
            if self.board[r][col] == '-':
                self.board[r][col] = symbol
                return r
        return None

    def undo(self, row, col):
        self.board[row][col] = '-'

    def wins_at(self, row, col, symbol):
        m, n = self.size
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while 0 <= r < m and 0 <= c < n and self.board[r][c] == symbol:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= self.k:
                return True
        return False

    def evaluate(self):
        m, n = self.size
        k = self.k
        score = 0
        center = n // 2
        for r in range(m):
            if self.board[r][center] == self.COMPUTER:
                score += 3
            elif self.board[r][center] == self.HUMAN:
                score -= 3
        for r in range(m):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    er, ec = r + (k - 1) * dr, c + (k - 1) * dc
                    if not (0 <= er < m and 0 <= ec < n):
                        continue
                    window = [self.board[r + i * dr][c + i * dc] for i in range(k)]
                    mine = window.count(self.COMPUTER)
                    theirs = window.count(self.HUMAN)
                    empty = window.count('-')
                    if mine and theirs:
                        continue
                    if mine == k - 1 and empty == 1:
                        score += 50
                    elif mine == k - 2 and empty == 2:
                        score += 5
                    if theirs == k - 1 and empty == 1:
                        score -= 80
                    elif theirs == k - 2 and empty == 2:
                        score -= 5
        return score

    def miniMax(self, depth, maximizing, last=None):
        if last is not None and self.wins_at(last[0], last[1], last[2]):
            if last[2] == self.COMPUTER:
                return self.WIN_SCORE + depth
            return -self.WIN_SCORE - depth
        cols = self.valid_columns()
        if not cols:
            return 0
        if depth == 0:
            return self.evaluate()

        if maximizing:
            best = float('-inf')
            for col in cols:
                row = self.drop(col, self.COMPUTER)
                best = max(best, self.miniMax(depth - 1, False, (row, col, self.COMPUTER)))
                self.undo(row, col)
            return best
        else:
            best = float('inf')
            for col in cols:
                row = self.drop(col, self.HUMAN)
                best = min(best, self.miniMax(depth - 1, True, (row, col, self.HUMAN)))
                self.undo(row, col)
            return best

    def alphaBetaPruning(self, depth, alpha, beta, maximizing, last=None):
        if last is not None and self.wins_at(last[0], last[1], last[2]):
            if last[2] == self.COMPUTER:
                return self.WIN_SCORE + depth
            return -self.WIN_SCORE - depth
        cols = self.valid_columns()
        if not cols:
            return 0
        if depth == 0:
            return self.evaluate()

        if maximizing:
            best = float('-inf')
            for col in cols:
                row = self.drop(col, self.COMPUTER)
                best = max(best, self.alphaBetaPruning(depth - 1, alpha, beta, False, (row, col, self.COMPUTER)))
                self.undo(row, col)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return best
        else:
            best = float('inf')
            for col in cols:
                row = self.drop(col, self.HUMAN)
                best = min(best, self.alphaBetaPruning(depth - 1, alpha, beta, True, (row, col, self.HUMAN)))
                self.undo(row, col)
                beta = min(beta, best)
                if alpha >= beta:
                    break
            return best

    def computer_move(self, depth=None):
        if depth is None:
            depth = self.SEARCH_DEPTH
        best_score = float('-inf')
        best_col = None
        for col in self.valid_columns():
            row = self.drop(col, self.COMPUTER)
            score = self.alphaBetaPruning(depth - 1, float('-inf'), float('inf'),
                                          False, (row, col, self.COMPUTER))
            self.undo(row, col)
            if score > best_score:
                best_score = score
                best_col = col
        if best_col is not None:
            self.make_move(best_col, self.COMPUTER)

    def check_win(self, symbol):
        rows, cols = self.size
        for row in range(rows):
            if self.connected(self.get_horizontal(row), symbol):
                return True
        for col in range(cols):
            if self.connected(self.get_vertical(col), symbol):
                return True
        for row in range(rows):
            for col in range(cols):
                if self.connected(self.get_diagonal(row, col), symbol) or self.connected(self.reverse_diagonal(row, col), symbol):
                    return True
        return False

    def play(self):
        rows, cols = self.size
        self.board = self.initialize(rows, cols)
        self.render()
        move_counter = random.choice([0, 1])
        available_moves = 42
        while ((self.check_win('X') == False) and (self.check_win('O') == False) and available_moves != 0):
            if move_counter % 2 == 0:
                print('Your Turn')
                try:
                    col = int(input("Enter the column 0-6: "))
                except ValueError:
                    print("Invalid Move")
                    continue
                if (col >= 0 and col < 7) and self.make_move(col, 'X'):
                    move_counter += 1
                    available_moves -= 1
                else:
                    print("Invalid Move")
                self.render()
            else:
                print("Computer's move:")
                self.computer_move()
                move_counter += 1
                available_moves -= 1
                self.render()
            if self.check_win('X'):
                print("You win!")
                break
            if self.check_win('O'):
                print("Computer wins!")
                break
            if available_moves == 0:
                print('Its a draw')
                break