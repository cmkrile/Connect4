import random

class ConnectGame:
    # Constructor
    def __init__(self, n, m, k):
        self.board = self.initialize(m, n)
        self.size = m, n
        self.turn = 1
        self.k = k
        self.depth = 5  # AI search depth — raise for harder AI, lower for faster response

    # Creates/initializes board in size m,n
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
        # convert integer values 1 and -1 into 'X' and 'O' respectively
        if entry == 1:
            return 'X'
        elif entry == -1:
            return 'O'
        else:
            return '-'

    def render(self):
        # renders a board on the terminal using X, O and -
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

    # Gets the left to right diagonal
    def get_diagonal(self, row, col):
        lst = []
        m, n = self.size
        shift = (row - col)
        for i in range(m):
            for j in range(n):
                if (i - shift) == j:
                    lst.append(self.board[i][j])
        return lst

    # Gets the right to left diagonal
    def reverse_diagonal(self, row, col):
        lst = []
        m, n = self.size
        shift = (col - row)
        for i in range(m):
            for j in range(n):
                if (i + j) == shift:
                    lst.append(self.board[i][j])
        return lst

    # Gets horizontal row
    def get_horizontal(self, row):
        return self.board[row]

    # Gets vertical column
    def get_vertical(self, col):
        lst = []
        for row in self.board:
            lst.append(row[col])
        return lst

    def connected(self, lst):
        count = 0
        for item in lst:
            if item == self.convert(self.turn):
                count += 1
                if count == self.k:
                    return True
            else:
                count = 0
        return False

    # Check win for a specific symbol string X or O
    def check_win_for(self, symbol):
        rows, cols = self.size
        original_turn = self.turn
        self.turn = 1 if symbol == 'X' else -1

        result = False
        for row in range(rows):
            if self.connected(self.get_horizontal(row)):
                result = True
                break
        if not result:
            for col in range(cols):
                if self.connected(self.get_vertical(col)):
                    result = True
                    break
        if not result:
            for row in range(rows):
                for col in range(cols):
                    if self.connected(self.get_diagonal(row, col)) or \
                       self.connected(self.reverse_diagonal(row, col)):
                        result = True
                        break
                if result:
                    break

        self.turn = original_turn
        return result

    # Goes through entire board and returns a list of all possible moves in (x,y)
    def possible_moves(self, lst):
        moves = []
        for i, row in enumerate(lst):
            for j, col in enumerate(row):
                if col == '-':
                    moves.append([i, j])
        return moves

    # Returns valid column indices the AI/player can drop into
    def valid_columns(self):
        rows, cols = self.size
        valid = []
        for col in range(cols):
            if self.board[0][col] == '-':
                valid.append(col)
        return valid

    # Takes in column and symbol, drops piece to lowest open row
    def make_move(self, col, symbol):
        for row in reversed(self.board):
            if row[col] == '-':
                row[col] = symbol
                return True
        return False

    # Undo a move in a column
    def undo_move(self, col):
        for row in self.board:
            if row[col] != '-':
                row[col] = '-'
                return

    # Randomly chooses column from valid columns
    def random_move(self):
        valid = self.valid_columns()
        if valid:
            col = random.choice(valid)
            self.make_move(col, 'O')

    # Scoring heuristic: evaluate a window of k cells for a given symbol
    def score_window(self, window, symbol, opp_symbol):
        score = 0
        count = window.count(symbol)
        empty = window.count('-')
        opp_count = window.count(opp_symbol)
        if count == self.k:
            score += 100000         
        elif count == self.k - 1 and empty == 1:
            score += 50              
        elif count == self.k - 2 and empty == 2:
            score += 10              

        if opp_count == self.k - 1 and empty == 1:
            score -= 80              
        return score

    # Board evaluation heuristic used by Minimax
    def evaluate_board(self):
        rows, cols = self.size
        ai_sym  = 'O'
        hum_sym = 'X'
        score   = 0
        centre_col = cols // 2
        centre = [self.board[r][centre_col] for r in range(rows)]
        score += centre.count(ai_sym) * 6

        for r in range(rows):
            for c in range(cols - self.k + 1):
                window = [self.board[r][c + i] for i in range(self.k)]
                score += self.score_window(window, ai_sym, hum_sym)
        for c in range(cols):
            for r in range(rows - self.k + 1):
                window = [self.board[r + i][c] for i in range(self.k)]
                score += self.score_window(window, ai_sym, hum_sym)
        for r in range(rows - self.k + 1):
            for c in range(cols - self.k + 1):
                window = [self.board[r + i][c + i] for i in range(self.k)]
                score += self.score_window(window, ai_sym, hum_sym)
        for r in range(self.k - 1, rows):
            for c in range(cols - self.k + 1):
                window = [self.board[r - i][c + i] for i in range(self.k)]
                score += self.score_window(window, ai_sym, hum_sym)

        return score

    # Minimax — returns the best (col, score) for the current player.
        if self.check_win_for('O'):
            return (None, 100000 + depth)   # AI wins
        if self.check_win_for('X'):
            return (None, -(100000 + depth)) # Human wins
        valid = self.valid_columns()
        if not valid or depth == 0:
            return (None, self.evaluate_board())

        if maximizing:
            best_score = float('-inf')
            best_col   = random.choice(valid)
            for col in valid:
                self.make_move(col, 'O')
                _, score = self.miniMax(depth - 1, False)
                self.undo_move(col)
                if score > best_score:
                    best_score = score
                    best_col   = col
            return (best_col, best_score)
        else:
            best_score = float('inf')
            best_col   = random.choice(valid)
            for col in valid:
                self.make_move(col, 'X')
                _, score = self.miniMax(depth - 1, True)
                self.undo_move(col)
                if score < best_score:
                    best_score = score
                    best_col   = col
            return (best_col, best_score)

    # Alpha-Beta Pruning — same as Minimax but prunes branches that
    def alphaBetaPruning(self, depth, alpha, beta, maximizing):
        if self.check_win_for('O'):
            return (None, 100000 + depth)
        if self.check_win_for('X'):
            return (None, -(100000 + depth))
        valid = self.valid_columns()
        if not valid or depth == 0:
            return (None, self.evaluate_board())
        if maximizing:
            best_score = float('-inf')
            best_col   = random.choice(valid)
            for col in valid:
                self.make_move(col, 'O')
                _, score = self.alphaBetaPruning(depth - 1, alpha, beta, False)
                self.undo_move(col)
                if score > best_score:
                    best_score = score
                    best_col   = col
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return (best_col, best_score)
        else:
            best_score = float('inf')
            best_col   = random.choice(valid)
            for col in valid:
                self.make_move(col, 'X')
                _, score = self.alphaBetaPruning(depth - 1, alpha, beta, True)
                self.undo_move(col)
                if score < best_score:
                    best_score = score
                    best_col   = col
                beta = min(beta, best_score)
                if alpha >= beta:
                    break  # Alpha cut-off — maximiser would never allow this branch
            return (best_col, best_score)

    # Use Alpha-Beta to pick and execute the AI's move
    def computer_move(self):
        col, score = self.alphaBetaPruning(self.depth, float('-inf'), float('inf'), True)
        if col is not None:
            self.make_move(col, 'O')

    # Checks horizontal/vertical/both diagonal win conditions
    def check_win(self, symbol):
        rows, cols = self.size
        original_turn = self.turn
        self.turn = 1 if symbol == 'X' else -1
        result = False
        for row in range(rows):
            if self.connected(self.get_horizontal(row)):
                result = True
                break
        if not result:
            for col in range(cols):
                if self.connected(self.get_vertical(col)):
                    result = True
                    break
        if not result:
            for row in range(rows):
                for col in range(cols):
                    if self.connected(self.get_diagonal(row, col)) or \
                       self.connected(self.reverse_diagonal(row, col)):
                        result = True
                        break
                if result:
                    break
        self.turn = original_turn
        return result

    def play(self):
        rows, cols = self.size
        self.board = self.initialize(rows, cols)
        self.render()
        move_counter = 0
        while True:
            available_moves = self.valid_columns()
            if not available_moves:
                print("It's a draw!")
                break
            if move_counter % 2 == 0:
                print("Your Turn (X)")
                try:
                    col = int(input(f"Enter column (0-{cols - 1}): "))
                except ValueError:
                    print("Please enter a number.")
                    continue
                if col < 0 or col >= cols or col not in available_moves:
                    print("Invalid move — column is full or out of range.")
                    continue
                self.make_move(col, 'X')
                move_counter += 1
                self.render()
                if self.check_win('X'):
                    print("You win!")
                    break
            else:
                print("Computer's move (O)...")
                self.computer_move()
                move_counter += 1
                self.render()
                if self.check_win('O'):
                    print("Computer wins!")
                    break