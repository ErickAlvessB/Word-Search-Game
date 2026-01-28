import random
import string

ANSI_COLORS = [
    "\033[91m",  # vermelho
    "\033[92m",  # verde
    "\033[93m",  # amarelo
    "\033[94m",  # azul
    "\033[95m",  # magenta
    "\033[96m",  # ciano
]

RESET = "\033[0m"


class Board:
    def __init__(self, size, words):
        self.size = size
        self.found_words = [];
        self.words = [word.upper() for word in words]
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        self.generate_board()
    
    def generate_board(self):
        for word in self.words:
            placed = self.place_word(word)
            if not placed:
                print(f"Aviso: não foi possível colocar a palavra '{word}'")
        self.fill_empty_spaces()
    
    def place_word(self, word):
        direction = random.choice(self.DIRECTIONS)
        dx, dy = direction
        for _ in range(100):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self._can_place(word, row, col, dx, dy):
                self._write_word(word, row, col, dx, dy)
                return True
        return False
    
    def fill_empty_spaces(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '':
                    self.board[i][j] = random.choice(string.ascii_uppercase)
    
    def _can_place(self, word, row, col, dx, dy):
        for i in range(len(word)):
            r = row + i * dx
            c = col + i * dy
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.board[r][c] not in ('', word[i]):
                return False
        return True

    def _write_word(self, word, row, col, dx, dy):
        for i in range(len(word)):
            r = row + i * dx
            c = col + i * dy
            self.board[r][c] = word[i]

    def word_exists(self, word):
        for row in range(self.size):
            for col in range(self.size):
                for dx, dy in self.DIRECTIONS:
                    if self._check_direction(word, row, col, dx, dy):
                        return True, row, col, dx, dy
        return False, None, None, None, None


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
                cell = self.board[i][j]

                color = None
                for word in self.found_words:
                    if (i, j) in word["positions"]:
                        color = word["color"]
                        break

                if color:
                    print(f"{color}{cell}{RESET}  ", end="")
                else:
                    print(f"{cell}  ", end="")

            print()
        print()
        print()

    def try_register_word(self, word):
        found, row, col, dx, dy = self.word_exists(word)
        if not found:
            return False

        color = ANSI_COLORS[len(self.found_words) % len(ANSI_COLORS)]
        positions = set()

        for i in range(len(word)):
            r = row + i * dx
            c = col + i * dy
            positions.add((r, c))

        self.found_words.append({
            "positions": positions,
            "color": color
        })

        return True

    
    def _search_from(self, word, row, col):
        for dx, dy in self.DIRECTIONS:
            if self._check_direction(word, row, col, dx, dy):
                return True
        return False
    
    def _check_direction(self, word, row, col, dx, dy):
        for i in range(len(word)):
            r = row + i * dx
            c = col + i * dy

            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False

            if self.board[r][c] != word[i]:
                return False

        return True
    def all_words_found(self):
        if(len(self.found_words) == len(self.words)):
           return True;
    
        return False;