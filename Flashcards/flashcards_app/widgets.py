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


class CardInput(tk.Frame):
    def __init__(self, *args, term_variable=None, def_variable=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.term_variable = term_variable or tk.StringVar()
        self.def_variable = def_variable or tk.StringVar()

        self.term_input = LabelInput(
            self, label='Term', var=term_variable,
            input_class=ttk.Entry
        )
        self.def_input = LabelInput(
            self, label='Definition', var=def_variable,
            input_class=ttk.Entry
        )

        self.term_input.grid(row=0, column=0, sticky='ew')
        self.def_input.grid(row=0, column=1, sticky='ew')


class LabelInput(tk.Frame):
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
