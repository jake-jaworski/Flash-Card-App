from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


def new_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(word_dict)
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(card_background, image=card_front)
    canvas.itemconfig(check_guess, text="")
    timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)
    canvas.itemconfig(check_guess, text="Did you guess the word?")


def known_word():
    word_dict.remove(current_card)
    data = pd.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ---------DATAFRAME SETUP--------- #
try:
    raw_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    raw_data = pd.read_csv("data/french_words.csv")
    word_dict = raw_data.to_dict(orient="records")
else:
    word_dict = raw_data.to_dict(orient="records")


# ---------UI SETUP--------- #

# window setup
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(5000, func=flip_card)

# initialize images
card_back = PhotoImage(file="images/card_back.gif")
card_front = PhotoImage(file="images/card_front.gif")
right = PhotoImage(file="images/right.gif")
wrong = PhotoImage(file="images/wrong.gif")

# canvas setup
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 100, text="English", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
check_guess = canvas.create_text(400, 450, text="", font=("Arial", 24, "normal"), fill="white")


# button setup
correct_button = Button(image=right, highlightthickness=0, borderwidth=0, highlightbackground=BACKGROUND_COLOR, command=known_word)
incorrect_button = Button(image=wrong, highlightthickness=0, borderwidth=0, highlightbackground=BACKGROUND_COLOR, command=new_card)


# object positioning
canvas.grid(column=0, row=0, columnspan=2)
correct_button.grid(column=1, row=1)
incorrect_button.grid(column=0, row=1)

new_card()

window.mainloop()