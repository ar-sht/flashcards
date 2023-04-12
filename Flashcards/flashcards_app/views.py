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
            self, parent, term_vars: [tk.StringVar], def_vars: [tk.StringVar],
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

        self.load_button = ttk.Button(self.buttons_frame, text='Load', command=self._on_load)
        self.load_button.pack(side=tk.LEFT)

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

    def _on_load(self):
        self.event_generate('<<LoadCardSet>>')

    def _reset(self):
        self.event_generate('<<CardEntriesReset>>')

    def deploy(self, num):
        for i in range(num):
            self._add_entry()
