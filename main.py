import chess
import random

board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')


def Eval(board,maximizingPlayer):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    evaluation = 0
    whiteMaterial = 0
    blackMaterial = 0

    # Evaluate piece values on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.piece_type
            piece_color = piece.color
            if piece_color == chess.WHITE:
                evaluation += piece_values[piece_type]
                whiteMaterial += piece_values[piece_type]
            else:
                evaluation -= piece_values[piece_type]
                blackMaterial += piece_values[piece_type]


    # Calculate material difference
    MaterialDif = whiteMaterial - blackMaterial
    evaluation += MaterialDif

    # Add additional factors here (e.g., pawn structure, king safety, piece mobility)
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            evaluation += -9999
        else:
            evaluation += 9999
        #print("Checkmate found!")
        print(board.move_stack,evaluation)


    return evaluation


def AlphaBeta(board, depth, alpha, beta, maximizingPlayer):
    WhitePieceMobility = 0
    BlackPieceMobility = 0
    #FUNCTIONS THAT ARE NOT SEARCH BUT IMPORTANT MOVE ORDERS!!!

    def IsCapture(board, move):

        source_square = move.from_square
        destination_square = move.to_square
        before_piece = board.piece_at(source_square)

        if before_piece is not None:
            after_piece = board.piece_at(destination_square)

            # Check for normal captures or en passant captures
            if after_piece is not None and after_piece.color != before_piece.color:
                return True

            # Check for pawn promotion captures
            if move.promotion is not None:
                return True

        return False
    #ORDER MOVES TO IMPORVE EFFICIENCY ALSO TO BE ABLE TO FIND CHECKMATE IN THE SHORTEST ROUTE
    def OrderMoves(board,moves):
        def move_priority(move):
            if board.is_checkmate():
                return 5  # Checkmate should have highest priority
            if board.promoted:
                return 4
            if board.is_capture(move):
                return 2
            if board.gives_check(move):
                return 4
            if board.is_castling(move):
                return 1
            return 0

        ordered_moves = sorted(moves, key=move_priority, reverse=True)

        return ordered_moves


    #ACTUAL AI ALPHABETA PRUNING ALGORITHM
    if board.is_game_over() or depth == 0:
        # Game is over, return the evaluation of the final position
        return None, Eval(board,maximizingPlayer)

    bestMove = None
    if maximizingPlayer:
        maxEval = -9999
        moves = board.legal_moves
        BlackPieceMobility = moves.count()
        LegalMoves = OrderMoves(board,moves)
        for move in LegalMoves:

            board.push(move)
            if board.is_check() or IsCapture(board,move) == True:
                _, eval = AlphaBeta(board, depth, alpha, beta, maximizingPlayer=False)
            else:
                _, eval = AlphaBeta(board, depth - 1, alpha, beta, maximizingPlayer=False)
            board.pop()

            if eval > maxEval:
                maxEval = eval
                bestMove = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return bestMove, maxEval
    else:
        minEval = 9999
        moves = board.legal_moves
        LegalMoves = OrderMoves(board, moves)
        WhitePieceMobility = moves.count()
        for move in LegalMoves:
            board.push(move)
            if board.is_check() or IsCapture(board,move) == True:
                _, eval = AlphaBeta(board, depth, alpha, beta, maximizingPlayer=True)
            else:
                _, eval = AlphaBeta(board, depth - 1, alpha, beta, maximizingPlayer=True)
            board.pop()

            if eval < minEval:
                minEval = eval
                bestMove = move

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return bestMove, minEval




for i in range(50):

    usr_input = input("What do you want to do?: ")
    board.push_san(usr_input)

    AImove, _ = AlphaBeta(board, depth=4, alpha=-9999, beta=9999, maximizingPlayer=False)
    if AImove is None:
        print("AI cannot make a move. Stalemate or checkmate.")
        break

    print("\n")
    board.push(AImove)
    print(AImove)
    print(board)

    if board.is_checkmate():
        print("AI Wins!!!")
        break


    if board.is_checkmate():
        print("Human Wins!!!")
        break
