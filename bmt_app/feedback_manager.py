import webbrowser as wb
from gui_maker import appLayoutModifier
from constants import *


class feedbackManager(appLayoutModifier):

    # NOTE: Production only
    FEEDBACK_DIR = f"{computer}\\Appdata\\Local\\BobsiMo Timer\\feedback"

    # NOTE: Use this in development instead but comment out before production
    # FEEDBACK_DIR = f".\\feedback"

    def __init__(self, master, window_name='BMT - Feedback Manager',
                 window_icon=app_icon):
        self.master = master
        self.profile_info = self.master.profile_info
        self.feedback_win = tk.Toplevel(self.master.timer_win)
        self.feedback_win.wm_title(window_name)
        self.feedback_win.wm_iconbitmap(window_icon)
        self.feedback_win.wm_transient(self.master.timer_win)
        self.feedback_win.grab_set()

        # A json file with the information about the person
        # sending the feedback
        self.the_feedback = {}

        # Widgets
        self.text_area = ScrolledText(self.feedback_win,
                                      font=('consolas', 20),
                                      width=24, height=10)
        self._textareaplaceholder()
        self.text_area.pack(expand=1, fill='both')

        # when we tap on the text to type, the place holder goes
        self.text_area.bind('<FocusIn>', self._textareaplaceholderrestore)

        self.options_area = self.AreaMaker(self.feedback_win)

        self.ButtonMaker(self.options_area, 'Send Feedback',
                         command=self.send_feedback)

    def _textareaplaceholder(self):
        # Place holder
        self.text_area.insert(1.0, 'Write your feedback here...')
        self.WidgetFgChanger(self.text_area, '#aaa')

    def _textareaplaceholderrestore(self, event=None):
        # Place holder to allow for writing.
        self.text_area.delete(1.0, tk.END)
        self.WidgetFgChanger(self.text_area, '#111')

    def send_feedback(self):
        self.the_feedback.update(**self.master.profile_info)
        self.the_feedback.update(
            feedback=self.text_area.get(1.0, tk.END)
        )
        self.write_to_json()
        self.feedback_win.destroy()

    def write_to_json(self):
        """make a json file with the profile information
        of the person sending the feedback and his feedback message.
        {
        "username":"Bobsi"
        "minutes_left": 50
        "feedback":['''lkjsdlkjlfjlaskdlk''', ...]
        }

        """
        if not os.path.isdir(self.FEEDBACK_DIR):
            os.makedirs(self.FEEDBACK_DIR)

        # OPEN the json file for appending to whatever is in it, not overwriting
        with open(f"{self.FEEDBACK_DIR}\\FB.json", 'a') as fdb:
            json.dump(self.the_feedback, fdb, indent=4,
                      separators=(',', ':'))


class sendFeedback():
    def __init__(self, caller):
        self.caller = caller
        self.url = 'https://mail.google.com/mail/?extsrc=mailto&url=mailto%3Atechnaijarise%40gmail.com'
        self.default = wb.WindowsDefault('feedback')
        self.default.open_new_tab(self.url)
