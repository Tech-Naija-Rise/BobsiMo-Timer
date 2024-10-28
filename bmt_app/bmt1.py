from plyer import notification
from activity_manager import activitiesManager as AM, Activity as ACT
from feedback_manager import sendFeedback
from weblink import homePage
from gui_maker import Window, appLayoutModifier
from profile_manager import profilesChooser
from constants import *





class countdownTimer:
    def __init__(self, minutes):
        self.minutes = minutes

        self._pause = False
        self.display_time = f"{self.minutes}"  # minutes

    def to_seconds(self, minutes):
        return minutes*60

    def to_minutes(self, seconds):
        return divmod(seconds, 60)

    def timer(self):
        """Updates every minute"""
        while self.minutes:
            if not self._pause:
                self.display_time = f"{self.minutes}"
                self.minutes -= 1
                time.sleep(60)
            else:
                pass

    def start(self):
        t = threading.Thread(target=self.timer)
        t.start()

    def pause(self):
        self._pause = True

    def resume(self):
        self._pause = False


class BMT(countdownTimer, appLayoutModifier):
    def __init__(self, profile_info={}) -> None:

        self.profile_info = dict(profile_info)

        if self.profile_info:
            self.username = self.profile_info['username']
            self.minutes_left = self.profile_info['minutes_left']
        else:
            self.username = 'Guest'
            self.minutes_left = 90

        super().__init__(self.minutes_left)

        # for direct manipulation of json files
        self.PM = profilesChooser()

        self.show_gui()

    def menu(self):
        self.menubar = tk.Menu(self.timer_win, tearoff=False)

        helpmenu = tk.Menu(self.menubar, tearoff=0)

        helpmenu.add_command(label="Give Feedback",
                             command=lambda: sendFeedback(self))

        self.menubar.add_cascade(label='Help', menu=helpmenu)
        self.timer_win.configure(menu=self.menubar)

    def show_gui(self, window_name='BobsiMo Timer', window_icon=app_icon):
        self.timer_win = Window()
        self.timer_win.title(window_name)
        self.menu()
        self.timer_win.iconbitmap(window_icon)

        self.timer_win.state('zoomed')

        # GUI-FRAMES---------------------------------
        self.all_frame = tk.Frame(self.timer_win)
        self.all_frame.pack(expand=True, fill='both')

        self.top_frame = tk.Frame(self.all_frame)
        self.top_frame.pack(fill='x')

        self.bd_area = tk.Frame(self.all_frame)
        self.bd_area.pack(expand=True, fill='both')

        self.act_area = tk.Frame(self.all_frame)
        self.act_area.pack(expand=True, fill='both', side='bottom')
        # ---------------------------------------------

        # BUTTONS----------------------------
        self.minimizeBt = tk.Button(self.top_frame,
                                    text='Minimize Window',
                                    font=('sans-serif', 15),
                                    command=lambda: self.timer_win.wm_iconify())
        self.minimizeBt.pack(side='right')

        self.actionBt = tk.Button(self.act_area,
                                  text='I want to go on a break',
                                  font=('sans-serif', 20), command=self.pause)
        self.actionBt.pack()
        # ---------------------------------------------
        self.timer_win.protocol('WM_DELETE_WINDOW', self.exit_protocol)
        self.gui_big_msg()

        # NOTE
        self.start_timer()

        self.timer_win.mainloop()
# --------------------------------------------

    def gui_big_msg(self, msg="""
Welcome to BMT :) """):
        self.bigMsgTxt = tk.Label(self.bd_area,
                                  text=msg,
                                  font=('sans-serif', 50),
                                  fg='green')
        self.bigMsgTxt.pack(fill='both', expand=1)

    def GuiUpdateMsg(self, txt):
        """Change the main big display text"""
        self.WidgetTextChanger(self.bigMsgTxt, txt)

    def exit_protocol(self):
        """What to do when user is trying to exit"""
        from tkinter import messagebox as ms
        self.trying_to_exit = True
        if self.trying_to_exit:
            self.message_box = ms.showwarning('Can\'t exit this app',
                                              f'Sorry, {self.username}, once your timer has started.\nyou can\'t exit this app')

    # Main functionality
    def PM_update_prof(self, username, minutes_left):
        self.profile_info.update(username=username,
                                 minutes_left=minutes_left)
        self.PM.write_profile(self.profile_info)

    def timer(self):
        """Updates every minute"""
        while True:
            if self.minutes:
                if not self._pause:
                    # display

                    self.GuiUpdateMsg(f"""\
{self.username}, you have {self.minutes}
minutes left.""")

                    # record
                    self.PM_update_prof(self.username, self.minutes)

                    # NOTE change this back to 60 seconds sleep
                    time.sleep(60)

                    # countdown
                    self.minutes -= 1
                else:
                    self.PM_update_prof(self.username, self.minutes)
            else:
                self.timeup()
                break

    def timeup(self):
        """What happens when the timer finishes"""
        self.GuiUpdateMsg(f"""\
{self.username}, your time is up.
Please allow the other person
to use the computer.""")

        self.WidgetFgChanger(self.bigMsgTxt, 'red')

        
        self.timer_win.bell()
        

        self.WidgetTextChanger(self.pauseBt, f"""\
Switch Profile""")
        self.pauseBt['command'] = self.switch_profile

        
        self.PM_update_prof(
            self.username, self.PM.default_time)

    def switch_profile(self):
        """Allow the users to choose their profile when the timer
        for one profile finishes"""

        # XXX Inefficient

        # Session of this person ends
        self.timer_win.destroy()

        # it's like a loop
        self.PM.show_gui()

        # start again from the beginning
        self.__init__(self.PM.profile_info)

    def start_timer(self):
        t = threading.Thread(target=self.timer)
        # t.daemon=True
        t.start()

    def _pause_confirm(self):
        self.fear_Allah = messagebox.askyesno("No Cheating", """Are you pausing because you are leaving for a while?
                        \rNote: this is because a user might feel the urge to pause so that he gets more minutes to play in real life.""")
        return self.fear_Allah

    def pause(self):
        if self._pause_confirm():
            self._pause = True

            # Update the message content
            self.WidgetTextChanger(self.bigMsgTxt, f"""\
{self.username} has gone on a break.
they have {self.minutes} minutes left.""")
            self.WidgetFgChanger(self.bigMsgTxt, 'red')

            self.pauseBt['text'] = 'Resume'
            self.pauseBt['command'] = self.resume

    def resume(self):
        self._pause = False

        # Update the message content
        self.WidgetTextChanger(self.bigMsgTxt, f"""\
{self.username}, you have {self.minutes}
minutes left.""")
        self.WidgetFgChanger(self.bigMsgTxt, 'green')
        self.pauseBt['text'] = 'I want to go on a break'
        self.pauseBt['command'] = self.pause


class BMT2(countdownTimer, appLayoutModifier):

    def __init__(self) -> None:
        """The Activities Version of the Timer"""
        self.timer_running = False

        self.activity = None
        self.act_name = 'Something'
        self.duration = int()
        self.dur_type = 'minutes'

        # For break time feature
        self.pause_duration = 5

        super().__init__(self.duration)
        self.show_gui()

    def show_activities(self):
        """show the activities as choosable buttons"""
        AM(self).show_act_gui()

    def menu(self):
        self.menubar = tk.Menu(self.timer_win, tearoff=False)

        helpmenu = tk.Menu(self.menubar, tearoff=0)
        activities = tk.Menu(self.menubar, tearoff=0)

        activities.add_command(label="Open Activities Window",
                               command=lambda: self.show_activities())

        helpmenu.add_command(label="BMT Home Page",
                             command=lambda: homePage(self))
        helpmenu.add_separator()
        helpmenu.add_command(label="Give Feedback",
                             command=lambda: sendFeedback(self))

        self.menubar.add_cascade(label='Activities', menu=activities)
        self.menubar.add_cascade(label='Help', menu=helpmenu)

        self.timer_win.configure(menu=self.menubar)

    def __center_window(self, any_window):
        """Center the window on screen"""
        any_window.update()

        self.screen_width = any_window.winfo_screenwidth()
        self.screen_height = any_window.winfo_screenheight()
        self.win_width = self.screen_width//2
        self.win_height = self.screen_height//2

        self.win_x = (self.screen_width//2) - (self.win_width//2)
        self.win_y = (self.screen_height//2) - (self.win_height//2)

        any_window.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")

    def show_gui(self, window_name='BobsiMo Timer', window_icon=app_icon):
        self.MSG_SIZE = 50
        self.timer_win = Window()

        self.timer_win.title(window_name)

        self.menu()

        self.timer_win.iconbitmap(window_icon)

        # self.timer_win.state('zoomed')

        # GUI-FRAMES---------------------------------
        self.all_frame = tk.Frame(self.timer_win)
        self.all_frame.pack(expand=True, fill='both')

        self.top_frame = tk.Frame(self.all_frame)
        self.top_frame.pack(fill='x')

        self.bd_area = tk.Frame(self.all_frame)
        self.bd_area.pack(expand=True, fill='both')

        self.act_area = tk.Frame(self.all_frame)
        self.act_area.pack(expand=True, fill='both', side='bottom')
        # ---------------------------------------------

        # BUTTONS----------------------------
        # self.Bt = tk.Button(self.act_area,
        #                             text='Open my activities',
        #                             font=('sans-serif', 15),
        #                             command=lambda: self.actMan.show_gui())
        # self.minimizeBt.pack()

        self.actionBt = tk.Button(self.act_area,
                                  text=f'Select an activity to focus on',
                                  font=('sans-serif', 13),
                                  command=self.show_activities)
        self.actionBt.pack()
        # ---------------------------------------------
        # self.timer_win.protocol('WM_DELETE_WINDOW', self.exit_protocol)
        
        self.gui_big_msg()
        self.GuiUpdateMsg('DEFAULT')

        # Centering the window must be after all the
        # packing of its children
        # self.__center_window(self.timer_win)
        self.timer_win.bind('<Configure>', self.responsive_adjust)
        self.timer_win.mainloop()
# --------------------------------------------

    def responsive_adjust(self, event):
        """Let the size of the window drive the size of
        the big message. and vice versa"""
        width = self.timer_win.winfo_width()

        if width <= 700:
            self.modify_msg_size(30)
        else:
            self.modify_msg_size(50)

    def modify_msg_size(self, width):
        """Modify the size of the big message"""
        self.bigMsgTxt['font'] = ('sans-serif', width)
        return width

    def gui_big_msg(self, msg="""\
Welcome to BMT :) """):
        self.bigMsgTxt = tk.Label(self.bd_area,
                                  text=msg,
                                  font=('sans-serif', self.MSG_SIZE),
                                  fg='green')
        self.bigMsgTxt.pack(fill='both', expand=1)

    def GuiUpdateMsg(self, state: str):
        """Change the main big display text

        There are 4 `state`s the message can be in.
        The message can explicitly be changed

        ### 1. when the app is started the first time (DEFAULT STATE):

            "welcome to BobsiMo Timer :)"

        ### 2. when the timer starts it is one of \
        2 states depending on the activity (RUNNING STATE):

               a. 'You have 20 minutes left to {code}'
               b. 'You are to {code}'

        ### 3. when the user is on a break (BREAK STATE), then:

                "You are on a break now."

                (and an optional "you have 3 minutes left" if there's a
                 time limit/duration)

        ### 4. when the user's time is up (TIMEUP STATE) (which is only when
             there's a time limit):

                "Your time is up,
                Go to next activity?"

        ## DEFAULT STATE
        ## RUNNING STATE
        ## BREAK STATE
        ## TIMEUP STATE
        ## FREE STATE

        for the `state`, enter DEFAULT

        """
        if state.upper() == 'DEFAULT':
            self.WidgetFgChanger(self.bigMsgTxt, 'green')
            self.WidgetTextChanger(self.bigMsgTxt, f"""\
What are you working on? :)""")

        elif state.upper() == 'RUNNING':
            self.WidgetFgChanger(self.bigMsgTxt, 'green')

            if (self.activity is not None) and (self.activity.duration is not None):

                self.WidgetTextChanger(self.bigMsgTxt, f"""\
You have {self.duration} {self.dur_type.lower()} left
to {self.act_name}.""")

            else:
                self.WidgetTextChanger(self.bigMsgTxt, f"""\
You are now to
{self.act_name}.""")

        elif state.upper() == 'BREAK':
            self.WidgetFgChanger(self.bigMsgTxt, 'red')
            if (self.activity is not None) and (self.activity.duration is not None):

                self.WidgetTextChanger(self.bigMsgTxt, f"""\
You are on a break.
{self.duration} {self.dur_type} left.""")

            else:
                self.WidgetTextChanger(self.bigMsgTxt, f"""\
You are now on a break""")

        elif state.upper() == 'TIMEUP':
            self.WidgetFgChanger(self.bigMsgTxt, 'blue')
            if (self.activity is not None) and (self.activity.duration is not None):

                self.WidgetTextChanger(self.bigMsgTxt, f"""\
Congrats, You have finished
your activity succesfully""")

            else:
                self.WidgetTextChanger(self.bigMsgTxt, f"""\
Congrats, You have finished
your activity succesfully""")

    def __count_words(self):
        """internal function to count words"""
        pass

    def task(self, act_obj):
        """This is the thread to run when there's no
        duration/ time limit"""
        self.act_name = act_obj.name
        # count Up instead. depending on
        # the settings of whether he wants
        # to learn about himself.
        self.GuiUpdateMsg(state='RUNNING')
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

        ##

    def timer(self, act_obj):
        """Timer has to have an activity to time
        otherwise what's the purpose"""
        # the self.activity has already been
        # determined at the bottom self.start_timer
        self.act_name = self.activity.name
        self.duration = int(self.activity.duration)
        self.dur_type = self.activity.dur_type

        while True:
            if not self.duration <= 0:
                if not self._pause:

                    self.GuiUpdateMsg('RUNNING')

                    if 'minute' in self.dur_type.lower():
                        time.sleep(60)
                    elif 'hour' in self.dur_type.lower():
                        time.sleep(60*60)
                    elif 'second' in self.dur_type.lower():
                        time.sleep(1)

                    self.duration -= 1
                else:
                    pass
            else:
                self.timeup()
                break

    def notify(self):
        """Notify the user that his time is up"""
        msg = f"""\
Congratulations, you have finished 
the activity: {self.activity.name}."""
        
        notification.notify(
            title=f"{self.activity.name} is over",
            message=msg,
            app_name=app_name,
            app_icon=app_icon,
            timeout=120
        )

    def timeup(self):
        """What happens when the timer finishes"""
        self.GuiUpdateMsg("TIMEUP")

        self.timer_win.bell()

        self.WidgetTextChanger(self.actionBt, f"Go to Activities")
        self.actionBt['command'] = self.show_activities
        try:
            self.notify()
        except Exception:
            pass

        # NOTE: change the pause button to be to choose
        # a profile from a list of profiles again.
        # We don't the app to ever exit for parent mode


    def resume(self):
        """Resume the timer"""
        self._pause = False
        self.GuiUpdateMsg('RUNNING')
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

    def pause(self):
        """Cause a pause loop for a limited time"""
        self._pause = True
        self.GuiUpdateMsg('BREAK')
        self.WidgetTextChanger(self.actionBt, 'Resume')
        self.actionBt['command'] = self.resume

    def start_timer(self, name, act_obj: ACT):
        """The function that determines 
        whether to count down or up."""

        # The current activity whose timer is to be started
        self.activity = act_obj

        # Now we have the data here
        self.bg_timer_thread = threading.Thread(
            name=f'act with duration: {name}', target=lambda: self.timer(self.activity))

        self.bg_task_thread = threading.Thread(
            name=f'act only: {name}', target=lambda: self.task(self.activity))

        # Determine from here whether this is just an activity
        # or a timed one
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

        if (act_obj is not None) and (act_obj.duration is not None):
            self.bg_timer_thread.start()
        else:
            self.bg_task_thread.start()

    def stop_timer(self):
        """Stop the timer"""


def main():
    # TODO: Make the window resizing to be responsive
    # i.e. make the text be smaller when the window gets smaller
    # TODO: reset the timer: take it back to "welcome"
    BMT2()


if __name__ == "__main__":
    main()
