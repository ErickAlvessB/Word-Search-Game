from game_board import GameBoard
from game_display import GameDisplay

class Game:
    def __init__(self, words, board_size):
        self.game_board = GameBoard(size=board_size, words=words)
        self.game_display = GameDisplay(self.game_board)

    def run(self):
        while not self.game_board.all_words_found():
            self.game_display.display_board()

            guess = input("Digite uma palavra (ou 'sair'): ").upper()
            if guess == "SAIR":
                break

            result = self.game_board.try_register_word(guess)

            if result == "ALREADY_FOUND":
                print("Essa palavra já foi encontrada.")
            elif result == "FOUND":
                print("Palavra encontrada!")
            elif result == "INVALID":
                print("Palavra inválida.")
            else: # This covers cases where the word is not on the board or other False returns
                print("Palavra não encontrada.")


        print("Você chegou ao final do jogo!!!")

        if self.game_board.all_words_found():
            print("Todas as palavras foram encontradas. Parabéns!")
        else:
            print(f"Infelizmente você não concluiu o jogo.\nPalavras Encontradas {len(self.game_board.found_words)}!")