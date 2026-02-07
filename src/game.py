import string
from game_board import GameBoard
from game_display import GameDisplay

class Game:
    def __init__(self, words, board_size):
        self.game_board = GameBoard(size=board_size, words=words)
        self.game_display = GameDisplay(self.game_board)

    def _parse_coord(self, coord_str):
        coord_str = coord_str.upper()
        if len(coord_str) < 2:
            return None
        
        col_char = coord_str[0]
        row_str = coord_str[1:]
        
        if not col_char.isalpha() or not row_str.isdigit():
            return None
            
        col = string.ascii_uppercase.find(col_char)
        row = int(row_str)
        
        if col == -1 or not (0 <= row < self.game_board.size):
            return None
            
        return row, col

    def run(self):
        while not self.game_board.all_words_found():
            self.game_display.display_board()
            self.game_display.display_word_list()

            guess = input("Digite as coordenadas de início e fim (ex: A1 G1) ou 'sair': ").upper()
            if guess == "SAIR":
                break

            parts = guess.split()
            if len(parts) != 2:
                self.game_display.display_message("Entrada inválida. Use o formato: A1 G1")
                continue

            start_str, end_str = parts
            start_coord = self._parse_coord(start_str)
            end_coord = self._parse_coord(end_str)

            if not start_coord or not end_coord:
                self.game_display.display_message("Coordenadas inválidas.")
                continue

            result = self.game_board.validate_and_register_word(start_coord, end_coord)

            if result == "INVALID_SELECTION":
                self.game_display.display_message("Seleção inválida. As palavras devem ser retas (horizontal, vertical ou diagonal).")
            elif result == "NOT_A_WORD":
                self.game_display.display_message("Essa não é uma palavra válida.")
            elif result == "ALREADY_FOUND":
                self.game_display.display_message("Essa palavra já foi encontrada.")
            elif result == "FOUND":
                self.game_display.display_message("Palavra encontrada!")

        self.game_display.display_message("Você chegou ao final do jogo!!!")

        if self.game_board.all_words_found():
            self.game_display.display_message("Todas as palavras foram encontradas. Parabéns!")
        else:
            self.game_display.display_message(f"Infelizmente você não concluiu o jogo.\nPalavras Encontradas {len(self.game_board.found_words)}!")