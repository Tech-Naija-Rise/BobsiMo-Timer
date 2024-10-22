import tkinter as tk
import tkinter.ttk as ttk
from gui_maker import topWindow
import json
from constants import app_icon, app_name, computer
import pathlib
# For Dev only
app_icon = '.\\BMT_logo.png'


class Activity:
    def __init__(self, activity_info: dict):
        """An instance of an activity"""
        self.activity_info = activity_info
        self.activity_info.setdefault("name", "(No activity title)")

        self.name = self.activity_info['name']
        self.duration = self.activity_info['duration']
        self.duration_type = self.activity_info['dur_type']
        self.dur_type = self.duration_type

    def __dict__(self):
        return self.activity_info


class activitiesManager():
    """Every Toplevel class should have a parent from which it is
    called"""
    ACTS_PATH = pathlib.Path(
        f'{computer}\\Appdata\\Local\\BobsiMo Timer\\activities')

    def __init__(self, caller):
        """I am in charge of all things having to do with activities in this app"""
        self.caller = caller
        self.activities = self.get_activities()

        # the activity for everyone to know
        self.active = None
    # MAIN FUNCTIONALITY

    def start_timer(self, act_obj):
        """Continue to BMT window and start the Timer.

        Pass my self into the BMT so that he can modify me"""
        self.hide_act_gui()

        # this way, we have given
        # the data to the parent
        self.active = act_obj

        # Do the modification of that class
        self.act_name = self.active.name
        self.duration = self.active.duration
        self.dur_type = self.active.dur_type

        # NOTE: be sure to put a confirmation
        # but why?

        # why is it that the timer should not allow multiple
        # timers?
        # I am falling into the mistake of
        # thinking of only myself while making
        # something for people. WHY?

        # if the

        self.caller.activity = act_obj
        self.caller.start_timer(self.act_name, act_obj)

    def select_activity(self, act_obj: Activity, bt):
        """When the activity button is clicked,
        select it (TODO)and show some information about
        that activity(TODO)

        For now just enable the start timer button
        Maybe we can further"""

        self.active = act_obj
        self.gui_enable_bt(self.startBt)

        if act_obj is not None:
            if act_obj.duration is not None:
                # prettify the duration to fit
                self.msg['text'] = f"""\
You will now {act_obj.name} for {act_obj.duration} {act_obj.dur_type}"""

            # NOTE: FEATURE "no time limit ""
            # if there's no specific time frame
            else:
                self.msg['text'] = f"""\
You will now {act_obj.name}"""

        else:
            pass
        # make the start timer have the activity info with
        # which it will go to BMTimer.
        self.startBt['command'] = lambda: self.start_timer(act_obj)

    def get_activities(self):
        """Get the activities from
         the json file and present them as objects
        return the list of those activity objects"""
        activities = []

        try:
            with open(f'{self.ACTS_PATH}\\activities.json', 'r') as acts:
                actss = json.load(acts)
        except Exception as e:
            print(e)
            return activities
            # sort the info coming in the
            # appropriate order (according to the index number)
            # actss = dict(sorted(actss.items()))

            # Transform each activity dictionary
            # into an Activity object

        for act in actss:
            a = Activity(dict(act))

            activities.append(a)

        return activities

    def store_activities(self):
        """Store the activity object in the json file"""
        import os
        a = []
        for act in self.activities:
            aa = dict(act.activity_info)
            a.append(aa)

        if not self.ACTS_PATH.is_dir():
            os.makedirs(self.ACTS_PATH)

        with open(f'{self.ACTS_PATH}\\activities.json', 'w') as acts_:
            json.dump(a, acts_)

    def show_act_gui(self):
        """Either show gui as a toplevel with a parent window
        or show it as a standalone window.
        if as_top_level is True, then you must provide it's parent
        window (or class)"""

        self.act_win = topWindow(self.caller.timer_win)

        self.menubar1 = tk.Menu(self.act_win)

        self.menubar1.add_command(label='ADD', command=self.show_act_editor)
        # self.menubar1.add_command(label='EDIT', command=lambda: self.show_editor())
        self.act_win.configure(menu=self.menubar1)

        self.all_frame = tk.Frame(self.act_win)
        self.all_frame.pack()

        self.topframe = tk.Frame(self.all_frame)
        self.topframe.pack()

        self.mainframe = tk.Frame(self.all_frame)
        self.mainframe.pack()

        self.bottomframe = tk.Frame(self.all_frame)
        self.bottomframe.pack()

        # self.gui_top_elements()
        self.gui_main_elements()
        self.gui_actions_elements()
        # self.__position_window(self.act_win)
        self.act_win.mainloop()

    def __position_window(self, any_window):
        """Center the window on screen"""
        any_window.update()

        self.screen_width = any_window.winfo_screenwidth()
        self.screen_height = any_window.winfo_screenheight()

        self.win_width = self.screen_width//2
        self.win_height = self.screen_height//2

        self.win_x = (self.screen_width//2)
        self.win_y = (self.screen_height//2)

        any_window.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")

    def hide_act_gui(self):
        self.act_win.destroy()

    def gui_top_elements(self):
        self.titleframe = tk.Frame(self.topframe)
        self.titleframe.pack(expand=1, fill='x')

        self.title = tk.Label(self.titleframe, font=('sans-serif', 20),
                              text='My Activities')
        self.title.pack(expand=1)

    def gui_main_elements(self):
        self.actsframe = tk.Frame(self.mainframe)
        self.actsframe.pack(expand=1, fill='y')

        if self.activities:
            # make a list of the activities as buttons
            self.make_buttons(self.activities)
        else:
            self.show_act_editor()

        self.msg_frame = tk.Frame(self.actsframe)
        self.msg_frame.pack(expand=1)

        self.msg = tk.Label(self.msg_frame,
                            text='Click on an activity \
button below to focus on',
                            font=('sans-serif', 15), fg='red')
        self.msg.pack(expand=1)

    def gui_actions_elements(self):
        """The area where the actions stay"""
        self.startBt = tk.Button(self.bottomframe,
                                 bg='#1a2',
                                 font=('sans-serif', 15),
                                 text="Start Timer")
        self.startBt.pack(expand=1)
        self.gui_disable_bt(self.startBt)

    def gui_enable_bt(self, bt):
        bt['state'] = 'normal'
        bt['bg'] = '#1f2'

    def gui_disable_bt(self, bt):
        bt['state'] = 'disabled'
        bt['bg'] = '#aaa'

    def make_button(self, label='activity for duration', act_obj=None):
        """Make a single button with the act_obj as
        the activity class instance

        """
        self.active = act_obj
        self.ActBt = tk.Button(self.mainframe, font=(
            'sans-serif', 10), width=30, text=label,
            command=lambda: self.select_activity(act_obj, self.ActBt))
        self.ActBt.pack(pady=5)
        return self.ActBt

        # TODO: Scrolling function

    def make_buttons(self, list_of_activities=[]):
        """The list must be a list of activity
        Return the list of button widgets made"""
        self.bt_list = []

        for act in list_of_activities:

            # for the no_time-limit feature
            if act.duration is not None:
                bt = self.make_button(f'{act.name} for {act.duration}{act.dur_type[0].lower()}',
                                      act)
                self.bt_list.append(bt)
            else:
                bt = self.make_button(f'{act.name}', act)
                self.bt_list.append(bt)

        return self.bt_list

    def show_act_editor(self, act_obj=None, bt=None):
        """You can optionally add the information so that it is inserted
        once the toplevel appears

        `bt` is for specifying which button was pressed
        so that the text can then be changed"""
        # I call him, I pass my self into him and he can now modify me
        # without creating a new instance
        a = editActivity(self, act_obj, bt)


class editActivity():
    def __init__(self, master, activity=None, caller=None):
        """The caller is just the button that initiated the edit"""
        self.master = master.act_win
        self.main = master
        self.caller = caller

        self.activity = activity

        self.show_gui(self.activity)

    def show_gui(self, info=None):
        self.edit_win = topWindow(self.master)

        self.no_limit = tk.BooleanVar(self.edit_win, False, 'no limit')

        self.all_frame = tk.Frame(self.edit_win)
        self.all_frame.pack(expand=1)

        """The title section of this GUI"""
        self.header_area = tk.Frame(self.all_frame)
        self.header_area.pack()

        self.Header = tk.Label(self.header_area,
                               text="""Create an Activity""",
                               font=('sans-serif', 20),
                               )
        self.Header.pack()

        """The form entry section of this GUI"""
        self.form_area = tk.Frame(self.all_frame)
        self.form_area.pack(pady=20, expand=1)

        self.line1 = tk.Frame(self.form_area)
        self.line1.pack(pady=20, expand=1)

        self.line2 = tk.Frame(self.form_area)
        self.line2.pack(pady=20, expand=1)

        # Title of the activity
        self.formLabel1 = tk.LabelFrame(self.line1,
                                        text="Title:",
                                        font=('sans-serif', 15),
                                        )
        self.formLabel1.pack(side='left', padx=20)

        # if the activity name is given, it means that it is editing
        # else, it is creating a new one

        self.formEntry1 = tk.Entry(self.formLabel1,
                                   font=('sans-serif', 15),
                                   )
        self.formEntry1.pack(padx=20)

        # For the editing of the activities TODO
        if info is not None:
            self.formEntry1.insert(0, str(info.name))
        # -----------------------------------

        # NOTE: FEATURE
        self.no_limit_bt = tk.Checkbutton(
            self.line2, variable=self.no_limit, text='No Time Limit', command=self.gui_no_limit)
        self.no_limit_bt.pack()

        # TESTS----------------------------

        # ------------------------------------------------

        # How long the activity is--------------------
        self.formLabel2 = tk.LabelFrame(self.line2,
                                        text="Duration",
                                        font=('sans-serif', 15),

                                        )
        self.formLabel2.pack(side='left', padx=20)

        self.formEntry2 = tk.Spinbox(self.formLabel2,
                                     font=('sans-serif', 15),
                                     from_=0,
                                     to=10000
                                     )
        self.formEntry2.pack(side='left', expand=1, padx=20)

        self.duration_option = tk.StringVar(self.edit_win)
        self.duration_options = ['Minutes', 'Seconds', 'Hours']
        self.duration_option.set(self.duration_options[0])

        self.formEntry3 = tk.OptionMenu(
            self.formLabel2, self.duration_option, *self.duration_options)
        self.formEntry3.pack(side='right')
        # --------------------------------------------

        """The action buttons section"""
        self.actions_area = tk.Frame(self.all_frame)
        self.actions_area.pack(side='bottom', fill='x', expand=1)

        self.saveBt = tk.Button(self.actions_area,
                                text="Save Activity",
                                font=('sans-serif', 15),
                                command=lambda: self.save_profile(self.main))
        self.saveBt.pack(expand=1)

        # NOTE: FEATURE of no limit
        self.pack_info = self.formLabel2.pack_info()
        self.pack_info.pop('in')
        self.gui_no_limit()

    def gui_no_limit(self):
        """What to do when the "No time limit" box is checked or unchecked"""
        if self.no_limit.get():
            self.formLabel2.pack_forget()
        else:
            self.formLabel2.pack(**self.pack_info)

    def get_info(self):
        """Get the form information
        if there's no time limit, then just 
        have duration to be none; meaning that 
        there's no specific time frame the user
        is expecting to finish his activity"""
        name = self.formEntry1.get()

        # ALWAYS when you want a "winfo..." you must
        # do widget.update() first
        self.formLabel2.update()

        if self.formLabel2.winfo_ismapped():
            duration = self.formEntry2.get()
            duration_option = self.duration_option.get()
        elif not self.formLabel2.winfo_ismapped():
            duration = None
            duration_option = None

        return dict(name=name, duration=duration, dur_type=duration_option)

    def save_profile(self, main: activitiesManager):
        """Save the profile then update the main window
        return to his caller with the information
        Create a new activity button with the provided information

        TODO: Provide a way to have the button info be modified and not add a button
          when this function is called from a button that has been clicked"""

        f = self.get_info()
        self.activity = Activity(f)
        self.edit_win.destroy()

        if self.activity.duration is not None:
            main.make_button(f'{self.activity.name} for {
                self.activity.duration}{self.activity.dur_type[0].lower()}',
                self.activity)
        # else if there's no time limit
        else:
            main.make_button(f"{self.activity.name}", self.activity)

        # add this new activity into the activities list
        main.activities.append(self.activity)
        main.store_activities()


if __name__ == '__main__':
    activitiesManager().show_act_gui()
