from feedback_manager import feedbackManager
from gui_maker import appLayoutModifier
from profile_manager import profilesChooser
from constants import *

#For Dev only
#app_icon = './BMT_logo.ico'

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
                             command=lambda: feedbackManager(self))

        self.menubar.add_cascade(label='Help', menu=helpmenu)
        self.timer_win.configure(menu=self.menubar)

    def show_gui(self, window_name='BobsiMo Timer', window_icon=app_icon):
        self.timer_win = tk.Tk()
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

        self.pauseBt = tk.Button(self.act_area,
                                 text='I want to go on a break',
                                 font=('sans-serif', 20), command=self.pause)
        self.pauseBt.pack()
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

        self.timer_win.wm_deiconify()
        self.timer_win.bell()
        self.timer_win.tk_strictMotif(0)
        self.timer_win.tkraise()

        # NOTE: change the pause button to be to choose
        # a profile from a list of profiles again.
        # We don't the app to ever exit

        self.WidgetTextChanger(self.pauseBt, f"""\
Switch Profile""")
        self.pauseBt['command'] = self.switch_profile

        # NOTE:RESET back to default time
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
        self.fear_Allah = messagebox.askyesno("Fear Allah", """Are you pausing because you are leaving for a while?
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


def main():
    pm = profilesChooser()
    pm.show_gui(app_name,app_icon)

    bmt = BMT(pm.profile_info)


if __name__ == "__main__":
    main()
