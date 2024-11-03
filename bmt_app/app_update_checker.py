from constants import *
import requests
import plyer
import tempfile
from gui_maker import Message, topWindow, Window
import ctypes


class Updater:
    """Update manager with GUI for update progress"""
    update_url = "https://tech-naija-rise.github.io/BobsiMo-Timer/version.json"

    def __init__(self, master, current_version):
        self.current_version = current_version
        self.main_app =master
        self.master = self.main_app.timer_win


        # # Start Download in Thread
        threading.Thread(target=self.check_for_updates).start()


    def show_gui(self):
        self.dialog = tk.Toplevel(self.master)
        self.dialog.title("Updating Bobsimo Timer")
        self.dialog.geometry("400x150+200+200")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.master)
        self.dialog.grab_set()

        # Label
        self.label = ttk.Label(
            self.dialog, text="Downloading the latest update...")
        self.label.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.dialog, length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        self.label2 = ttk.Label(
            self.dialog, text="")
        self.label2.pack(pady=10)    


    def check_for_updates(self):   
        # URL to your version.json file

        try:
            # Fetch the JSON data
            response = requests.get(self.update_url)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the JSON response
            data = response.json()
            self.latest_version = data['latest_version']
            self.download_url = data['download_url']
            self.release_notes = data['release_notes']
            
            # Define the installer path
            installer_filename = f"BobsiMo Timer-{self.latest_version}.exe"  # Give it a clear name
            self.installer_path = os.path.join(
                tempfile.gettempdir(), installer_filename)

            # Compare versions
            if self.latest_version > self.current_version:
                downloadnew=Message('YESNO',f'Version {self.latest_version} is Available', f"""\
A new version of {app_name_only} is available.
Would you like to update it now?""")
                if downloadnew:
                    self.show_gui()
                    self.download_installer()

                # You can also add code to prompt the user to download the update
            else:
                print("You are using the latest version.")

        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")

    def download_installer(self):
        """Download the update with progress."""
        try:
            with requests.get(self.download_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0

                with open(self.installer_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress_percentage = (
                                downloaded_size / total_size) * 100
                            self.update_progress(progress_percentage)

            self.label.config(text="Download complete! Installing update...")
            self.run_installer()

        except requests.exceptions.RequestException as e:
            self.label.config(text="Download failed!")
            messagebox.showerror(
                "Error", f"Failed to download the update: {e}")
            self.dialog.destroy()

    def run_installer(self):
        """Run the installer with elevated permissions."""
        try:
            # Use ShellExecute with 'runas' to prompt for admin permissions
            result = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", self.installer_path, "/S", None, 1)
            if result > 32:  # ShellExecute returns values over 32 on success
                if Message('YESNO',"Restart Required", "The update has been installed. Do you want to restart the app now?"):
                    self.restart_application()
            else:
                print("Installation failed or was canceled by the user.")
        except Exception as e:
            print(f"Installation failed: {e}")
    
    def update_progress(self, value):
        """Update the progress bar in the dialog."""
        self.progress["value"] = value
        self.label2['text'] = f'Downloaded: {value :0.1f}%'
        self.dialog.update_idletasks()

    def restart_application(self):
        """Restart the application."""
        exe_path = pathlib.Path(self.installer_path)  # This gives you the path of the running executable
        print(f"Restarting {exe_path}")
        self.dialog.destroy()
        self.main_app.destroy()
        # Start a new instance of the application
        # subprocess.Popen(exe_path)

        os.startfile(exe_path)

        
