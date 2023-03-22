import tkinter as tk
from tkinter import ttk


class HomeDirectory(ttk.Frame):
    """The home page from which you can do the stuffs"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padding=(100, 25))

        ttk.Label(self, text='Flashcards!', font=('TkDefaultFont', 48, 'bold')).grid(row=0, sticky='ew')

        options_frame = ttk.Frame(self)
        option_labels = ('Create', 'Load', 'About')
        for option in option_labels:
            tk.Button(
                options_frame, text=option,
                command=lambda *_: self.event_generate(f'<<Get{option}Page>>'),
                bg='#88bbcc', font=('TkDefaultFont', 24, 'bold'), width=10
            ).pack(ipady=5, pady=10)
        options_frame.grid(row=1, sticky='nsew', pady=20)


class CreateSetView(ttk.Frame):
    pass
