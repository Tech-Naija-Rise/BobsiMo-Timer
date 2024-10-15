import tkinter as tk

class appLayoutModifier:
    def AreaMaker(self, where=None):
        fr = tk.Frame(where)
        fr.pack()
        return fr

    def ButtonMaker(self, where=None, label=None, command=None):
        bt = tk.Button(where,
                       text=label,
                       command=command,
                       font=('sans-serif', 10))
        bt.pack()
        return bt

    def RadioButtonMaker(self, where=None, label=None, variable=None, command=None):
        bt = tk.Radiobutton(where, variable=variable, text=label,
                            command=command,
                            font=('sans-serif', 10))
        bt.pack()
        return bt
    # developer methods: for developers only to customize frontend

    def WidgetTextChanger(self, widget: tk.Widget, new_text: str):
        """A special function to change the text of the GUI's various widgets"""
        widget['text'] = new_text

    def WidgetBgChanger(self, widget: tk.Widget, new_color: str):
        """A special function to change the background color
          of the GUI's various widgets"""
        widget['bg'] = new_color

    def WidgetFgChanger(self, widget: tk.Widget, new_color: str):
        """A special function to change the text color
          of the GUI's various widgets"""
        widget['fg'] = new_color
