from board import Board

words = ["MEMORIA", "THREAD", "PROCESSO", "CPU", "TECLADO", "MOUSE"]
board = Board(size=10, words=words)

found = set()

while not board.all_words_found():
    board.display_board()

    guess = input("Digite uma palavra (ou 'sair'): ").upper()
    if guess == "SAIR":
        break

    result = board.try_register_word(guess)

    if result == "ALREADY_FOUND":
        print("Essa palavra já foi encontrada.")
    elif result == "FOUND":
        print("Palavra encontrada!")
    elif result == "INVALID":
        print("Palavra inválida.")
    else:
        print("Palavra não encontrada.")

print("Você chegou ao final do jogo!!!")

if(board.all_words_found()):
    print("Todas as palavras foram encontradas. Parabéns!")

else:
    print(f"Infelizmente você não concluiu o jogo.\nPalavras Encontradas {len(board.found_words)}!")
