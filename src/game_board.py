import random
import string

class GameBoard:
    def __init__(self, size, words):
        self.size = size
        self.found_words = [];
        self.words = [word.upper() for word in words]
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        self.generate_board()
    
    def generate_board(self):
        successfully_placed_words = []
        for word in self.words:
            placed = self.place_word(word)
            if not placed:
                print(f"Aviso: não foi possível colocar a palavra '{word}'")
            else:
                successfully_placed_words.append(word)
        self.words = successfully_placed_words
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

    def try_register_word(self, word):
        if word not in self.words:
            return "INVALID"

        for found_word_data in self.found_words:
            if word == found_word_data["word"]:
                return "ALREADY_FOUND"

        found, row, col, dx, dy = self.word_exists(word)
        if not found:
            return False

        positions = set()
        for i in range(len(word)):
            r = row + i * dx
            c = col + i * dy
            positions.add((r, c))

        self.found_words.append({
            "word": word,
            "positions": positions,
            "color": None # Color is handled by GameDisplay
        })

        return "FOUND"

    
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