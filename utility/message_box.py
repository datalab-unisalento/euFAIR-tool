import tkinter as tk
from tkinter import messagebox


def box(title, text, _icon='warning'):
    msg_box = tk.messagebox.askquestion(title, text, icon=_icon)

    if msg_box == 'yes':
        ans = 1
    else:
        ans = 0

    return ans
