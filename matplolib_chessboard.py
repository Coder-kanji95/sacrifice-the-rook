import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import chess
import io

from matplotlib.widgets import Button

#----------------------------Sub-programs----------------------------------------
def createBoard(lightColour = "#F0D9B5", darkColour = "#B58863"):
    board = np.zeros((8, 8, 3))
    board[::2, ::2] = matplotlib.colors.to_rgb(lightColour)
    board[1::2, 1::2] = matplotlib.colors.to_rgb(lightColour)
    board[::2, 1::2] = matplotlib.colors.to_rgb(darkColour)
    board[1::2, ::2] = matplotlib.colors.to_rgb(darkColour)
    
    return board

def addLabels(ax):
    for i in range(8):
        ax.text(i + 0.5, -0.3, chr(65 + i), ha = "center", va = "center", fontname = "Courier New", fontsize = 16, fontweight = "bold")
        ax.text(-0.3, i + 0.5, str(8 - i), ha = "center", va = "center", fontname = "Courier New", fontsize = 16, fontweight = "bold")

# def addPieces(ax, pieces, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
#     fen = fen.split("/")
    
#     for i, row in enumerate(fen):
#         col = 0
#         for char in row:
#             if char.isdigit():
#                 col = col + int(char)
#             else:
#                 ax.text(col + 0.5, i + 0.56, pieces[char], fontsize = 40, ha = "center", va = "center")
#                 col = col + 1

def updateBoard(fig, ax, pieceTexts, board, columnMap, pieces):
    #remove old piece Text objects (avoid overlap drawing)
    for pieceText in pieceTexts:
        pieceText.remove()
    
    pieceTexts.clear()

    #draw current position
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            square = chess.square_name(square)

            file = square[0]
            rank = square[1]

            x = columnMap[file]
            y = 8 - int(rank) + 0.5

            pieceText = ax.text(x, y, pieces[piece.symbol()], fontsize = 40, ha = "center", va = "center")
            pieceTexts.append(pieceText)

    fig.canvas.draw_idle()

def previousTurn(fig, ax, pieceTexts, board, columnMap, pieces, currentMove):
    if currentMove[0] > 0:
        board.pop()
        currentMove[0] = currentMove[0] - 1

        updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

def nextTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove):
    if currentMove[0] < len(moves):
        move = moves[currentMove[0]]

        board.push(move)
        currentMove[0] = currentMove[0] + 1

        updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)


#This is called by app.py (main program file) to display rook sacs. Inside of startDisplay(), it runs the other subroutines as needed
def startDisplay(rookSacs):
    columnMap = {"a": 0.5, "b": 1.5, "c": 2.5, "d": 3.5, "e": 4.5, "f": 5.5, "g": 6.5, "h": 7.5}

    pieces = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }

    boardState = {
    "a1": "R",
    "a2": "P",
    "a3": "",
    "a4": "",
    "a5": "",
    "a6": "",
    "a7": "p",
    "a8": "r",
    
    "b1": "N",
    "b2": "P",
    "b3": "",
    "b4": "",
    "b5": "",
    "b6": "",
    "b7": "p",
    "b8": "n",
    
    "c1": "B",
    "c2": "P",
    "c3": "",
    "c4": "",
    "c5": "",
    "c6": "",
    "c7": "p",
    "c8": "b",
    
    "d1": "Q",
    "d2": "P",
    "d3": "",
    "d4": "",
    "d5": "",
    "d6": "",
    "d7": "p",
    "d8": "q",
    
    "e1": "K",
    "e2": "P",
    "e3": "",
    "e4": "",
    "e5": "",
    "e6": "",
    "e7": "p",
    "e8": "k",
    
    "f1": "B",
    "f2": "P",
    "f3": "",
    "f4": "",
    "f5": "",
    "f6": "",
    "f7": "p",
    "f8": "b",
    
    "g1": "N",
    "g2": "P",
    "g3": "",
    "g4": "",
    "g5": "",
    "g6": "",
    "g7": "p",
    "g8": "n",
    
    "h1": "R",
    "h2": "P",
    "h3": "",
    "h4": "",
    "h5": "",
    "h6": "",
    "h7": "p",
    "h8": "r",
    }

    chessBoard = createBoard()
    fig, ax = plt.subplots(figsize = (10, 10))
    plt.imshow(chessBoard, extent = (0, 8, 8, 0), origin = "lower")

    # addPieces(ax, pieces)
    addLabels(ax)

    ax.set_xlim(-0.7, 8.7)
    ax.set_ylim(8.7, -0.7)

    ax.set_title("Rook Sacrifice Games", fontsize=20, pad=20)
    
    for rookSac in rookSacs:
        game = rookSac[0]
        index = rookSac[1]
        materialGained = rookSac[2]

        pgn = game["pgn"]
        game = chess.pgn.read_game(io.StringIO(pgn)) 

        board = game.board()
        moves = list(game.mainline_moves())

        currentMove = [0]

        pieceTexts = []

        #update board
        updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

        #buttons to go through moves
        previous = plt.axes([0.35, 0.02, 0.1, 0.05])
        next = plt.axes([0.55, 0.02, 0.1, 0.05])
    
        previousBtn = Button(previous, "◀")
        nextBtn = Button(next, "▶")
    
        previousBtn.on_clicked(lambda event: previousTurn(fig, ax, pieceTexts, board, columnMap, pieces, currentMove))
        nextBtn.on_clicked(lambda event: nextTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove))

    ax.axis("off")
    plt.show()