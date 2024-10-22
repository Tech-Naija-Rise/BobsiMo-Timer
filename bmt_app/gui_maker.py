import tkinter as tk
from tkinter.commondialog import Dialog
from constants import *


#DEV only
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

    def __center_window(self, any_window):
        """Center the window on screen"""
        any_window.update()

        self.win_width = 900
        self.win_height = 500

        self.screen_width = any_window.winfo_screenwidth()
        self.screen_height = any_window.winfo_screenheight()

        self.win_x = (self.screen_width//2) - (self.win_width//2)
        self.win_y = (self.screen_height//2) - (self.win_height//2)

        any_window.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")

class Window(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className="Tk", useTk=True, sync=False, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.wm_iconbitmap(app_icon)
        self.tk_setPalette('#aaa')

    def __center_window(self, any_window):
        """Center the window on screen"""
        any_window.update()

        self.win_width = 900
        self.win_height = 500

        self.screen_width = any_window.winfo_screenwidth()
        self.screen_height = any_window.winfo_screenheight()

        self.win_x = (self.screen_width//2) - (self.win_width//2)
        self.win_y = (self.screen_height//2) - (self.win_height//2)

        any_window.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")


class Messages(Dialog):
    def __init__(self, master=None, **options):
        super().__init__(master, **options)


class topWindow(tk.Toplevel):
    """A window that is going to stay 
    always on top. e.g. for dialogs..."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.wm_iconbitmap(app_icon)
        self.wm_transient(self.master)
        self.grab_set()

    def __center_window(self, any_window):
        """Center the window on screen"""
        any_window.update()

        self.win_width = 900
        self.win_height = 500

        self.screen_width = any_window.winfo_screenwidth()
        self.screen_height = any_window.winfo_screenheight()

        self.win_x = (self.screen_width//2) - (self.win_width//2)
        self.win_y = (self.screen_height//2) - (self.win_height//2)

        any_window.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")


class Button(tk.Button):
    pass


class Frame(tk.Frame):
    pass


class Input(tk.Entry):
    pass
