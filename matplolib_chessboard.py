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

def goThruGame(game, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts):
    gameInfo = game[0]
    #index = rookSac[1]
    #materialGained = rookSac[2]

    pgn = gameInfo["pgn"]
    chessGame = chess.pgn.read_game(io.StringIO(pgn)) 

    board = chessGame.board()
    moves = list(chessGame.mainline_moves())

    currentMove = [0]

    #update board
    updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

    previousBtn.on_clicked(lambda event: previousTurn(fig, ax, pieceTexts, board, columnMap, pieces, currentMove))
    nextBtn.on_clicked(lambda event: nextTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove))

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

def previousGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts):
    if currentGame[0] > 0:
        currentGame[0] = currentGame[0] - 1

        goThruGame(rookSacGames[currentGame[0]], fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts)

def nextGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts):
    if currentGame[0] < len(rookSacGames)-1: #go to the next game if not already at the last game
        currentGame[0] = currentGame[0] + 1

        goThruGame(rookSacGames[currentGame[0]], fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts)

#This is called by app.py (main program file) to display rook sacs. Inside of startDisplay(), it runs the other subroutines as needed
def startDisplay(rookSacs):
    #bringing the rook sac info of each game together
    #structure of rookSacGames list - #[index, materialGained] is the info needed for one rook sac
    #[
    #   [game1,  [ [index, materialGained], [index, materialGained] ] ....],
    #   [game2, [ [index, materialGained], [index, materialGained] ] ....],
    #   ......
    #]
    rookSacGames = []
    for i in range(0, len(rookSacs)-1):
        game = []
        info = []
        sacInfo = []
        nextSacInfo = []

        #check if the current rook sac game & next one are the same
        #if they are, merge the rook sac infos together
        rookSac = rookSacs[i]
        if rookSac[0] == rookSacs[i+1][0]: #the first item (index 0) => the game info dictionary
            game.append(rookSac[0])

            sacInfo.append(rookSac[1]) #the next item is the index of the rook sac as it was found in the main program file (index+1 is the move number where thr rook sac happens)
            sacInfo.append(rookSac[2]) #rookSac[2] is the material recovered by the player who sac'd the rook

            nextSacInfo.append(rookSacs[i+1][1]) #these are the same as rookSac[1] & rookSac[2] but its from the next inner list in rookSacs list
            nextSacInfo.append(rookSacs[i+1][2])

            info.append(sacInfo)
            info.append(nextSacInfo)

            game.append(info)
            rookSacGames.append(game)

    columnMap = {"a": 0.5, "b": 1.5, "c": 2.5, "d": 3.5, "e": 4.5, "f": 5.5, "g": 6.5, "h": 7.5}

    pieces = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }

    chessBoard = createBoard()
    fig, ax = plt.subplots(figsize = (10, 10))
    plt.imshow(chessBoard, extent = (0, 8, 8, 0), origin = "lower")

    addLabels(ax)

    ax.set_xlim(-0.7, 8.7)
    ax.set_ylim(8.7, -0.7)

    ax.set_title("Rook Sacrifice Games", fontsize=20, pad=20)

    #buttons to go through moves
    #plt.axes([left, bottom, width, height])
    previousMove = plt.axes([0.36, 0.02, 0.1, 0.05])
    nextMove = plt.axes([0.57, 0.02, 0.1, 0.05])

    previousBtn = Button(previousMove, "◀")
    nextBtn = Button(nextMove, "▶")

    #buttons to go to next & previous game
    prevGame = plt.axes([0.15, 0.02, 0.1, 0.05])
    nxtGame = plt.axes([0.76, 0.02, 0.1, 0.05])

    previousGameBtn = Button(prevGame, "Previous Game")
    nextGameBtn = Button(nxtGame, "Next Game")

    pieceTexts = []
    #start with the first game
    game = rookSacGames[0]
    goThruGame(game, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts)

    currentGame = [0]
    nextGameBtn.on_clicked(lambda event: nextGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts))

    previousGameBtn.on_clicked(lambda event: previousGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts))
    
    ax.axis("off")
    plt.show()