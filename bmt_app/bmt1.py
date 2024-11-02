import threading, subprocess,sys,ctypes
from gui_maker import Message  # Replace with the actual import
from plyer import notification  # Replace with the actual import
import time

from activity_manager import activitiesManager as AM, Activity as ACT
from feedback_manager import sendFeedback
from weblink import homePage
from gui_maker import Window, appLayoutModifier, Message
from profile_manager import profilesChooser
from constants import *

# check for updates
import requests


def check_for_updates(current_version):
    # URL to your version.json file
    url = "https://tech-naija-rise.github.io/BobsiMo-Timer/version.json"

    try:
        # Fetch the JSON data
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()
        latest_version = data['latest_version']
        download_url = data['download_url']
        release_notes = data['release_notes']

        # Compare versions
        if latest_version > current_version:
            print(f"Update available! Latest version: {latest_version}")
            print(f"Release notes: {release_notes}")
            print(f"Download here: {download_url}")
            # You can also add code to prompt the user to download the update
        else:
            print("You are using the latest version.")

    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")


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

        self.actions_area = tk.Frame(self.all_frame)
        self.actions_area.pack(expand=True, fill='both', side='bottom')
        # ---------------------------------------------

        # BUTTONS----------------------------
        self.minimizeBt = tk.Button(self.top_frame,
                                    text='Minimize Window',
                                    font=('sans-serif', 15),
                                    command=lambda: self.timer_win.wm_iconify())
        self.minimizeBt.pack(side='right')

        self.actionBt = tk.Button(self.actions_area,
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
        helpmenu.add_command(label="Give Feedback",
                             command=lambda: sendFeedback(self))
        helpmenu.add_separator()
        helpmenu.add_command(label="Check for Updates",
                             command=lambda: self.check_for_updates(VERSION))

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

        self.actions_area = tk.Frame(self.all_frame)
        self.actions_area.pack(expand=True, fill='both', side='bottom')
        # ---------------------------------------------

        # BUTTONS----------------------------
        # self.Bt = tk.Button(self.actions_area,
        #                             text='Open my activities',
        #                             font=('sans-serif', 15),
        #                             command=lambda: self.actMan.show_gui())
        # self.minimizeBt.pack()

        self.actionBt = tk.Button(self.actions_area,
                                  text=f'Select an activity to focus on',
                                  font=('sans-serif', 13),
                                  command=self.show_activities)
        self.actionBt.pack()

        self.finishBt = tk.Button(self.actions_area,
                                  text=f'Finish',
                                  font=('sans-serif', 13),
                                  command=self.stop_timer)
        self.finishBt.pack()
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
            timeout=10
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
    def stop_timer(self):
        t = threading.Thread(target=self._stop_timer).start()

    def _stop_timer(self):
        """Stop the timer. This is run when
        the user clicks on Finish button.
        """
        # XXX: this is the lazy way of doing it
        if self.bg_timer_thread.is_alive():
            self.bg_timer_thread.join()

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

    def tasks_only_mode(self):
        """A mode for just showing my tasks but in
        a check box manner. for ticking it"""

    def check_for_updates(self, current_version):
        threading.Thread(name='updateCheck', target=lambda: self._check_for_updates(
            current_version)).start()

    def _check_for_updates(self, current_version):
        # URL to your version.json file
        url = "https://tech-naija-rise.github.io/BobsiMo-Timer/version.json"

        try:
            # Fetch the JSON data
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the JSON response
            data = response.json()
            latest_version = data['latest_version']
            self.download_url = data['download_url']
            self.release_notes = data['release_notes']

            # Compare versions
            if latest_version > current_version:
                downloadnew = Message('OKCANCEL', f'Version {latest_version} Available', f"""\
A new version of {app_name_only} is available.
Would you like to download it now?""")

                if downloadnew:
                    self.update_app(self.download_url)

                # You can also add code to prompt the user to download the update
            else:
                print("You are using the latest version.")

        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")


class BobsimoTimer:
    url = "https://tech-naija-rise.github.io/BobsiMo-Timer/version.json"
    def __init__(self):
        self.activity = None
        self.duration = 0
        self.dur_type = ''
        self.act_name = ''
        self._pause = False
        self.current_version = VERSION  # Your current version here

        if not self.is_elevated():
            self.relaunch_as_admin()  # Re-launch if not elevated
        else:
            self.check_for_updates()  # Start checking for updates
        self.root.mainloop()  # Start the Tkinter event loop
        self.check_for_updates()  # Start checking for updates
        # Initialize your GUI components here

    def is_elevated(self):
        """Check if the script is running with elevated privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
        
    def relaunch_as_admin(self):
        """Re-launch the application with admin privileges."""
        print("Requesting administrator privileges...")
        try:
            # Construct the command to run the current script as admin
            command = ['runas', '/user:Administrator', f'"{sys.executable}"'] + [f'"{arg}"' for arg in sys.argv]
            subprocess.call(command)
        except Exception as e:
            print(f"Failed to relaunch as admin: {e}")
        sys.exit()  # Exit the current instance


    def GuiUpdateMsg(self, state: str):
        """Update the main display message based on the state."""
        states = {
            'DEFAULT': self._default_state,
            'RUNNING': self._running_state,
            'BREAK': self._break_state,
            'TIMEUP': self._timeup_state
        }
        
        state = state.upper()
        if state in states:
            states[state]()

    def _default_state(self):
        """Set the default state message."""
        self.WidgetFgChanger(self.bigMsgTxt, 'green')
        self.WidgetTextChanger(self.bigMsgTxt, "What are you working on? :)")

    def _running_state(self):
        """Set the message for when the timer is running."""
        self.WidgetFgChanger(self.bigMsgTxt, 'green')
        message = (f"You have {self.duration} {self.dur_type.lower()} left to {self.act_name}."
                    if self.activity and self.activity.duration 
                    else f"You are now to {self.act_name}.")
        self.WidgetTextChanger(self.bigMsgTxt, message)

    def _break_state(self):
        """Set the message for when the user is on a break."""
        self.WidgetFgChanger(self.bigMsgTxt, 'red')
        message = ("You are on a break."
                   f" {self.duration} {self.dur_type} left."
                   if self.activity and self.activity.duration 
                   else "You are now on a break.")
        self.WidgetTextChanger(self.bigMsgTxt, message)

    def _timeup_state(self):
        """Set the message for when the timer finishes."""
        self.WidgetFgChanger(self.bigMsgTxt, 'blue')
        message = "Congrats, you have finished your activity successfully."
        self.WidgetTextChanger(self.bigMsgTxt, message)

    def start_timer(self, name, act_obj):
        """Start the timer for the given activity."""
        self.activity = act_obj
        self.act_name = act_obj.name
        self.duration = int(act_obj.duration) if act_obj.duration else 0
        self.dur_type = act_obj.dur_type

        self._init_timer_threads(name)
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

        if self.activity and self.activity.duration:
            self.bg_timer_thread.start()
        else:
            self.bg_task_thread.start()

    def _init_timer_threads(self, name):
        """Initialize the timer threads."""
        self.bg_timer_thread = threading.Thread(
            name=f'act with duration: {name}', 
            target=self.timer
        )
        self.bg_task_thread = threading.Thread(
            name=f'act only: {name}', 
            target=self.task
        )

    def task(self, act_obj):
        """Thread for tasks without a duration."""
        self.act_name = act_obj.name
        self.GuiUpdateMsg(state='RUNNING')
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

    def timer(self):
        """Countdown timer logic."""
        while self.duration > 0:
            if not self._pause:
                self.GuiUpdateMsg('RUNNING')
                time.sleep(self._get_sleep_duration())
                self.duration -= 1
            else:
                time.sleep(1)  # Check every second if paused
        
        self.timeup()

    def _get_sleep_duration(self):
        """Determine the sleep duration based on duration type."""
        if 'minute' in self.dur_type.lower():
            return 60
        elif 'hour' in self.dur_type.lower():
            return 3600
        elif 'second' in self.dur_type.lower():
            return 1

    def notify(self):
        """Notify the user that their time is up."""
        msg = f"Congratulations, you have finished the activity: {self.activity.name}."
        notification.notify(
            title=f"{self.activity.name} is over",
            message=msg,
            app_name='Bobsimo Timer',
            app_icon='path/to/icon.ico',  # Set your actual icon path
            timeout=10
        )

    def timeup(self):
        """Handle timer completion."""
        self.GuiUpdateMsg("TIMEUP")
        self.timer_win.bell()
        self.WidgetTextChanger(self.actionBt, "Go to Activities")
        self.actionBt['command'] = self.show_activities
        self.notify()

    def pause(self):
        """Pause the timer."""
        self._pause = True
        self.GuiUpdateMsg('BREAK')
        self.WidgetTextChanger(self.actionBt, 'Resume')
        self.actionBt['command'] = self.resume

    def resume(self):
        """Resume the timer."""
        self._pause = False
        self.GuiUpdateMsg('RUNNING')
        self.WidgetTextChanger(self.actionBt, 'Take a break')
        self.actionBt['command'] = self.pause

    def check_for_updates(self):
        """Check if a new version is available."""
        try:
            response = requests.get(self.url)  # URL to your JSON file
            response.raise_for_status()

            data = response.json()
            latest_version = data['latest_version']
            self.download_url = data['download_url']
            self.release_notes = data['release_notes']

            if self.current_version < latest_version:
                self._prompt_for_update(latest_version, self.download_url)

        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")

    def _prompt_for_update(self, latest_version, download_url):
        """Prompt the user to update the app."""
        response = messagebox.askyesno(
            title=f'Version {latest_version} Available',
            message=f"A new version of Bobsimo Timer is available. Would you like to download it now?"
        )

        if response:  # If the user clicked 'Yes'
            # Start a new thread for the update process
            update_thread = threading.Thread(target=self.update_app, args=(download_url,))
            update_thread.start()

    def update_app(self, download_url):
        """Download and install the new version."""
        try:
            # Download the installer to a temporary file
            local_filename = download_url.split('/')[-1]  # Extract the file name from the URL
            print(f'Downloading to {local_filename}')
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    total_length = int(r.headers.get('content-length', 0))
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            self._update_progress(len(chunk), total_length)

            print(f"Downloaded update: {local_filename}")
            self.run_installer(local_filename)

        except requests.exceptions.RequestException as e:
            print(f"Failed to download the update: {e}")

    def run_installer(self, installer_path):
        """Run the installer silently."""
        try:
            print(f"Installing {installer_path}...")
            # Example of a silent install command for NSIS
            subprocess.run([installer_path, '/S'], check=True)
            print("Installation completed successfully.")

            # Ask the user to restart the application
            if messagebox.askyesno("Restart Required", "The application needs to restart to apply the update. Restart now?"):
                self.restart_application()

        except subprocess.CalledProcessError as e:
            print(f"Installation failed: {e}")

    def restart_application(self):
        """Restart the application."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def _update_progress(self, downloaded, total):
        """Update progress (optional)."""
        percent = (downloaded / total) * 100 if total > 0 else 0
        print(f"Downloaded: {downloaded} bytes, Total: {total} bytes, Progress: {percent:.2f}%",end='\r')

def main():
    """Main entry point for the application."""
    BMT2()

if __name__ == "__main__":
    main()
