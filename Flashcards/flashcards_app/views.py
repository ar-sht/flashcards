import tkinter as tk
from tkinter import ttk
from . import widgets as w
from tkinter.simpledialog import Dialog


class CreateView(ttk.Frame):
    def __init__(self, parent, name_var: tk.StringVar, num_entries: tk.IntVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.name_var = name_var
        self.num_entries = num_entries
        self.term_vars = []
        self.def_vars = []

        self.name_inp_frame = ttk.Frame(self)
        w.LabelInput(
            self.name_inp_frame, var=self.name_var, label="Name", input_class=ttk.Entry
        ).grid(row=0, column=0)
        self.name_inp_frame.grid(row=0, column=0, pady=15)

        self.add_button = ttk.Button(self, text='Add Card', command=self._add_entry)
        self.add_button.grid(row=99, pady=(15, 0))

        self.buttons_frame = ttk.Frame(self)
        self.clear_button = ttk.Button(self.buttons_frame, text='Clear', command=self.reset)
        self.clear_button.grid(row=0, column=0)
        ttk.Frame(self.buttons_frame).grid(row=0, column=1)
        self.save_button = ttk.Button(self.buttons_frame, text='Save', command=self._on_save)
        self.save_button.grid(row=0, column=2)
        self.buttons_frame.grid(row=100, sticky='e', padx=30, pady=(15, 0))
        self.buttons_frame.columnconfigure(1, minsize=10)
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)

    def _add_entry(self):
        if self.num_entries.get() >= 97:
            return
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
            entry_frame, id=self.num_entries.get() + 1
        )
        temp_button.configure(command=lambda: self._remove_entry(temp_button))
        temp_button.grid(row=0, column=6)
        entry_frame.columnconfigure(1, minsize=20)
        entry_frame.columnconfigure(3, minsize=20)
        entry_frame.columnconfigure(5, minsize=20)
        self.event_generate('<<CardEntryAdded>>')
        entry_frame.grid(
            row=self.num_entries.get() + 1, column=0, sticky=(tk.W + tk.E),
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
        self.term_vars.pop(entry.id - 1)
        self.def_vars.pop(entry.id - 1)
        self.event_generate('<<CardEntryRemoved>>')
        self.num_entries.set(entry.id - 1)
        for i in range(entry.id - 1, proper_num):
            self._add_entry()

    def _on_save(self):
        self.event_generate('<<SaveCardSet>>')

    def deploy(self):
        self._add_entry()
        self._add_entry()

    def reset(self):
        for term_var in self.term_vars:
            term_var.set(value="")
        for def_var in self.def_vars:
            def_var.set(value="")
        self.event_generate('<<CardEntriesReset>>')
