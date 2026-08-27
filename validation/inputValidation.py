#input validation - the same as one of the validation functions from my NEA (another project)
from tkinter import messagebox

def titleValidation(title):
    if len(title) == 0:
        messagebox.showwarning("Error", "No title input")

        validTitle = False
        return validTitle
    else:
        title = title.strip() #remove unnecessary whitespace

        #allow letters, numbers & symbols to be input
        allowedChrs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*_():/.,'- "
        symbols = "!@#$%^&*():/.,'-><[]{}\|"

        #check if the input is above the min length of input & not exceeding the max length
        if (len(title) >= 2) and (len(title) <=100):
            goodLength = True
        else:
            goodLength = False
        
        #check if input contains only symbols
        allSymbols = all(character in symbols for character in title)

        #input title is only valid if all input characters are allowed, length is fine & input doesn't have only symbols
        if (all(character in allowedChrs for character in title)) and (goodLength == True) and (allSymbols != True):
            validTitle = True
            return validTitle
        else:
            validTitle = False
            messagebox.showwarning("Error", "Title must be between 2 & 100 characters, contain letters, numbers, symbols & spaces only & should not contain only symbols")

            return validTitle