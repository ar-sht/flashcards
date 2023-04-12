import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from . import models as m
from . import views as v
from tkinter import filedialog


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_var = tk.StringVar()
        self.term_vars = []
        self.def_vars = []
        self.starting_num = 2

        self.withdraw()
        self.dialog = v.ChoiceDialog(self, 'Load or Create?')
        if self.dialog.choice.get() == 'Load':
            self._on_load_chosen()
        elif self.dialog.choice.get() == 'Create':
            self._on_create_chosen()
        else:
            self.destroy()
        self.deiconify()

        self.model = m.CSVModel()

        self.wm_geometry('1000x600')

        self.title("Flashcards!")
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.grid(row=1, padx=10, sticky='nsew')

        self.num_entries = tk.IntVar(value=0)
        self.creation = v.CreateView(
            self, term_vars=self.term_vars, def_vars=self.def_vars,
            name_var=self.name_var, num_entries=self.num_entries
        )
        self.creation.bind('<<CardEntryAdd>>', self._on_add_entry)
        self.creation.bind('<<CardEntriesReset>>', self._reset_vars)
        self.creation.bind('<<SaveCardSet>>', self._on_save)
        self.creation.bind('<<LoadCardSet>>', self._on_load_chosen)
        self.creation.deploy(self.starting_num)
        self.notebook.add(self.creation, text='Create')

    def _on_add_entry(self, *_):
        self.num_entries.set(self.num_entries.get() + 1)
        print(self.num_entries.get())
        if len(self.term_vars) < self.num_entries.get():
            self.term_vars.append(tk.StringVar())
            self.def_vars.append(tk.StringVar())

    def _reset_vars(self, *_):
        for term_var in self.term_vars:
            term_var.set(value="")
        for def_var in self.def_vars:
            def_var.set(value="")

    def _on_save(self, *_):
        if self.name_var.get() == "":
            messagebox.showerror(
                title='Error',
                message='Cannot save Set',
                detail='Please provide a title for your Flashcard Set.'
            )
            return
        data = {
            'Terms': [term_var.get() for term_var in self.term_vars],
            'Definitions': [def_var.get() for def_var in self.def_vars]
        }
        self.model.filename = self.name_var.get() + '.csv'
        self.model.save_set(data)
        self._reset_vars()
        self.name_var.set(value="")

    def _on_create_chosen(self, *_):
        self.term_vars = []
        self.def_vars = []

    def _on_load_chosen(self, *_):
        filename = filedialog.askopenfilename(
            title='Select a set to load',
            filetypes=[('CSV', '*.csv *.CSV')],
        )

        if filename:
            self.model = m.CSVModel(filename=filename)
            data = self.model.load_set()
            for term, definition in data:
                print(term, definition)
                self.term_vars.append(tk.StringVar(value=term))
                self.def_vars.append(tk.StringVar(value=definition))
            self.starting_num += len(self.term_vars) - 2

    def remove_entry(self, row_num):
        self.num_entries.set(self.num_entries.get() - 1)
        self.term_vars.pop(row_num - 1)
        self.def_vars.pop(row_num - 1)
