from board import Board


words = ["MEMORIA", "THREAD", "PROCESSO", "CPU", "TECLADO", "MOUSE"]
board = Board(size=10, words=words)

found = set()

while len(found) < len(words):
    board.display_board()
    
    guess = input("Digite uma palavra (ou 'sair'): ").upper()
    if guess == "SAIR":
        break

    if guess in found:
        print("Essa palavra já foi encontrada.")
        continue

    if guess in words and board.word_exists(guess):
        print("Palavra encontrada!")
        found.add(guess)
    else:
        print("Palavra não encontrada.")
