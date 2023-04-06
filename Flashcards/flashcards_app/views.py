import tkinter as tk
from tkinter import ttk
from . import widgets as w


class CreateView(tk.Frame):
    def __init__(self, parent, num_entries: tk.IntVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.num_entries = num_entries
        self.term_vars = []
        self.def_vars = []

        self.add_button_frame = ttk.Frame(self)
        self.add_button = ttk.Button(self.add_button_frame, text='Add Card', command=self._add_entry)
        self.add_button.grid()
        self.add_button_frame.grid(row=99, column=0, pady=(15, 5))

        self.columnconfigure(0, weight=1)

    def _add_entry(self):
        entry_frame = ttk.Frame(self)
        ttk.Label(entry_frame, text=f"Card {self.num_entries.get() + 1}").grid(row=0, column=0, sticky='ew')
        self.term_vars.append(tk.StringVar())
        self.def_vars.append(tk.StringVar())
        w.CardInput(
            entry_frame, term_variable=self.term_vars[self.num_entries.get()],
            def_variable=self.def_vars[self.num_entries.get()]
        ).grid(row=0, column=1)
        self.event_generate('<<CardEntryAdded>>')
        entry_frame.grid(
            row=self.num_entries.get(), column=0, sticky=(tk.W + tk.E),
            pady=(15, 0), padx=10
        )
        for i in range(3):
            entry_frame.columnconfigure(i, weight=1)
