import tkinter as tk
from tkinter import ttk
from . import widgets as w


class CreateView(ttk.Frame):
    def __init__(self, parent, num_entries: tk.IntVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.num_entries = num_entries
        self.term_vars = []
        self.def_vars = []
        self.buttons = []

        self.add_button = ttk.Button(self, text='Add Card', command=self._add_entry)
        self.add_button.grid(row=99, pady=(15, 0))

        self.columnconfigure(0, weight=1)

    def _add_entry(self):
        entry_frame = ttk.Frame(self)
        ttk.Frame(entry_frame).grid(row=0, column=1)
        ttk.Frame(entry_frame).grid(row=0, column=3)
        ttk.Frame(entry_frame).grid(row=0, column=5)
        ttk.Label(entry_frame, text=f"Card {self.num_entries.get() + 1}").grid(row=0, column=0, sticky='ew')
        if len(self.term_vars) < self.num_entries.get() + 1:
            self.term_vars.append(tk.StringVar())
        if len(self.def_vars) < self.num_entries.get() + 1:
            self.def_vars.append(tk.StringVar())
        w.LabelInput(
            entry_frame, var=self.term_vars[self.num_entries.get()],
            label='Term', input_class=ttk.Entry
        ).grid(row=0, column=2)
        w.LabelInput(
            entry_frame, var=self.def_vars[self.num_entries.get()],
            label='Definition', input_class=ttk.Entry
        ).grid(row=0, column=4)
        temp_button = w.InputRemoveButton(
            entry_frame, id=self.num_entries.get()
        )
        temp_button.configure(command=lambda: self._remove_entry(temp_button))
        self.buttons.append(temp_button)
        temp_button.grid(row=0, column=6)
        entry_frame.columnconfigure(1, minsize=20)
        entry_frame.columnconfigure(3, minsize=20)
        entry_frame.columnconfigure(5, minsize=20)
        self.event_generate('<<CardEntryAdded>>')
        entry_frame.grid(
            row=self.num_entries.get(), column=0, sticky=(tk.W + tk.E),
            pady=(15, 0), padx=10
        )
        for i in range(7):
            if i == 3:
                entry_frame.columnconfigure(i, weight=1)
            else:
                entry_frame.columnconfigure(i, weight=3)

    def _remove_entry(self, entry: w.InputRemoveButton):
        for child in self.grid_slaves():
            if entry.id < int(child.grid_info()['row']) < 99:
                child.grid_remove()
        proper_num = self.num_entries.get() - 1
        self.term_vars.pop(entry.id)
        self.def_vars.pop(entry.id)
        self.event_generate('<<CardEntryRemoved>>')
        self.num_entries.set(entry.id)
        for i in range(entry.id, proper_num):
            self._add_entry()

    def deploy(self):
        self._add_entry()
        self._add_entry()
