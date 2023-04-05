from tkinter import *
from tkinter import messagebox
from random import randint
from datetime import date, time


def updateStatus():
    show_score["text"] = f"Your Score: {score}"
    show_top_score["text"] = f"Top Score: {topScore}"
    attempts_left["text"] = f"Attempts left: {user_att}"
    #coincidences["text"] = f"Matches found:" 

def saveTScore():
    global topScore
    try:
        with open("top.dat", "w+") as file:
            file.write(str(topScore))
            file.write("\n")
    except:
        messagebox.showinfo("The Error occurred while saving the TopScore!")

def getTScore():
    try:
        with open("top.dat", "r") as file:
            topScore = int(file.readline())
    except:
        topScore = 0
        return topScore

def getGuessWords():
    try:
        with open("words.dat", "r+") as file:
            wordslist = [i.strip() for i in file.readlines()]
            chosen_word = wordslist[randint(0, len(wordslist) - 1)]
    except:
        messagebox.showinfo("The program has to stop!", f"The Error occurred while reading the file.")
        quit(0)
    return chosen_word

def startGame():
    global word_hidden, word_to_guess
    coincidences["text"] = f"Matches found: 0" 
    word_to_guess = chosen_word
    word_hidden = "*" * len(word_to_guess)
    word["text"] = word_hidden
    word.place(x = WIDTH // 2 - word.winfo_reqwidth() // 2, y = 50)
    updateStatus()

def startNewGame():
    global word_hidden, word_to_guess
    coincidences["text"] = f"Matches found: 0"
    chosen_word = getGuessWords()
    word_to_guess = chosen_word
    word_hidden = "*" * len(word_to_guess)
    word["text"] = word_hidden
    word.place(x = WIDTH // 2 - word.winfo_reqwidth() // 2, y = 50)
    for btn in range(26):
        buttons[btn]["text"] = chr(start_btn + btn)
        buttons[btn]["state"] = "normal"
    user_att = 10
    updateStatus()

def checkWords(st, st1):
    result = 0
    for i in range(len(st)):
        if st[i] != st1[i]:
            result += 1
    coincidences["text"] = f"Matches found: {result}"
    return result

def getHidden(char):
    temp_str = ""
    for i in range(len(word_to_guess)):
        if word_to_guess[i] == char:
            temp_str += char
        else:
            temp_str += word_hidden[i]
    return temp_str

def buttonClicked(n):
    global word_hidden, score, user_att, total_count
    buttons[n]["text"] = "."
    buttons[n]["state"] = "disabled"
    temp_word_hidden = word_hidden
    word_hidden = getHidden(chr(start_btn + n))
    check_count = checkWords(word_hidden, temp_word_hidden)
    total_count += check_count
    coincidences["text"] = f"Matches found: {total_count}"
    word["text"] = word_hidden
    if check_count > 0:
        score += check_count * 5
    else:
        score -= 10
        if score < 0:
            score = 0
        user_att -= 1   
    updateStatus()
    if word_to_guess == word_hidden:
        score += score // 2
        updateStatus()
        if score > topScore:
            messagebox.showinfo("Congratulations!", f"You have got the highest Score: {topScore}! \nThe guessed word: {word_to_guess}. \nPress OK to continue the game.")
            total_count = 0
            coincidences["text"] = f"Matches found: {total_count}"
            saveTScore()
        else:
            messagebox.showinfo("Congratulations!", f"The guessed word: {word_to_guess}. \nPress OK to continue the game.")
            total_count = 0
            coincidences["text"] = f"Matches found: {total_count}"
        startNewGame()
    if user_att == 0:
        messagebox.showinfo("Game is over!", f"The number of possible attempts is over! \nPress OK to continue the game.")
        total_count = 0
        coincidences["text"] = f"Matches found: {total_count}"
        startNewGame()


main = Tk()
main.resizable(False, False)
main.title("...GUESS THE WORD...")
WIDTH = 720
HEIGHT = 480
SCR_WIDTH = main.winfo_screenwidth()
SCR_HEIGHT = main.winfo_screenheight()
POS_X = SCR_WIDTH // 2 - WIDTH // 2
POS_Y = SCR_HEIGHT // 2 - HEIGHT // 2
main.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")
img = PhotoImage(file="back.png")
label = Label(main, image=img)
label.place(x=0, y=0)
main.configure(background="lightgreen")
main.iconbitmap("myIcon.ico")
DATE = date.today().strftime("%A %d.%m.%Y")


word = Label(font="consolas 30 bold", bg="orange")

guess = Label(main, text=".::GUESS THE WORD::.", font="consolas 22 bold", bg="lightblue")
show_score = Label(font="consolas 12 bold", bg="lightgreen")
show_top_score = Label(font="consolas 12 bold", bg="lightgreen")
attempts_left = Label(font="consolas 12 bold", bg="lightgreen")
coincidences = Label(font="consolas 12 bold", bg="lightgreen")
show_date = Label(font="consolas 12 bold", text=f"Today is: {DATE}", fg="black", bd=2)
guess.place(x=210, y=10)
show_score.place(x=10, y=165)
show_top_score.place(x=10, y=190)
attempts_left.place(x=10, y=215)
coincidences.place(x=400, y=315)
show_date.place(x=10, y=400)


score = 0
topScore = 100
user_att = 10
total_count = 0


start_btn = ord("A")
buttons = []
for btn in range(26):
    buttons.append(Button(text=chr(start_btn + btn), width=2, font="montserrat 15 bold", bg="lightblue", fg="blue", activebackground="cyan", activeforeground="magenta", bd=3, relief="raised"))
    buttons[btn].place(x = 215 + (btn % 9) * 40, y = 150 + btn // 9 * 50)
    buttons[btn]["command"] = lambda x = btn: buttonClicked(x)

word_to_guess = ""
word_hidden = ""



chosen_word = getGuessWords()
startGame()

main.mainloop()
