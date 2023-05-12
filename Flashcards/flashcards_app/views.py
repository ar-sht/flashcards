import tkinter as tk
from tkinter import ttk
from . import widgets as w
from tkinter.simpledialog import Dialog


class ChoiceDialog(Dialog):
    def __init__(self, parent, title):
        self.choice = tk.StringVar()
        super().__init__(parent, title=title)

    def body(self, frame):
        ttk.Label(frame, text='Load existing set or create new one?').grid(row=0)
        choice_frame = ttk.Frame(
            frame
        )
        w.RadioGroup(
            choice_frame, variable=self.choice, values=['Load', 'Create']
        ).grid(row=0)
        choice_frame.grid(row=1, pady=10)

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(
            box, text='Cancel', command=self.cancel
        ).grid(padx=5, pady=5)

        ttk.Button(
            box, text='Ok', command=self.ok, default=tk.ACTIVE
        ).grid(row=0, column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


class CreateView(ttk.Frame):
    def __init__(
            self, parent, term_vars: list[tk.StringVar], def_vars: list[tk.StringVar],
            name_var: tk.StringVar, num_entries: tk.IntVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.term_vars = term_vars
        self.def_vars = def_vars
        self.name_var = name_var
        self.num_entries = num_entries

        self.name_inp_frame = ttk.Frame(self)
        w.LabelInput(
            self.name_inp_frame, var=self.name_var, label="Name", input_class=ttk.Entry
        ).grid(row=0, column=0)
        self.name_inp_frame.grid(row=0, column=0, pady=15)

        self.add_button = ttk.Button(self, text='Add Card', command=self._add_entry)
        self.add_button.grid(row=99, pady=(15, 0))

        self.buttons_frame = ttk.Frame(self)

        ttk.Frame(self.buttons_frame).pack(side=tk.LEFT, expand=True, fill='x')

        self.save_button = ttk.Button(self.buttons_frame, text='Save', command=self._on_save)
        self.save_button.pack(side=tk.RIGHT, padx=15)

        self.clear_button = ttk.Button(self.buttons_frame, text='Clear', command=self._reset)
        self.clear_button.pack(side=tk.RIGHT)

        self.buttons_frame.grid(row=100, sticky='ew', padx=30, pady=(15, 0))

        self.columnconfigure(0, weight=1)

    def _add_entry(self):
        self.event_generate('<<CardEntryAdd>>')

        if self.num_entries.get() >= 98:
            return

        entry_frame = ttk.Frame(self)

        ttk.Frame(entry_frame).grid(row=0, column=1)
        ttk.Frame(entry_frame).grid(row=0, column=3)
        ttk.Frame(entry_frame).grid(row=0, column=5)

        ttk.Label(entry_frame, text=f"Card {self.num_entries.get()}").grid(row=0, column=0, sticky='ew')

        w.LabelInput(
            entry_frame, var=self.term_vars[self.num_entries.get() - 1],
            label='Term', input_class=ttk.Entry
        ).grid(row=0, column=2)
        w.LabelInput(
            entry_frame, var=self.def_vars[self.num_entries.get() - 1],
            label='Definition', input_class=ttk.Entry
        ).grid(row=0, column=4)

        temp_button = w.InputRemoveButton(
            entry_frame, id=self.num_entries.get()
        )
        temp_button.configure(command=lambda: self._remove_entry(temp_button))
        temp_button.grid(row=0, column=6)

        entry_frame.columnconfigure(1, minsize=20)
        entry_frame.columnconfigure(3, minsize=20)
        entry_frame.columnconfigure(5, minsize=20)

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
            row_num = int(child.grid_info()["row"])
            if row_num == entry.id:  # remove the row corresponding to button
                child.grid_remove()
            if row_num > entry.id:  # bring all other rows down one
                child.grid_configure(row=row_num - 1)
                for grandchild in child.grid_slaves():
                    if isinstance(grandchild, ttk.Label):
                        grandchild.configure(text=f'Card {row_num - 1}')

        try:
            self.master.remove_entry(entry.id)
        except ValueError:
            raise Exception('Master is missing function remove_entry')

    def _on_save(self):
        self.event_generate('<<SaveCardSet>>')

    def _reset(self):
        self.event_generate('<<CardEntriesReset>>')

    def deploy(self, num):
        for i in range(num):
            self._add_entry()


class ReviewView(ttk.Frame):
    def __init__(
            self, parent, term_vars: list[tk.StringVar], def_vars: list[tk.StringVar],
            name_var: tk.StringVar, *args, **kwargs
    ):
        super().__init__(parent,  *args, **kwargs)
        self.name_var = name_var
        self._cur_card_index = 0
        self._var_type = 'term'
        self.all_vars = {'term': term_vars, 'definition': def_vars}

        ttk.Label(
            self, textvariable=self.name_var, font=('TkDefaultFont', 36)
        ).grid(row=0, column=0, sticky='ew', pady=(0, 15), padx=(200, 0))

        self.content_frame = ttk.Frame(self)

        ttk.Button(self.content_frame, text='Prev', command=self._on_prev).grid(row=1, column=0)

        self.cur_card = w.Flashcard(
            self.content_frame, variable=self.all_vars[self._var_type][self._cur_card_index],
            label_args={'font': ('TkDefaultFont', 24)}
        )
        self.cur_card.grid(row=0, column=1, rowspan=3)

        ttk.Button(self.content_frame, text='Flip', command=self._on_flip).grid(row=4, column=1)

        ttk.Button(self.content_frame, text='Next', command=self._on_next).grid(row=1, column=2, pady=(10, 0))

        self.content_frame.columnconfigure(1, weight=1, minsize=200)
        self.content_frame.grid(row=1, column=0, sticky='ew', padx=200)

        self.columnconfigure(0, weight=1)

    def _on_prev(self, *_):
        if self._cur_card_index > 0:
            self._cur_card_index -= 1
        self._regen_card()

    def _on_next(self, *_):
        if self._cur_card_index < len(self.all_vars[self._var_type]) - 1:
            self._cur_card_index += 1
        self._regen_card()

    def _on_flip(self, *_):
        self._var_type = 'term' if self._var_type == 'definition' else 'definition'
        self._regen_card()

    def _regen_card(self):
        self.cur_card.destroy()
        self.cur_card = w.Flashcard(
            self.content_frame, variable=self.all_vars[self._var_type][self._cur_card_index],
            label_args={'font': ('TkDefaultFont', 24)}
        )
        self.cur_card.grid(row=0, column=1, rowspan=3)


class QuizView(ttk.Frame):
    def __init__(
            self, parent, term_vars: list[tk.StringVar], def_vars: list[tk.StringVar],
            warnings: list[tk.StringVar], *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.term_vars = term_vars
        self.def_vars = def_vars
        self.answers = [tk.StringVar(value='') for _ in def_vars]
        self.warnings = warnings

        ttk.Label(
            self, text='Quiz Thyself', font=('TkDefaultFont', 24)
        ).grid(row=0, column=0, sticky='ew', pady=(0, 15))

        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=1, sticky='ew')
        self.refresh()
        ttk.Button(
            self, text="Check", command=self._trigger_check
        ).grid(row=3, pady=10)

    def _render_question(self, i):
        w.QuizQuestion(
            self.content_frame, self.term_vars[i].get(),
            self.answers[i], self.warnings[i].get()
        ).pack(expand=True, fill='both')

    def refresh(self):
        for child in self.content_frame.winfo_children():
            child.destroy()
        for i in range(len(self.term_vars)):
            self._render_question(i)

    def _trigger_check(self, *_):
        self.event_generate('<<AnswersSubmitted>>')
