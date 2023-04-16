import pandas as pd
import tkinter as tk
import random
import json
import requests
import os
BACKGROUND_COLOR = "#B1DDC6"

url = 'https://farasa.qcri.org/webapi/diacritize/'
api_key = os.environ['farasa_api_key']
# qMLJCUPWzzlGNCtKFF


try:
    data = pd.read_csv('data/known_words.csv')
except :
    e = pd.read_csv('data/Arabic_words.csv')
    e.to_csv('data/known_words.csv')
    data = pd.read_csv('data/known_words.csv')
word_list = data.to_dict(orient='records')
ran = random.choice(word_list)
text = ran['Arabic']
payload = {'text': text, 'api_key': api_key}
data = requests.post(url, data=payload)
result = json.loads(data.text)

# Random word from csv file

def random_word():
    global ran
    try:
        ran = random.choice(word_list)
    except:
        e = pd.read_csv('data/Arabic_words.csv')
        e.to_csv('data/known_words.csv')
    finally:
        card.itemconfig(title, text='Arabic')
        text = ran['Arabic']
        card.itemconfig(new_word, text=result['text'])
        card.itemconfig(flip, image=front_card_img)
        window.after(3000, flip_card)


def flip_card():
    card.itemconfig(title, text='English')
    card.itemconfig(new_word, text=ran['English'])
    card.itemconfig(flip, image=back_card_img)

def known_words():
    word_list.remove(ran)
    print(len(word_list))
    new_data = pd.DataFrame(word_list)
    new_data.to_csv('data/known_words.csv')
    random_word()

# Window
window = tk.Tk()
window.title('Flash Cards')
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.after(3000, flip_card)

# Images
front_card_img = tk.PhotoImage(file='images/card_front.png')
back_card_img = tk.PhotoImage(file='images/card_back.png')
right_button_img = tk.PhotoImage(file='images/right.png')
wrong_button_img = tk.PhotoImage(file='images/wrong.png')

# Canvas
card = tk.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flip = card.create_image(400, 263, image=front_card_img)
title = card.create_text(400, 100, text='Arabic', font=('Ariel', 40, 'italic'))
new_word = card.create_text(400, 255, text=result['text'], font=('Ariel', 60, 'bold'))

card.grid(row=0, column=0, columnspan=2)

# Button
right_button = tk.Button(image=right_button_img, command=known_words, highlightthickness=0)
wrong_button = tk.Button(image=wrong_button_img, command=random_word, highlightthickness=0)

right_button.grid(row=1, column=0)
wrong_button.grid(row=1, column=1)

window.mainloop()
