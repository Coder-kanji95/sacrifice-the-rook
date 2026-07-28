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

#----------------------------Sub-programs----------------------------------------
def searchRookSacs(pInpFrame, pOutFrame, pUserEntry):
    #get the Chess.com username from the entry widget & pass it to validation
    username = pUserEntry.get().strip()
    titleValidation(username)

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

searchBtn = ctk.CTkButton(inpFrame, text = "Search for rook sacrifices", font = ("Comic Sans Ms", 16), command = lambda: searchRookSacs(inpFrame, outFrame, userEntry))
searchBtn.grid(row = 5, column = 1, padx = 5, pady = 10, sticky = "w")

app.mainloop()