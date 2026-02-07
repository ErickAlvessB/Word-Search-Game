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

    def _get_board_lines(self):
        lines = []
        lines.append("Tabuleiro:")
        lines.append(self._get_column_headers_line())
        lines.append(self._get_separator_line())
        lines.extend(self._get_rows_lines())
        return lines

    def _get_column_headers_line(self):
        header_line = "    " # 4 spaces to align with "XX |" for row numbers
        for j in range(self.game_board.size):
            header_line += f" {string.ascii_uppercase[j]} " # Letter with 1 space before and 1 after
        return header_line

    def _get_separator_line(self):
        return "   " + "---" * self.game_board.size # 3 dashes per column

    def _get_word_list_lines(self):
        lines = []
        lines.append("Palavras a encontrar:")
        
        found_words_list = [fw["word"] for fw in self.game_board.found_words]
        max_word_len = 0
        for word in self.game_board.words:
            display_word = word
            if word in found_words_list:
                display_word = f'{word} (encontrada)'
            lines.append(display_word)
            if len(display_word) > max_word_len:
                max_word_len = len(display_word)
        return lines, max_word_len

    def _display_game_layout(self):
        board_lines = self._get_board_lines()
        word_list_lines, max_word_len = self._get_word_list_lines()

        # Calculate max board line length (excluding newline characters)
        max_board_line_len = 0
        for line in board_lines:
            # We need to account for ANSI color codes if they are present
            # A simple way to estimate visible length is to remove them before calculating length
            # This is a heuristic, actual terminal rendering might vary
            clean_line = line.replace(RESET, '')
            for color_code in ANSI_COLORS:
                clean_line = clean_line.replace(color_code, '')
            max_board_line_len = max(max_board_line_len, len(clean_line))

        # Determine spacing
        # Adding a fixed buffer for visual separation
        spacing_buffer = 5 
        
        # Combine lines
        all_lines = []
        max_len = max(len(board_lines), len(word_list_lines))
        for i in range(max_len):
            board_part = board_lines[i] if i < len(board_lines) else ""
            word_list_part = word_list_lines[i] if i < len(word_list_lines) else ""

            # Pad board_part to consistent width for alignment
            clean_board_part = board_part.replace(RESET, '')
            for color_code in ANSI_COLORS:
                clean_board_part = clean_board_part.replace(color_code, '')
            
            current_spacing = max_board_line_len - len(clean_board_part) + spacing_buffer

            all_lines.append(f"{board_part}{' ' * current_spacing}{word_list_part}")
        
        print('\n'.join(all_lines))
        print() # Add an extra newline for better separation from input prompt

    def display_message(self, message):
        print(message)

    def _get_rows_lines(self):
        rows = []
        for i in range(self.game_board.size):
            row_str = f"{i:2} |" # Row number (2 chars) and separator (|)
            for j in range(self.game_board.size):
                cell = self.game_board.board[i][j]

                color_to_apply = None
                for idx, word_data in enumerate(self.game_board.found_words):
                    if (i, j) in word_data["positions"]:
                        color_to_apply = ANSI_COLORS[idx % len(ANSI_COLORS)]
                        break

                if color_to_apply:
                    row_str += f"{color_to_apply} {cell} {RESET}" # Letter with 1 space before and 1 after
                else:
                    row_str += f" {cell} " # Letter with 1 space before and 1 after
            rows.append(row_str)
        return rows