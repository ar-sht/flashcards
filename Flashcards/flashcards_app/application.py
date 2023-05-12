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
        self.creation.deploy(self.starting_num)
        self.notebook.add(self.creation, text='Create')

        self.review = v.ReviewView(
            self, term_vars=self.term_vars, def_vars=self.def_vars,
            name_var=self.name_var
        )
        self.notebook.add(self.review, text='Review')

        self.quiz_warnings = [tk.StringVar(value="") for _ in self.term_vars]
        self.quiz = v.QuizView(
            self, term_vars=self.term_vars, def_vars=self.def_vars, warnings=self.quiz_warnings
        )
        self.quiz.bind('<<AnswersSubmitted>>', self._on_submission)
        self.notebook.add(self.quiz, text='Quiz')

    def _on_submission(self, *_):
        for i in range(len(self.quiz.answers)):
            answer = self.quiz.answers[i].get()
            from thefuzz import fuzz
            ratio = fuzz.ratio(answer, self.def_vars[i].get())
            if answer == "":
                self.quiz_warnings[i].set(value="Unanswered")
            elif ratio >= 80:
                self.quiz_warnings[i].set(value="Correct!")
            else:
                self.quiz_warnings[i].set(value="Incorrect.")
        self.quiz.refresh()

    def _on_add_entry(self, *_):
        self.num_entries.set(self.num_entries.get() + 1)
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
            self.term_vars = []
            self.def_vars = []
            self.model = m.CSVModel(filename=filename)
            data = self.model.load_set()
            for term, definition in data:
                self.term_vars.append(tk.StringVar(value=term))
                self.def_vars.append(tk.StringVar(value=definition))
            self.starting_num += len(self.term_vars) - 2

    def remove_entry(self, row_num):
        self.num_entries.set(self.num_entries.get() - 1)
        self.term_vars.pop(row_num - 1)
        self.def_vars.pop(row_num - 1)
