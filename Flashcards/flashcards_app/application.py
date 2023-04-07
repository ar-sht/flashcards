import tkinter as tk
from tkinter import ttk
from . import models as m
from . import views as v


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # get the models on in!
        self.terms = []
        self.defs = []

        self.wm_geometry('1000x600')

        self.title("Flashcards!")
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.grid(row=1, padx=10, sticky='nsew')

        self.num_entries = tk.IntVar(value=0)
        self.creation = v.CreateView(self, num_entries=self.num_entries)
        self.creation.bind('<<CardEntryAdded>>', self._on_entry_added)
        self.creation.bind('<<CardEntryRemoved>>', self._on_entry_removed)
        self.creation.deploy()
        self.notebook.add(self.creation, text='Create')

    def _on_entry_added(self, *_):
        self.num_entries.set(value=self.num_entries.get() + 1)
        self.terms = [term_var.get() for term_var in self.creation.term_vars]
        self.defs = [def_var.get() for def_var in self.creation.def_vars]
        print(self.terms)

    def _on_entry_removed(self, *_):
        self.terms = [term_var.get() for term_var in self.creation.term_vars]
        self.defs = [def_var.get() for def_var in self.creation.def_vars]
        print(self.terms)
