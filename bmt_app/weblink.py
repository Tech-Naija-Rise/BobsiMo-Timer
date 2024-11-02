from constants import *
import webbrowser as wb


class homePage():
    """Home Page of BMT"""
    def __init__(self, caller):
        self.caller=caller
        self.url = 'https://tnr-software.netlify.app/bmt/bmt'
        t=threading.Thread(name='homePage',target=self.start)
        t.start()
    def start(self):
        self.default = wb.WindowsDefault('BMT homepage')
        self.default.open_new_tab(self.url)