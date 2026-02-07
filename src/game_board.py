import random
import string

class GameBoard:
    def __init__(self, size, words):
        self.size = size
        self.found_words = [];
        self.words = [word.upper() for word in words]
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        self.all_word_info = [] # Stores info about all placed words: {"word": str, "start_coord": (r, c), "end_coord": (r, c), "direction": (dx, dy)}
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
        for _ in range(100):
            direction = random.choice(self.DIRECTIONS)
            dx, dy = direction
            for r_start in range(self.size):
                for c_start in range(self.size):
                    if self._can_place(word, r_start, c_start, dx, dy):
                        self._write_word(word, r_start, c_start, dx, dy)
                        
                        end_r = r_start + (len(word) - 1) * dx
                        end_c = c_start + (len(word) - 1) * dy

                        self.all_word_info.append({
                            "word": word,
                            "start_coord": (r_start, c_start),
                            "end_coord": (end_r, end_c),
                            "direction": direction
                        })
                        return True
        return False
    
    def get_all_word_positions(self):
        all_positions_data = []
        for word_info in self.all_word_info:
            word_str = word_info["word"]
            start_r, start_c = word_info["start_coord"]
            dx, dy = word_info["direction"]
            
            positions_set = set()
            for i in range(len(word_str)):
                r = start_r + i * dx
                c = start_c + i * dy
                positions_set.add((r, c))
            
            all_positions_data.append({
                "word": word_str,
                "positions": positions_set
            })
        return all_positions_data
    
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

    def get_word_from_coords(self, start_coord, end_coord):
        (r1, c1) = start_coord
        (r2, c2) = end_coord

        # Horizontal
        if r1 == r2:
            if c1 > c2: c1, c2 = c2, c1 # Swap to read left-to-right
            return "".join(self.board[r1][c] for c in range(c1, c2 + 1))
        # Vertical
        elif c1 == c2:
            if r1 > r2: r1, r2 = r2, r1 # Swap to read top-to-bottom
            return "".join(self.board[r][c1] for r in range(r1, r2 + 1))
        # Diagonal
        elif abs(r1 - r2) == abs(c1 - c2):
            if r1 > r2: # Ensure we read from top-left to bottom-right or top-right to bottom-left
                r1, r2 = r2, r1
                c1, c2 = c2, c1
            
            dr = 1 if r2 > r1 else -1
            dc = 1 if c2 > c1 else -1
            
            word = []
            r, c = r1, c1
            while r != r2 + dr and c != c2 + dc:
                word.append(self.board[r][c])
                r += dr
                c += dc
            return "".join(word)
        else:
            return None

    def validate_and_register_word(self, start_coord, end_coord):
        word = self.get_word_from_coords(start_coord, end_coord)

        if not word:
            return "INVALID_SELECTION"

        # Check both the word and its reverse
        reversed_word = word[::-1]
        
        is_word_in_list = word in self.words
        is_reversed_in_list = reversed_word in self.words
        
        if not is_word_in_list and not is_reversed_in_list:
            return "NOT_A_WORD"

        actual_word = word if is_word_in_list else reversed_word

        for found_word_data in self.found_words:
            if actual_word == found_word_data["word"]:
                return "ALREADY_FOUND"
        
        # Get positions
        positions = set()
        (r1, c1) = start_coord
        (r2, c2) = end_coord
        
        if r1 == r2: # Horizontal
            for c in range(min(c1, c2), max(c1, c2) + 1):
                positions.add((r1, c))
        elif c1 == c2: # Vertical
            for r in range(min(r1, r2), max(r1, r2) + 1):
                positions.add((r, c1))
        else: # Diagonal
            dr = 1 if r2 > r1 else -1
            dc = 1 if c2 > c1 else -1
            r, c = r1, c1
            while True:
                positions.add((r,c))
                if r == r2 and c == c2:
                    break
                r += dr
                c += dc

        self.found_words.append({
            "word": actual_word,
            "positions": positions,
            "color": None 
        })

        return "FOUND"

    def all_words_found(self):
        return len(self.found_words) == len(self.words)