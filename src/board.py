import random
import string

class Board:
    def __init__(self, size, words):
        self.size = size
        self.words = [word.upper() for word in words]
        self.board = [['' for _ in range(size)] for _ in range(size)]
        
        self.generate_board()

    def generate_board(self):
        for word in self.words:
            self.place_word(word)
    
        self.fill_empty_spaces()

    def place_word(self, word):
        row = random.randint(0, self.size - 1)

        if(len(word) > self.size):
            return
        
        col = random.randint(0, self.size - len(word))

        for i, letter in enumerate(word):
            self.board[row][col + i] = letter
        
    def fill_empty_spaces(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '':
                    self.board[i][j] = random.choice(random.choice(string.ascii_uppercase))

    def display_board(self):
        print("\nTabuleiro:")
        
        # Mostra indices ao redor do tabuleiro
        self._print_column_headers()
        
        self._print_separator()
        self._print_rows()


    def _print_column_headers(self):
        print("   ", end="")
        for j in range(self.size):
            print(f"{j:2}", end=" ")
        print()

    def _print_separator(self):
        print("   " + "-" * (self.size * 3))

    def _print_rows(self):
        for i in range(self.size):
            print(f"{i} |", end=" ")
            for j in range(self.size):
                cell = self.board[i][j] if self.board[i][j] else '.'
                print(f"{cell:2}", end=" ")
            print()

        print()