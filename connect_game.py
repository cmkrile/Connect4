import random
class ConnectGame:
    # Constructor
    def __init__(self, n, m, k):
        self.board = self.initialize(m, n)
        self.size = m, n
        self.turn = 1
        self.k = k

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

    # Uses convert method to check if there are 4 in a row of either X or O's
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


    # Goes through entire board and returns a list of all possible move in (x,y)
    # Based upon Figure 9.5.4: Iterating through multi-dimensional lists using enumerate().
    def possible_moves(self, lst):
        moves = []
        for i, row in enumerate(lst):
            for j, col in enumerate(row):
                if col == '-':
                    moves.append([i, j])
        return moves

    # Takes in location of intended move and sets x,y location to X or O
    # Used reversed based on Table 9.2.1: Available list methods.
    def make_move(self, col, symbol):
        for row in reversed(self.board):
            if row[col] == '-':
                row[col] = symbol
                break

    # Randomly chooses x,y location from possible_moves list and sets location to O for computer move
    def random_move(self):
        open_spot = self.possible_moves(self.board)
        if open_spot:
            choice = random.choice(open_spot)
            self.make_move(choice[1], 'O')
    
    # Generates tree based upon available moves and chooses optimal choice
    # def computer_move(self):


    # Checks horizontal/vertical/both diagonal win conditions using connected, get horizontal/vertical/diagonal/reverse_diagonal methods
    def check_win(self, symbol):
        rows, cols = self.size
        for row in range(rows):
            if self.connected(self.get_horizontal(row)):
                return True
        for col in range(cols):
            if self.connected(self.get_vertical(col)):
                return True
        for row in range(rows):
            for col in range(cols):
                if self.connected(self.get_diagonal(row, col)) or self.connected(self.reverse_diagonal(row, col)):
                    return True
        return False

    # Initializes board with 7 columns, 6 rows, and uses while loop to track whose turn it is
    # Checks if the board is filled completely using available_moves
    # Confirms if user choice is a valid location/is in bounds of size of board as well as in list of possible_moves
    # Uses random_move method for computers turn to make a move
    # Checks all 3 win conditions and if any 3 are met breaks the while loop and prints winner/draw
    def play(self):
        rows, cols = self.size
        self.board = self.initialize(rows, cols)
        self.render()
        move_counter = 0
        available_moves = 42
        while ((self.check_win('X') == False) and (self.check_win('O') == False) and available_moves != 0):
            if move_counter % 2 == 0:
                print('Your Turn')
                col = int(input("Enter the column 0-6: "))
                if (col >= 0 and col < 7) and self.possible_moves(self.board):
                    self.make_move(col, 'X')
                    move_counter += 1
                    available_moves -= 1
                else:
                    print("Invalid Move")
                self.render()
            else:
                print("Computer's move:")
                self.random_move()
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

    # Implementation of miniMax concept
    # 
    def miniMax():
        #

    # Implementation of alphaBetaPruning concept
    #
    def alphaBetaPruning():
        #

