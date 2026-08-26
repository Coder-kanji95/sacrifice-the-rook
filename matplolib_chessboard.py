import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import chess
import io

from matplotlib.widgets import Button
from matplotlib import font_manager

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

def goThruGame(game, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveTxt):
    gameInfo = game[0]
    rookSacInfo = game[1]

    whitePlayer = gameInfo["white"]["username"]
    whiteELO = gameInfo["white"]["rating"]

    blackPlayer = gameInfo["black"]["username"]
    blackELO = gameInfo["black"]["rating"]

    whitePlayerTxt.set_text(f"{whitePlayer} ({whiteELO})")
    blackPlayerTxt.set_text(f"{blackPlayer} ({blackELO})")

    pgn = gameInfo["pgn"]
    chessGame = chess.pgn.read_game(io.StringIO(pgn)) 

    board = chessGame.board()
    moves = list(chessGame.mainline_moves())

    currentMove = [0]

    #update board
    updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

    previousBtn.on_clicked(lambda event: previousTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove, rookSacInfo, moveTxt))
    nextBtn.on_clicked(lambda event: nextTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove, rookSacInfo, moveTxt))

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

def previousTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove, rookSacInfo, moveTxt):
    if currentMove[0] > 0: #check whether there is a previous move to go back to
        board.pop() #if there is, undo the move that was just pushed
        currentMove[0] = currentMove[0] - 1 

        #displaying the move in chess notation
        #ex: e4 e5 & now u hit previous move. now what should happen is the first board.pop() (line 80) undoes e5. now, move that should be shown is e4 (the last one standing upto now), we temporarily undo e4 by a second .pop() & assign it (e4) to a variable so board.san() can get its notation
        #the reason for the second if condition is that if, after the first .pop(), we had no more moves to go back (such as on the first move of the game), then doing board.san() on the move would give an error
        #if it is the case such as the first move, then empty string is in the .set_text() so nothing displayed for the move

        if currentMove[0] > 0: #so, this second if determines if there is still a previous move whose notation can be displayed
            move = board.pop()

            #get the move in standard chess notation (SAN) ex: Nf3 (knight to f3)
            moveNotation = board.san(move)
            moveTxt.set_text(f"Move: {moveNotation}") #show on the matplotlib window

            board.push(move)
        else:
            moveTxt.set_text("")

        updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

def nextTurn(fig, ax, pieceTexts, board, columnMap, pieces, moves, currentMove, rookSacInfo, moveTxt):
    if currentMove[0] < len(moves): #checking whether there moves to go forwards to
        move = moves[currentMove[0]]

        #get the move in standard chess notation (SAN) ex: Nf3 (knight to f3)
        moveNotation = board.san(move)

        isRookSac = False
        materialGained = 0
        for rookSac in rookSacInfo:
            index = rookSac[0]
            materialGained = rookSac[1]

            if index == moves.index(move):
                isRookSac = True
                break

        if isRookSac == True:
            moveTxt.set_text(f"Move: {moveNotation} \n A stunning sacrifice! You sacrificed your ROOOOOOOOOK! Is it the PATH to VICTORY or the ULTIMATE BLUNDER? \n Material gained: {materialGained}") #show on the matplotlib window 
        else:
            moveTxt.set_text(f"Move: {moveNotation}")

        board.push(move)
        currentMove[0] = currentMove[0] + 1

        updateBoard(fig, ax, pieceTexts, board, columnMap, pieces)

def previousGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveTxt):
    if currentGame[0] > 0:
        currentGame[0] = currentGame[0] - 1

        goThruGame(rookSacGames[currentGame[0]], fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveTxt)

def nextGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveTxt):
    if currentGame[0] < len(rookSacGames)-1: #go to the next game if not already at the last game
        currentGame[0] = currentGame[0] + 1

        goThruGame(rookSacGames[currentGame[0]], fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveTxt)

#This is called by app.py (main program file) to display rook sacs. Inside of startDisplay(), it runs the other subroutines as needed
def startDisplay(rookSacs, jetBrainsNF):
    font_manager.fontManager.addfont(jetBrainsNF)
    font = font_manager.FontProperties(fname=jetBrainsNF)

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

    pieceTexts = [] #store text objects of the chess pieces

    whitePlayerTxt = ax.text(-1, 8, "", ha = "right", va = "top", font = font, fontsize = 16, fontweight = "bold")
    blackPlayerTxt = ax.text(-1, 0, "", ha = "right", va = "bottom", font = font, fontsize = 16, fontweight = "bold")

    #text object for displaying the move where the rook sac happens (game review style)
    moveText = ax.text(10, 4, "",  ha = "right", va = "top", font = font, fontsize = 16, fontweight = "bold", wrap = True)

    #start with the first game
    game = rookSacGames[0]
    goThruGame(game, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveText)

    currentGame = [0]
    nextGameBtn.on_clicked(lambda event: nextGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveText))

    previousGameBtn.on_clicked(lambda event: previousGame(rookSacGames, currentGame, fig, ax, columnMap, pieces, previousBtn, nextBtn, pieceTexts, whitePlayerTxt, blackPlayerTxt, moveText))
    
    ax.axis("off")
    plt.show()