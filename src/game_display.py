import string
from game_board import GameBoard

ANSI_COLORS = [
    "\033[91m",  # vermelho
    "\033[92m",  # verde
    "\033[93m",  # amarelo
    "\033[94m",  # azul
    "\033[95m",  # magenta
    "\033[96m",  # ciano
]

RESET = "\033[0m"


class GameDisplay:
    def __init__(self, game_board: GameBoard):
        self.game_board = game_board

    def display_board(self):
        print("\nTabuleiro:")
        
        # Mostra indices ao redor do tabuleiro
        self._print_column_headers()
        
        self._print_separator()
        self._print_rows()

    def _print_column_headers(self):
        print("   ", end="")
        for j in range(self.game_board.size):
            print(f"{string.ascii_uppercase[j]:2}", end=" ")
        print()

    def _print_separator(self):
        print("   " + "-" * (self.game_board.size * 3))

    def display_word_list(self):
        print("Palavras a encontrar:")
        found_words_list = [fw["word"] for fw in self.game_board.found_words]
        for word in self.game_board.words:
            if word in found_words_list:
                print(f'{word} (encontrada)')
            else:
                print(word)
        print()

    def display_message(self, message):
        print(message)

    def _print_rows(self):
        for i in range(self.game_board.size):
            print(f"{i} |", end=" ")
            for j in range(self.game_board.size):
                cell = self.game_board.board[i][j]

                color_to_apply = None
                for idx, word_data in enumerate(self.game_board.found_words):
                    if (i, j) in word_data["positions"]:
                        color_to_apply = ANSI_COLORS[idx % len(ANSI_COLORS)]
                        break

                if color_to_apply:
                    print(f"{color_to_apply}{cell}{RESET}  ", end="")
                else:
                    print(f"{cell}  ", end="")

            print()
        print()
        print()