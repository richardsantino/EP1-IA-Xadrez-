import chess
import random

# Arrays dos ultimos 10 estados e 10 movimentos feitos
lastTenStates = ["","","","","", "","","","",""]
lastTenMoves = ["","","","","", "","","","g8h8","h8g8"]

# Função que calcula a utilidade de um movimento a partir da potuação da mesa, e retorna a diferença entre eles
def utilidade(board, player):
  myP = 0
  xsP = 0
  if player.myColor == chess.BLACK:
    myP = countPoits(board, chess.BLACK)
    xsP = countPoits(board, chess.WHITE)
  else:
    myP = countPoits(board, chess.WHITE)
    xsP = countPoits(board, chess.BLACK)
  return myP - xsP

# Exceções importantes pro calculo da utilidade
def exceptions(board, move):
  u = 0
  # Book Moves no começo do jogo é bom
  if board.fullmove_number < 3 and move in ["e7e5", "e7e6", "d7d5", "d7d6", "g8f6", "b8c6", "c7c5", "g7g5"]:
    u += 1
  # Se um movimento coloca o rei do adversário em xeque, é muito bom
  if board.gives_check(move):
        u += 5
  # Se um movimento é uma captura, a utilidade dessa captura é o quanto eu ganho com ela
  if board.is_capture(move):
    my = chess.BaseBoard.piece_at(board, chess.parse_square(str(move)[:2]))
    xs = chess.BaseBoard.piece_at(board, chess.parse_square(str(move)[2:4]))
    if board.is_en_passant(move):
      if my.color == chess.BLACK:
        xs = chess.Piece.from_symbol("P")
      else:
        xs = chess.Piece.from_symbol("p")
    if xs.piece_type - my.piece_type >= 0:
      u += (xs.piece_type - my.piece_type)
  # Se o movimento me leva a um quadrado que está sendo atacado por alguém, é um movimento ruim
  if len(chess.BaseBoard.attacks(board, chess.parse_square(str(move)[2:4]))) > 0:
    u -= 1
  # Se o movimento ou o estado já tiver ocorrido nas ultimas 10 rodadas, é um movimento muito ruim
  board.push(move)
  if chess.BaseBoard.board_fen(board) in lastTenStates or str(move) in lastTenMoves:
    u -= 10
  board.pop()
  # retorna o resultado da análise dessas exceções
  return u

# Algoritmo do minimax semelhante ao que está no repositório, então só vou comentar das diferenças
def minimax(board, vezDoMax, profund, alpha, beta, isLegal, player):
  if board.is_game_over() or profund == 0:
    return None, utilidade(board, player)
  
  # Verifica se eu quero avaliar os movimentos legais ou pseudo-legais
  if isLegal:
    moves = board.legal_moves
  else:
    moves = board.pseudo_legal_moves

  if vezDoMax:
    melhorU = float("-inf")
    melhorMov = list(moves)[random.randint(0,moves.count() - 1)]
    for move in moves:
      exc = exceptions(board, move)   # calcula a utilidade das exceções
      board.push(move)
      mov, u = minimax(board, False, profund - 1, alpha, beta, isLegal, player)
      u += exc                        # Soma o valor das exceções a utiildade
      if u > melhorU:
        melhorU = u
        melhorMov = move
      board.pop()
      alpha = max(alpha, u)
      if beta <= alpha:
        break
    return melhorMov, melhorU
  else:
    piorU = float("inf")
    piorMov = list(moves)[random.randint(0,board.legal_moves.count() - 1)]
    for move in moves:
      exc = exceptions(board, move)   # calcula a utilidade das exceções
      board.push(move)
      mov, u = minimax(board, True, profund - 1, alpha, beta, isLegal, player)
      u += exc                        # Soma o valor das exceções a 
      if u < piorU:
        piorU = u
        piorMov = move
      board.pop()
      beta = min(beta, u)
      if beta <= alpha:
        break
    return piorMov, piorU
    
# Calcula a pontuação do tabuleiro para uma das cores, multiplicando o número de peças pelos seus valores padrões
def countPoits(board, color):
  pawns = chess.BaseBoard.pieces(board, chess.PAWN, color)
  rooks = chess.BaseBoard.pieces(board, chess.ROOK, color)
  knights = chess.BaseBoard.pieces(board, chess.KNIGHT, color)
  bishops = chess.BaseBoard.pieces(board, chess.BISHOP, color)
  queen = chess.BaseBoard.pieces(board, chess.QUEEN, color)
    
  points = (len(pawns) * 1 +
            len(knights) * 3 +
            len(bishops) * 3 +
            len(rooks) * 5 +
            len(queen) * 9
  )
  return points

