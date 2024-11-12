
import os
import threading
import subprocess
import sys
import ctypes
import time

from app_update_checker import Updater

from activity_manager import activitiesManager as AM, Activity as ACT, activitiesList as AL
from feedback_manager import sendFeedback
from weblink import homePage
from constants import *
from gui_maker import Notebook, Label, countBox, optionMenu, Area, topWindow, Window, Input, tickBox, Button


# This is an individual object unique to the app

# Functionality classes


# The main message


class bigDisplayMsg(Label):
    """The main message"""

    def __init__(self, parent=None, **kw):
        self.parent = parent
        self.size = 40
        super().__init__(self.parent, **kw)
        self['font'] = ('sans-serif', self.size)
        self['text'] = f"""What are you working on? :)"""
        self['fg'] = 'green'
        self.show()

# What you click when you want to pause


class breakBtn(Button):
    """What you click when you want to pause"""

    def __init__(self, parent, **options):
        super().__init__(parent, **options)
        self['text'] = 'Take a break'
        self.show()

    def take_break(self):
        """pause the timer
        and change the text"""

# What you click to finish your task


class finishBtn(Button):
    """What you click to finish your task"""

    def __init__(self, parent):
        super().__init__(parent)
        self['text'] = 'Finish'
        self.show()


# Notebook section 1


class timerSection(Area):
    """The Timer section for seeing the personalized timer"""

    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.show()

    def show(self):
        """Show the Big display message and the buttons
        at the bottom"""

        self.big_msg_area = Area(self)
        self.big_msg_area.pack(expand=1, fill='x')

        self.big_msg = bigDisplayMsg(self.big_msg_area)

        # sub area for buttons to stay
        self.actions_area = Area(self)
        self.actions_area.pack(expand=1)

        self.break_btn = breakBtn(self.actions_area)

        self.finish_btn = finishBtn(self.actions_area)

        self.pack(expand=1)
        
    def take_break(self):
        pass


# Notebook section 2

# as a rule, in this script, every class will
# automatically show itself


class activityBtn():
    """The button which is a todo: a component"""

    def __init__(self, parent, text, switch, **options):
        """Consists of a checkbox and
          a button and a focus button

          'switch' means whether the activity has
          been done or not. 
        """
        # where this component will stay
        self.parent = parent
        self.options = options
        self.text = text
        self.switch = switch

        self.options.setdefault('bg', '#ddd')
        self.options.setdefault('pady', 5)

        self.updownpadding = self.options['pady']
        self.bg = self.options['bg']

        # the button has more than 1 function
        # the ticking makes the work finished
        # while the text bt makes the options
        # available
        self.command = None

        self.act_area_main = Area(self.parent, bg=self.bg)
        self.act_area_main.pack(expand=1, fill='x',
                                pady=self.updownpadding)

        self.Variable = tk.BooleanVar(self.act_area_main)
        self.Variable.set(switch)

        self.showMain()

    def tickPart(self):
        """The part where you manually tick"""
        self.chkBtn_part = tickBox(self.act_area_main,
                                   variable=self.Variable,
                                   bg=self.bg)

        if self.Variable.get():
            self.chkBtn_part.select()
        elif not self.Variable.get():
            self.chkBtn_part.deselect()

        self.chkBtn_part.pack(side='left')

    def textPart(self):
        """The part where you can select the activity to
        edit, delete and more"""
        self.btn_part = Button(self.act_area_main,
                               text=self.text,
                               bg=self.bg)
        # change this instance's relief
        self.btn_part['relief'] = 'flat'
        self.btn_part['width'] = 40
        self.btn_part.pack(side='left')

    def actionPart(self):
        """The part where we focus or other options"""
        self.actionBt = Button(self.act_area_main, text='Focus')
        self.actionBt.pack(side='left')

    def showMain(self):
        """Show the component itself."""
        self.tickPart()
        self.textPart()
        self.actionPart()


class activitySection(Area):
    """The section where you'll see your activities (todo list)"""

    def __init__(self, parent, **kw):
        self.parent = parent

        super().__init__(self.parent, **kw)

        self.optionsArea()
        self.activitiesList()

        self.pack()

    def optionsArea(self, color='#ddd'):
        """The items where you can operate on activities"""
        self.options_area = Area(self, bg=color)
        self.options_area.pack(side='top', fill='x')

        self.add_bt = Button(self.options_area, text='Add',
                             width=10, height=2)
        self.add_bt.pack(side='left')

        self.add_bt['command'] = lambda: activityEditor(self)

        self.add_bt = Button(
            self.options_area, text='Delete', width=10, height=2)
        self.add_bt.pack(side='left')

        self.add_bt = Button(
            self.options_area, text='Edit', width=10, height=2)
        self.add_bt.pack(side='left')

    def activitiesList(self):
        """Display the activities"""
        # the scrollable area where all activity btns stay
        self.activities_area = Area(self)
        self.activities_area.pack(side='top')

        self.bts = activityBtn(self.activities_area,
                               'This is an activity', True)

    # functionality------------------------------------------


class Note(Notebook):
    """This is where sections all come together"""

    def __init__(self, parent):
        super().__init__(parent)
        self.show()

    def show(self):
        self.timer_section = timerSection(self)
        self.act_section = activitySection(self)

        self.add(self.timer_section, text='Timer')
        self.add(self.act_section, text='Activities')

        self.pack(fill='both', expand=1)

# Help text


class helpLabel(Label):
    """A label for describing what something does"""

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['fg'] = '#595959'
        self['font'] = ('sans-serif', 10)
        self['justify'] = 'left'

# Activity editor


class activityEditor(topWindow):
    def __init__(self, parent):
        """The place where you can manage your activities"""
        self.parent = parent
        super().__init__(self.parent)

        self.wm_transient(self.parent)
        self.grab_set()

        self.elements()

    def titlePart(self):
        title_part = Area(self.all_frame)
        title_part.pack(expand=1, fill='x')
        self.title_area = tk.LabelFrame(title_part,
                                        text='Title',
                                        font=('sans-serif', 13),
                                        )
        self.title_area.pack(side='left')

        innerframe = Area(self.title_area)
        innerframe.pack(fill='x', expand=1, padx=10)

        # just so i can have that left align
        helpbox = Area(innerframe)
        helpbox.pack(expand=1, fill='x')
        self.title_help = helpLabel(helpbox,
                                    text='what are you going to do?',
                                    )
        self.title_help.pack(side='left')  # left align

        titleinputbox = Area(innerframe)
        titleinputbox.pack(expand=1, fill='x')
        self.title_entry = Input(titleinputbox,
                                 font=('sans-serif', 13),
                                 width=30)
        self.title_entry.pack(side='left')

    def durationPart(self):
        duration_part = Area(self.all_frame)
        duration_part.pack(pady=20, expand=1, fill='x')
        self.dur_area = tk.LabelFrame(duration_part,
                                      text='Duration',
                                      font=('sans-serif', 13),
                                      )
        self.dur_area.pack(side='left')

        innerframe = Area(self.dur_area)
        innerframe.pack(expand=1, fill='both', padx=10)

        # duration
        durinner1 = Area(innerframe)
        durinner1.pack(fill='x', pady=20)

        # no limit
        durinner2 = Area(innerframe)
        durinner2.pack(fill='x')

        helpbox1 = Area(durinner1)
        helpbox1.pack(expand=1, fill='x')

        self.dur_help = helpLabel(helpbox1,
                                  text='how long are you going to take?',
                                  )
        self.dur_help.pack(side='left')

        entries_area = Area(durinner1)
        entries_area.pack()

        self.dur_entry = countBox(entries_area,
                                  font=('sans-serif', 13),
                                  )
        self.dur_entry.pack(side='left')

        self.durtype = tk.Variable(self)
        self.durtypes = ['minutes', 'seconds', 'hours']

        self.durtype_entry = optionMenu(entries_area,
                                        self.durtype, self.durtypes[0],
                                        *self.durtypes)
        self.durtype_entry.pack(side='left')

        # no time limit
        helpbox2 = Area(durinner2)
        helpbox2.pack(expand=1, fill='x')
        self.no_limit_help = helpLabel(helpbox2,
                                       text=f"""\
If you don’t know how long it will take,
you can tick this box below""")
        self.no_limit_help.pack(side='left')

        tickboxbox = Area(durinner2)
        tickboxbox.pack(expand=1, fill='x', pady=5)
        self.no_limitVar = tk.BooleanVar()

        self.no_limit = tickBox(
            tickboxbox, text='No Time Limit', variable=self.no_limitVar)
        self.no_limit.pack(side='left')

    def actionsPart(self):
        """Part where buttons can stay"""
        actions_part = Area(self.all_frame)
        actions_part.pack(expand=1, fill='x')

        # save button
        self.saveBtn = Button(actions_part,
                              text='Save Activity',
                              command=self.save)
        self.saveBtn.pack()

    def elements(self):
        self.all_frame = Area(self)
        self.all_frame.pack(expand=1, fill='both')
        self.titlePart()
        self.durationPart()
        self.actionsPart()

    # Functionality

    def save(self):
        """get all inputed info and close this topwindow"""

        # close
        self.destroy()


class App(Window):
    def __init__(self):
        super().__init__()
        self.menu()
        self.notebook = Note(self)
        self.mainloop()

    def menu(self):
        self.menubar = tk.Menu(self, tearoff=False)

        modes = tk.Menu(self, tearoff=False)
        modes.add_command(
            label='OTAT (One Thing At a Time) mode', state='disabled')

        helpmenu = tk.Menu(self, tearoff=False)
        helpmenu.add_command(label="BMT Home Page",)
        helpmenu.add_command(label="Give Feedback",)
        helpmenu.add_separator()
        helpmenu.add_command(label="Check for Updates")

        self.menubar.add_cascade(menu=modes, label='Productivity Modes')
        self.menubar.add_cascade(menu=helpmenu, label='Help')

        self.configure(menu=self.menubar)


App()
