#GUI Frameworks
import customtkinter as ctk
from tkinter import messagebox

#Input validation
from validation.inputValidation import titleValidation

#For making API requests & manipulating them
import requests
import json

#For the program to interact with system to get icon file, custom theme file...
import os
import sys

#To play the sound file (THE ROOOOOOOOK) when the button is clicked
import pygame

#To parse PGNs & detect rook sacrifices (in other words - core functionality)
import io
import chess.pgn

#To run background archive fetching & rook sac detecting operations concurrently with main GUI thread
import threading

#----------------------------Sub-programs----------------------------------------
def workerThread(pInpFrame, pOutFrame, pUserEntry, app):
    thread1 = threading.Thread(target=searchRookSacs, args=(pInpFrame, pOutFrame, pUserEntry, app))
    thread1.start()

def searchRookSacs(pInpFrame, pOutFrame, pUserEntry, app):
    #get the Chess.com username from the entry widget & pass it to validation
    username = pUserEntry.get().strip()
    valid = titleValidation(username)

    #if username is of valid format, send API request
    if valid == True:
        #send API request (with user agent - as Chess.com requires this to identify requests)
        headers = {
            "User-Agent": "RookSacCheckerTool/1.0 (kavijasaluwadana@gmail.com)"
        }

        url = f"https://api.chess.com/pub/player/{username}/games/archives"

        #credit: thanks https://www.endpoint51.com/python-api-error-handling/ for the very robust try/except error handling
        try:
            #try to send API request, if successful get the links to monthly archives of games, in the json. if not, appropiate error msg is displayed
            #NOTE: Do try-except method for error handling in my NEA as well
            response = requests.get(url, headers = headers, timeout = 5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "The request timed out. The server may be slow or unreachable.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Could not reach the server. Check the network or the URL.")
        except requests.exceptions.HTTPError as error:
            messagebox.showerror("Error", f"The server returned an error status: {error.response.status_code}")
        except requests.exceptions.JSONDecodeError:
            messagebox.showerror("Error", "The server returned a response that was not valid JSON.")
        except requests.exceptions.TooManyRedirects:
            messagebox.showerror("Error", "The request followed too many redirects. Check the URL.")
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error", f"An unexpected request error occurred: {error}")
        else:
            results = response.json()

            #check if there are actually links to monthly archives
            #new users (just created Chess.com acc) will not
            if len(results["archives"]) == 0:
                messagebox.showwarning("Error", f"{username}, you have no public games in the archive")
                gamesExist = False
            else:
                gamesExist = True

            if gamesExist == True:
                archives = results["archives"]
                allMonths = []

                #get each month's games & add it to a list
                for index in range(0, len(archives)):
                    try:
                        response = requests.get(archives[index], headers = headers, timeout = 5)
                        response.raise_for_status()
                    except requests.exceptions.Timeout:
                        messagebox.showerror("Error", "The request timed out. The server may be slow or unreachable.")
                    except requests.exceptions.ConnectionError:
                        messagebox.showerror("Error", "Could not reach the server. Check the network or the URL.")
                    except requests.exceptions.HTTPError as error:
                        messagebox.showerror("Error", f"The server returned an error status: {error.response.status_code}")
                    except requests.exceptions.JSONDecodeError:
                        messagebox.showerror("Error", "The server returned a response that was not valid JSON.")
                    except requests.exceptions.TooManyRedirects:
                        messagebox.showerror("Error", "The request followed too many redirects. Check the URL.")
                    except requests.exceptions.RequestException as error:
                        messagebox.showerror("Error", f"An unexpected request error occurred: {error}")
                    else:
                        monthlyResults = response.json()
                        allMonths.append(monthlyResults)

                #exclude variant games
                #the list 'allMonths' contains dictionaries of games in a single month (i think)
                #so in each iteration of the for loop, 'month' is a dict of games in a month
                #each game's data is stored in a dict & all the games of a month is in a list (this is what 'monthGames' is), accessible thru the "games" key of 'month' dict
                toReview = []
                for month in allMonths:
                    monthGames = month["games"]

                    #we iterate thru the list (acquired by the "games" key) to check the value of the "rules" key to each dict (chess game) to make sure each game checked for rook sacs is standard chess (the part where variants are filtered)
                    for game in monthGames:
                        if game["rules"] == "chess":
                            toReview.append(game)

                #pass this list (toReview) into the 'brains'/chess logic subroutine that will check each game for rook sacs
                #list 'toReview' - contains all public games of standard chess
                rookSacs = theBrains(pInpFrame, pOutFrame, toReview, username)

                app.after(0, displayRookSacs(rookSacs, pInpFrame, pOutFrame))

def theBrains(pInpFrame, pOutFrame, gameArchive, pUsername):
    rookSacGames = []

    for game in gameArchive:
        pgn = game["pgn"] #grab pgn of the chess game

        #get the colour of pieces the user was playing with
        #internally (in python-chess) chess.WHITE & chess.BLACK are boolean (capturedPiece.color also returns a bool)
        if game["white"]["username"].lower() == pUsername.lower():
            playerColour = chess.WHITE
        else:
            playerColour = chess.BLACK

        chessGame = game
        #allow python-chess to parse the pgn. python-chess expects a file but the pgn rn is a string so StringIO temporarily turns the string into an in-memory file
        game = chess.pgn.read_game(io.StringIO(pgn)) 
        board = game.board() #create a board

        #chess piece values
        pieceValues = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }

        moves = list(game.mainline_moves())
        #the pgn stores a sequence of moves & a for loop is used to replay them
        for index, move in enumerate(moves):

            #check whether the move is a capture of a piece or just a normal move of a piece moving to empty square. returns True/False
            if board.is_capture(move) == True:
                capturedPiece = board.piece_at(move.to_square)

                #sometimes, a move can be capture yet nothing on the move's destination square (EN PASSANT!!)
                if capturedPiece is not None:
                    #check if the captured piece is a rook

                    #internally, python-chess has constants for each piece, like chess.PAWN = 1, chess.ROOK = 4 & .piece_type also returns a num const so if condition checks if the num corresponding to the capturedPiece is the same as the num corresponding to a ROOK
                    #Also, the num constants are NOT the values of the pieces!

                    #check if the colour of the rook captured is the colour of pieces the user is playing with
                    #if both are true, that means the user's rook was captured....
                    if (capturedPiece.piece_type == chess.ROOK) and (capturedPiece.color == playerColour):
                        #.....meaning.....POSSIBLE ROOK SACRIFICE - start the heuristic
                        #the board is currently before the rook capture. make a copy of the board & push the rook capture
                        #the reason a copy is made is cuz to look ahead for material compensation without messing up the main loop
                        heuristicBoard = board.copy()
                        heuristicBoard.push(move)

                        lookAhead = 6 #NOTE: EXPERIMENT WITH THIS - Look ahead n moves => each player gets n/2 turns
                        materialGained = 0

                        #index+1 : as index corresponds to the current move - where the user's rook gets captured
                        #index+7 : as we want to check the next 6 moves (next 6 indexes) - end index not included
                        for futureMove in moves[index+1:index+7]:
                            #if the move is a capture & the user made this capture.....
                            if (heuristicBoard.is_capture(futureMove) == True) and (heuristicBoard.turn == playerColour):
                                futureCapturedPiece = heuristicBoard.piece_at(futureMove.to_square)

                                #......record how much material the user gains from the capture of this piece
                                materialGained = materialGained + pieceValues[futureCapturedPiece.piece_type]

                            heuristicBoard.push(futureMove)

                        #after going thru 6 moves (our user gets 3 turns), check if the total material they gained in this period is less than 5 points (the value of a rook). If so, that may mean it's a sacrifice
                        if materialGained < 5:
                            rookSacGame = []
                            rookSacGame.append(chessGame)
                            rookSacGame.append(index)
                            rookSacGame.append(materialGained)

                            rookSacGames.append(rookSacGame)

            board.push(move) #play the move where the user's rook is captured

    #return a (possibly massive) list of all rook sacs
    return rookSacGames

def displayRookSacs(pRookSacs, pInpFrame, pOutFrame):
    return

def rookSound():
    pygame.mixer.init()
    pygame.mixer.music.load("sacrifices-the-rook.mp3")
    pygame.mixer.music.play()

#----------------------------Main Program----------------------------------------
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

#create the main window
app = ctk.CTk()
app.title("ROOOOOK Sac Counter")
app.geometry("1920x1080")

#create a frame to hold two sub-frames (that will hold all the content - all the widgets: text, buttons, etc.)
frame = ctk.CTkFrame(app)
frame.pack(expand = True)

#create two sub-frames
inpFrame = ctk.CTkFrame(frame)
inpFrame.grid(row = 0, column = 0, padx = 5, pady = 10)

outFrame = ctk.CTkFrame(frame)
outFrame.grid(row = 0, column = 1, padx = 5, pady = 10)

#display the rook sound button
rookBtn = ctk.CTkButton(inpFrame, 
                        text = "♜", 
                        font = ("Comic Sans Ms", 40, "bold"), 
                        width = 100, 
                        height = 100, 
                        fg_color="#2771de",
                        hover_color="#80acee",
                        corner_radius = 50,
                        border_width= 3,
                        border_color = "#6fb5ff",

                        command = lambda: rookSound())
rookBtn.grid(row = 0, column = 0, padx = 5, pady = 10, columnspan = 2)

#display a title - 'Sacrifice the rook'
titleLbl = ctk.CTkLabel(inpFrame, text = "Sacrifice The ROOOOOOOOOK!",  font = ("Comic Sans Ms", 20, "bold"), text_color = "#00bfff")
titleLbl.grid(row = 1, column = 0, padx = 5, pady = 10, columnspan = 2)

#display kind of an engaging question + some description abt the games included in the search for rook sacs
questionLbl = ctk.CTkLabel(inpFrame, text = "How many times have you sacrificed your rook? Find out here",  font = ("Comic Sans Ms", 16))
questionLbl.grid(row = 2, column = 0, padx = 5, pady = 10, columnspan = 2)

textLbl = ctk.CTkLabel(inpFrame, text = "Games included:",  font = ("Comic Sans Ms", 14, "bold"))
textLbl.grid(row = 3, column = 0, padx = 5, pady = 10, columnspan = 2)

descLbl = ctk.CTkLabel(
    inpFrame, 
    text = "• Standard Chess only: Rapid, Blitz, Bullet, Daily (Variants are excluded) \n• Public games only (Private games are not counted) \n• All Live & Bot games",  
    font = ("Comic Sans Ms", 14),
    justify = "left",
    anchor = "w",
    text_color = "#aadfff"
    )
descLbl.grid(row = 4, column = 0, padx = 5, pady = 10, columnspan = 2)

#add the input box (for chess.com username) & search button
userEntry = ctk.CTkEntry(inpFrame, placeholder_text = "Enter your Chess.com username...", font = ("Comic Sans Ms", 14), width = 250)
userEntry.grid(row = 5, column = 0, padx = 5, pady = 10, sticky = "w")

searchBtn = ctk.CTkButton(inpFrame, text = "Search for rook sacrifices", font = ("Comic Sans Ms", 16), command = lambda: workerThread(inpFrame, outFrame, userEntry, app))
searchBtn.grid(row = 5, column = 1, padx = 5, pady = 10, sticky = "w")

app.mainloop()