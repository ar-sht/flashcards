import tkinter as tk
from tkinter import ttk


class BoundText(tk.Text):
    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)
            self.bind('<<Modified>>', self._set_var)

    def _set_content(self):
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())

    def _set_var(self):
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)


class InputRemoveButton(ttk.Button):
    def __init__(self, parent, *args, id, **kwargs):
        super().__init__(parent, *args, text='Remove', width=6, **kwargs)
        self.id = id


class Flashcard(ttk.Frame):
    def __init__(
            self, parent, variable,
            label_args=None, *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.variable = variable or tk.StringVar()
        self.label_args = label_args or dict()
        self.label = ttk.Label(self, textvariable=self.variable, **self.label_args)
        self.label.pack(expand=True, fill='both', ipady=5, ipadx=5)


class QuizQuestion(ttk.Frame):
    def __init__(
            self, parent, question, variable, status, **kwargs
    ):
        super().__init__(parent, **kwargs)
        self.variable = variable or tk.StringVar()
        self.status = status
        self.question = ttk.Label(self, text=question)
        self.answer = ttk.Entry(self, textvariable=self.variable)
        self.question.pack(expand=True, fill='both', pady=10, padx=20)
        self.answer.pack(expand=True, fill='both', pady=5, padx=40)
        ttk.Label(self, text=status, font=('TKDefaultFont', 8)).pack(expand=True, fill='both', pady=5)


class LabelInput(ttk.Frame):
    def __init__(
            self, parent, label, var, input_class=None,
            input_args=None, label_args=None, **kwargs
    ):
        super().__init__(parent, **kwargs)

        input_args = input_args or {}
        label_args = label_args or {}

        self.variable = var
        self.variable.label_widget = self

        if input_class in (
                ttk.Checkbutton, ttk.Button,
                ttk.Radiobutton
        ):
            input_args['variable'] = self.variable
        else:
            input_args['textvariable'] = self.variable

        self.input = input_class(self, **input_args)
        self.input.grid(row=0, column=0, sticky=(tk.W + tk.E))

        self.label = ttk.Label(self, text=label, **label_args)
        self.label.grid(row=1, column=0, sticky=(tk.W + tk.E))

        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        super().grid(sticky=sticky, **kwargs)


class RadioGroup(ttk.Frame):
    def __init__(
            self, *args, variable=None, values=None,
            button_args=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.variable = variable or tk.StringVar()
        self.values = values or list()
        self.button_args = button_args or dict()
        for v in self.values:
            button = ttk.Radiobutton(
                self, value=v, text=v,
                variable=self.variable, **self.button_args
            )
            button.pack(
                side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x'
            )
