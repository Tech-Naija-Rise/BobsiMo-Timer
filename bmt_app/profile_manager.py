from constants import *
from gui_maker import appLayoutModifier,Button

class profileViewer(appLayoutModifier):
    def __init__(self) -> None:
        self.PM = profilesChooser()



class profilesCreator(appLayoutModifier, tk.Toplevel):
    def __init__(self, master, window_name='BMT - Profiles Creator',
                 window_icon=''):
        """Where all sections stay"""
        self.profile_info = {}
        self.PM = profilesChooser()
        self.username = ''

        super().__init__(master)
        self.wm_title(window_name)
        try:
            self.iconbitmap(window_icon)
        except Exception:
            pass
        self.transient(master)
        self.grab_set()

        self.all_frame = tk.Frame(self)
        self.all_frame.pack(expand=1)

        """The title section of this GUI"""
        self.header_area = tk.Frame(self.all_frame)
        self.header_area.pack()

        self.Header = tk.Label(self.header_area,
                               text="""Create Your Profile""",
                               font=('sans-serif', 20),
                               )
        self.Header.pack()

        """The form entry section of this GUI"""
        self.form_area = tk.Frame(self.all_frame)
        self.form_area.pack(pady=20, expand=1)

        self.formLabel1 = tk.Label(self.form_area,
                                   text="Name:",
                                   font=('sans-serif', 10),
                                   )
        self.formLabel1.pack(side='left', padx=20)

        self.formEntry1 = tk.Entry(self.form_area,
                                   font=('sans-serif', 10),
                                   )
        self.formEntry1.pack(padx=20)

        """The action buttons section"""
        self.actions_area = tk.Frame(self.all_frame)
        self.actions_area.pack(side='bottom', fill='x', expand=1)

        self.createBt = Button(self.actions_area,
                                  text="Create Profile",
                                  font=('sans-serif', 10),
                                  command=self.create_profile)
        self.createBt.pack(expand=1)

    def get_form_info(self):
        """get all information entered into the form"""
        username = self.formEntry1.get()
        return username

    def create_profile(self):
        """Create a new profile with the default time"""
        self.username = self.get_form_info()

        warning = tk.Label(self.actions_area, text="""\
        please enter your name""", fg='red')
        # if the username has been typed
        if not self.username.strip():
            warning.pack()
        else:
            warning.forget()
            self.profile_info.update(
                username=self.username, minutes_left=self.PM.default_time)
            self.PM.write_profile(self.profile_info)
            self.destroy()
            return


class profilesChooser(appLayoutModifier):

    # NOTE: Production only
    PROFILES_DIR = f"{computer}\\Appdata\\Local\\BobsiMo Timer\\profiles"

    # NOTE: Use this in development instead but comment out before production
    # PROFILES_DIR = f".\\profiles"

    def __init__(self) -> None:
        """I am incharge of all functions having to do with
        touching (reading and writing) profile json files"""
        self.profile_info = {}
        self.default_time = 90

    # GUI methods: everything frontend
    def exit_protocol(self):
        """What to do when user is trying to exit"""
        from tkinter import messagebox as ms
        self.trying_to_exit = True
        if self.trying_to_exit:
            self.message_box = ms.showwarning('Can\'t exit this app',
                                              f"Sorry, you can't exit this app")

    def show_gui(self, window_name='BMT - Profiles Chooser', window_icon=''):
        self.profiles_win = tk.Tk(className=f' {window_name}')
        self.profiles_win.wm_protocol('WM_DELETE_WINDOW', self.exit_protocol)
        try:
            self.profiles_win.iconbitmap(window_icon)
        except Exception:
            pass

        self.profiles_win.wm_state('zoomed')

        self.gui_section_container()
        self._gui_center_window()

        # NOTE: the order of these functions is very important

        self._gui_profiles_section()
        self._gui_profile_viewer_section()

        self.profiles_win.mainloop()

    def gui_section_container(self):
        self.all_frame = tk.Frame(self.profiles_win)
        self.all_frame.pack(fill='both', expand=1)

        self.profiles_section = tk.Frame(self.all_frame)
        self.profiles_section.pack(side='left', fill='both', expand=1)

        self.profile_view_section = tk.Frame(self.all_frame)
        self.profile_view_section.pack(
            side='top', fill='both', expand=1, padx=10)

        self.profiles_create_section = tk.Frame(self.all_frame)
        self.profiles_create_section.pack(side='bottom', fill='both', expand=1)

    def _gui_profiles_section(self, title_txt: str = """\
PROFILES CHOOSER""", subtitle_txt="""\
Choose your profile to continue from where you stopped."""):
        
        """Make header section of this window"""
        # profiles area
        self.profiles_area = tk.Frame(self.profiles_section)
        self.profiles_area.pack(expand=1)

        self.header = tk.Frame(self.profiles_area)
        self.header.pack()

        self.profiles_bt_area = tk.Frame(self.profiles_area)
        self.profiles_bt_area.pack(pady=50)

        self._gui_no_profiles_msg()  # message when there are no profiles

        self.profilesSectionTitle = tk.Label(self.header,
                                             text=title_txt,
                                             font=('sans-serif', 20))
        self.profilesSectionTitle.pack()

        self.profilesSectionSubtitle = tk.Label(self.header,
                                                text=subtitle_txt,
                                                font=('sans-serif', 15))
        self.profilesSectionSubtitle.pack(pady=10)

        # make the buttons
        list_of_profilenames = self.get_profiles()
        self.make_profile_bts(*list_of_profilenames)

        # area for actions buttons
        self.profiles_actions_area = tk.Frame(self.profiles_area)
        self.profiles_actions_area.pack(expand=1)

        self.startBt = Button(self.profiles_actions_area,
                                 bg='#1f2',
                                 font=('sans-serif', 20),
                                 text="Start Timer")
        self.startBt.pack(expand=1)

        try:
            username = self.profile_info['username']
            self.startBt['command'] = lambda: self.continue_with(username)
        except Exception:
            self.WidgetBgChanger(self.startBt, '#aaa')
            self.startBt['state'] = 'disabled'

    def _gui_no_profiles_msg(self, msg="""\
There are no profiles. Please create one on the right."""):
        """The text to tell the user that there are no
        profiles available, so they can create below,
        THis is only called when there are no profiles otherwise,
        dispay buttons instead"""
        self.noProfilesMsg = tk.Label(self.profiles_bt_area,
                                      text=msg, fg='red', font=('sans-serif', 10))

    def make_profile_bt(self, name: str, position):
        """Make a single profile button .
        `position` parameter is for arrangement purposes"""
        self.profileBt = Button(self.profiles_bt_area,
                                   text=name.title(),
                                   font=('sans-serif', 15),
                                   command=lambda:
                                   self.view_profile_info(name.lower()))
        self.profileBt.grid(row=0, column=position, padx=10)

        return self.profileBt

    def make_profile_bts(self, *list_of_profilenames):
        """Make buttons from a list of profiles"""
        if list_of_profilenames:
            for name, __columns___ in zip(
                    list_of_profilenames,
                    range(list_of_profilenames.__len__())):
                self.make_profile_bt(name, __columns___)

    def _gui_profile_create_section(self, head_text: str = """\
Can't find your name?"""):
        self.profile_create_area = tk.Frame(self.profiles_create_section)
        self.profile_create_area.pack(expand=1)

        self.profileCreateSubtitle = tk.Label(
            self.profile_create_area,
            text=head_text, fg='#aaa', font=('sans-serif', 20))
        self.profileCreateSubtitle.pack()

        self.profileCreateBt = Button(self.profile_create_area, text="""\
Create your profile""", font=('sans-serif', 10),
            command=self.launch_profile_creator)
        self.profileCreateBt.pack()

    def _gui_profile_viewer_section(self, txt="""\
Click on a profile button to view
how much time you have left""", bg='#ddd', fg='#555'):
        """create a section to view basic info about the user"""
        self.profile_info_viewer_area = tk.Frame(self.profile_view_section,
                                                 bg=bg)
        self.profile_info_viewer_area.pack(expand=1, fill='y')
#
        self.profileInfoViewerText = tk.Label(self.profile_info_viewer_area,
                                              text=txt,
                                              font=('sans-serif', 20),
                                              bg=bg, fg=fg)
        self.profileInfoViewerText.pack(expand=1)

        self.seeDetailsBt = Button(self.profile_info_viewer_area,
                                      text='See Details', state='disabled')
        self.seeDetailsBt.pack(expand=1)

    def _gui_center_window(self):
        """center the app on screen"""
        self.profiles_win.update()

        self.win_width = 1000
        self.win_height = 400

        self.screen_width = self.all_frame.winfo_screenwidth()
        self.screen_height = self.all_frame.winfo_screenheight()

        self.win_x = (self.screen_width//2) - (self.win_width//2)
        self.win_y = (self.screen_height//2) - (self.win_height//2)

        self.profiles_win.wm_geometry(f"{self.win_width}x{
            self.win_height}+{self.win_x}+{self.win_y}")

    def hide_gui(self):
        """Hide the GUI"""

        try:
            self.profiles_win.destroy()
        except Exception:
            pass
    

    # Functionality: methods for touching the json files directly
    def get_profiles(self):
        """Get the list profilenames from the profiles
        folder, then append them to the `profilenames` folder"""
        self.profilenames = []

        profile_folder = pathlib.Path(self.PROFILES_DIR)
        try:
            for each_file in profile_folder.iterdir():
                self.profilenames.append(each_file.stem)

        # Meaning that either the folder doesn't exist
        # or we can't find it where we are searching
        except FileNotFoundError as e:
            # 1.3.0 FEATURE: prompt parent to create a profile for each
            self.prompt_parent_to_create_profile()

        return self.profilenames

    def read_profile(self, name):
        """Get the profile information from the json
        file and return it"""

        # get the profile info
        with open(f"{self.PROFILES_DIR}\\{name}.json", 'r') as profinfo:
            # assign this to the main self.profile_info dict
            self.profile_info = json.load(profinfo)
        return self.profile_info

    def write_profile(self, profile_info):
        """Create or update a users profile with 
        his `name` as the json's filename and the profile dictionary
        to write into this json file"""
        if profile_info:
            name = str(profile_info['username']).lower()
            # create profiles folder if none
            if os.path.isdir(self.PROFILES_DIR):
                pass
            else:
                # NOTE: PRODUCTION ONLY: os.makedirs
                #  Make a folder to hold all profile .json files
                os.makedirs(self.PROFILES_DIR)

            # make the file itself and dump the profile info inside
            with open(f"{self.PROFILES_DIR}\\{name}.json", 'w') as profile:
                json.dump(profile_info, profile)

    # -----------------------------------------------
    
    def prompt_parent_to_create_profile(self):
        """This is what happens when the app is installed newly on a computer
        The parent is prompted to make a profile for all of the kids who
        will be using the computer. This is the activation.
        """
        self.launch_profile_creator()

        #XXX
    def CTA(self):
        """DEPRECATED (see prompt_parent_to_create_profile): This is what happens when 
        there are no profiles.
        
        It calls the users attention to a button prompting for 
        creation of a profie"""

        self.WidgetBgChanger(self.profileCreateBt, 'red')
        self.WidgetFgChanger(self.profileCreateBt, 'white')
        self.noProfilesMsg.grid()


    # PROFILES CREATOR WINDOW --------------
    def profileCreator(self, window_name='BMT - Profiles Creator',
                       window_icon=app_icon):
        """Where all sections stay"""
        self.profcreator_win = tk.Toplevel(self.profiles_win)
        self.profcreator_win.wm_title(window_name)
        try:
            self.profcreator_win.wm_iconbitmap(window_icon)
        except Exception:
            pass
        self.profcreator_win.transient(self.profiles_win)
        self.profcreator_win.grab_set()

        self.all_frame = tk.Frame(self.profcreator_win)
        self.all_frame.pack(expand=1)

        """The title section of this GUI"""
        self.header_area = tk.Frame(self.all_frame)
        self.header_area.pack()

        self.Header = tk.Label(self.header_area,
                               text="""Create Your Profile""",
                               font=('sans-serif', 20),
                               )
        self.Header.pack()

        """The form entry section of this GUI"""
        self.form_area = tk.Frame(self.all_frame)
        self.form_area.pack(pady=20, expand=1)

        self.formLabel1 = tk.Label(self.form_area,
                                   text="Name:",
                                   font=('sans-serif', 10),
                                   )
        self.formLabel1.pack(side='left', padx=20)

        self.formEntry1 = tk.Entry(self.form_area,
                                   font=('sans-serif', 10),
                                   )
        self.formEntry1.pack(padx=20)

        """The action buttons section"""
        self.actions_area = tk.Frame(self.all_frame)
        self.actions_area.pack(side='bottom', fill='x', expand=1)

        self.createBt = Button(self.actions_area,
                                  text="Create Profile",
                                  font=('sans-serif', 10),
                                  command=self.create_profile)
        self.createBt.pack(expand=1)

        return self.profcreator_win

    def get_form_info(self):
        """get all information entered into the form"""
        username = self.formEntry1.get()
        return username

    def launch_profile_creator(self):
        self.PCr = self.profileCreator()
        self.PCr.mainloop()

    def create_profile(self):
        """Create a new profile with the default time"""
        self.username = self.get_form_info()

        warning = tk.Label(self.actions_area, text="""\
        please enter your name""", fg='red')
        # if the username has been typed
        if not self.username.strip():
            warning.pack()
        else:
            warning.forget()
            self.profile_info.update(
                username=self.username, minutes_left=self.default_time)

            self.write_profile(self.profile_info)


            self.make_profile_bt(self.username, len(self.profilenames))
            self.PCr.destroy()
# ---------------------------------------------

    def continue_with(self, name):
        """Continue with this user (whose name is clicked on).

        When we click our profile button, we want get the profile information,
        then assign that to the `profile_info` dict.

        Then exit the GUI (profileManager)"""

        self.read_profile(name)

        self.hide_gui()

    def view_profile_info(self, name):
        """Show the information from the json file in a 
        pretty format"""

        profileinfo = self.read_profile(name)
        username = profileinfo['username']
        mins_left = profileinfo['minutes_left']

        self.startBt['state'] = 'normal'
        self.WidgetBgChanger(self.startBt, '#1d1')
        self.WidgetFgChanger(self.startBt, '#111')
        self.startBt['command'] = lambda: self.continue_with(username)

        # prettified
        profile_info_viewer_text = f"""\
{username}, you have {mins_left} minutes left."""

        self.WidgetTextChanger(self.profileInfoViewerText,
                               profile_info_viewer_text)
# -----------------------------------------------------


if __name__ == '__main__':
    profilesChooser()