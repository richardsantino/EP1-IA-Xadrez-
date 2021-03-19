import chess
import chess.svg
import os 
from MinimaxFeatures import minimax, lastTenMoves, lastTenStates

# Classe de jogador Victor Hugo
class VictorHugoPlayer:
  myColor = chess.BLACK
  def VHMove(board, player):
    # Se houverem movimentos legais, entra no if, se não, significa que o rei provavelmente está em xeque,
    # e só tem movimentos pseudo-legais (é pra isso que serve o último bool na chamada da função)
    if board.legal_moves.count() > 0:
      move, valor = minimax(board, True, 4, float("-inf"), float("inf"), True, player)
      return move
    else:
      move, valor = minimax(board, True, 4, float("-inf"), float("inf"), False, player)
      return move

# Classe do jogo
class game:
  # Imprime o estado do jogo no terminal
  def gameState(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(board)

  # Chamada na vez do computador jogar, sempre as pretas
  # Chama o jogador pra ele escolher o movimento e o faz
  # Depois guarda o movimento e o estado num array com os ultimos 10 movimentos e estados, pra evitar um loop
  def computerTurn(player, board):
    print("Adversário")
    move = player.VHMove(board, player)
    board.push(move)
    lastTenStates.append(chess.BaseBoard.board_fen(board))
    lastTenStates.pop(0)
    lastTenMoves.append(str(move))
    lastTenMoves.pop(0)
  
  # Chamada na vez da pessoa jogar, sempre as brancas
  # Pede a jogada na notação UCI e verifica se ela é uma jogada legal
  # Se não for, pede por uma nova jogada
  def humanTurn(board):
    while True:
      print("\nSua vez!")
      jogada = input("Insira sua jogada pela notação UCI: ")
      jogUCI = chess.Move.from_uci(jogada)
      if jogUCI in board.legal_moves:
        board.push(jogUCI)
        return
      else:
        print("Jogada inválida, tente de novo :(")

# Instancia de um novo jogo
class newGame:
  def start(botColor):
    board = chess.Board()   # Cria um tabuleiro
    jogo = game             # Cria uma instância do jogo
    vh = VictorHugoPlayer
    vh.myColor = botColor   # Cria uma instância do jogador

    while not board.is_game_over(): # Mantem o jogo rodando
      jogo.gameState(board)
      if board.is_game_over(): 
        break
      if botColor == chess.BLACK:
        jogo.humanTurn(board)
        jogo.gameState(board)
        if board.is_game_over(): 
          break
        jogo.computerTurn(vh, board)
      else:
        jogo.computerTurn(vh, board)
        jogo.gameState(board)
        if board.is_game_over(): 
          break
        jogo.humanTurn(board)

    # Quando der game over, o resultado é filtrado
    res = board.result()
    if board.is_stalemate(): print("Empate!")
    elif board.is_insufficient_material(): print("Material insulficiente!")
    elif board.is_seventyfive_moves(): print("Empate por repetição de movimentos!")
    elif board.is_fivefold_repetition(): print("Empate por repetição de estados!")
    elif board.is_variant_end(): print("O jogo chegou ao fim!")
    elif board.is_checkmate: print("Xeque-mate! Branco vence!" if res == "1-0" else "Xeque-mate! Preto vence!")


novoJogo = newGame
print("Escolha sua cor:\n1- Preto\n2-Branco")
c = input("Sua escolha: ")
color = chess.BLACK
if c == "1": color = chess.WHITE
novoJogo.start(color)