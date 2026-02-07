from game_board import GameBoard
from game_display import GameDisplay
from game import Game;

if __name__ == "__main__":
    words_list = ["MEMORIA", "THREAD", "PROCESSO", "CPU", "TECLADO", "MOUSE"]
    game = Game(words_list, board_size=10)
    game.run()