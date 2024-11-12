import tkinter as tk
from tkinter.messagebox import *
from constants import *
import customtkinter as ctk
from tkinter.simpledialog import askfloat, askstring, askinteger

# DEV only


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
    def __init__(self):
        super().__init__()
        self.wm_title(f'{app_name_only}')
        self.wm_iconbitmap(app_icon)
        self.tk_setPalette('#eee')

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


class Notebook(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master,)


class panedWindow(tk.PanedWindow):
    def __init__(self, parent, **options):
        self.options = options
        super().__init__(parent, **self.options)


class Message():
    """Display a messagebox with a title and a message"""

    def __init__(self, type_, title, msg, parent=None):
        """Display a message with the type being one of:

        1. YESNO
        2. YESNOCANCEL
        3. QUESTION
        4. OKCANCEL
        5. ERROR
        6. INFO
        7. WARNING


        """
        if type_ == 'YESNO':
            askyesno(title, msg, parent=parent)
        elif type_ == 'YESNOCANCEL':
            askyesnocancel(title, msg, parent=parent)
        elif type_ == 'QUESTION':
            askquestion(title, msg, parent=parent)
        elif type_ == 'OKCANCEL':
            askokcancel(title, msg, parent=parent)
        elif type_ == 'ERROR':
            showerror(title, msg, parent=parent)
        elif type_ == 'INFO':
            showinfo(title, msg, parent=parent)
        elif type_ == 'WARNING':
            showwarning(title, msg, parent=parent)
        else:
            raise TypeError('no such type of message')


class Ask():
    def __init__(self, type_='', title='', question='', placeholder=None):
        """Bring up the dialog to ask the user for input
        1. STRING
        2. INTEGER
        3. FLOAT
        """
        self.answer = None
        if type_ == 'FLOAT':
            self.answer = askfloat(
                title=title, initialvalue=placeholder, prompt=question)
        elif type_ == 'STRING':
            self.answer = askstring(
                title=title, initialvalue=placeholder, prompt=question)
        elif type_ == 'INTEGER':
            self.answer = askinteger(
                title=title, initialvalue=placeholder, prompt=question)
        else:
            raise Exception('no such dialog')

    def __str__(self):
        return f'{self.answer}'


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


class Style(ttk.Style):
    def __init__(self, master):
        super().__init__(master)


class Button(tk.Button):
    def __init__(self, parent, **options):

        self.parent = parent
        self.options = options

        # default settings
        self.options.setdefault('font', ('sans-serif', 10))
        self.options.setdefault('relief', 'ridge')
        self.options.setdefault('bg', '#eee')
        # self.options.setdefault('bd',)

        super().__init__(self.parent, **self.options)

    def show(self, side='left', side_padding=5, updownpadding=0):
        self.pack(side=side, padx=side_padding, pady=updownpadding)


class tickBox(tk.Checkbutton):
    def __init__(self, parent=None, **options):
        self.parent = parent
        self.options = dict(options)
        self.options.setdefault('relief', 'flat')
        self.options.setdefault('bd')
        super().__init__(self.parent, **self.options)


class modernButton(ctk.CTkButton):
    def __init__(self, master, width=140, height=28, corner_radius=None, border_width=None, border_spacing=2, bg_color="transparent", fg_color=None, hover_color=None, border_color=None, text_color=None, text_color_disabled=None, background_corner_colors=None, round_width_to_even_numbers=True, round_height_to_even_numbers=True, text="CTkButton", font=None, textvariable=None, image=None, state="normal", hover=True, command=None, compound="left", anchor="center", **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, hover_color, border_color, text_color, text_color_disabled,
                         background_corner_colors, round_width_to_even_numbers, round_height_to_even_numbers, text, font, textvariable, image, state, hover, command, compound, anchor, **kwargs)


class Area(tk.Frame):
    def __init__(self, parent=None, **kw):
        super().__init__(master=parent, **kw)

    def show(self):
        self.pack()


class Label(tk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def show(self):
        self.pack()


class countBox(tk.Spinbox):
    def __init__(self, parent, **options):
        self.options = options
        self.options.setdefault('bg', '#fff')
        super().__init__(parent, **self.options)


class optionMenu(ttk.OptionMenu):
    def __init__(self, master, variable, default=None, *values, style="", direction="below", command=None):

        super().__init__(master, variable, default, *values,
                         style=style, direction=direction, command=command)


class Input(tk.Entry):
    def __init__(self, parent=None, **options):
        self.options = options
        self.options.setdefault('bg', '#fff')
        super().__init__(parent, **self.options)


def test():
    root = Window()
    entry = Input(root)
    entry.pack()
    entry = countBox(root)
    entry.pack()
    # entry = optionMenu(root)
    # entry.pack()
    root.mainloop()


if __name__ == '__main__':
    test()
