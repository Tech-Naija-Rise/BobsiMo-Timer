"""
BMT (App Compiler Automated Script)

This is a rough script to automate the process of making an app for me
so i can quickly ship new feature updates more quickly.


I normally 
start by making the app with pyinstaller
then i typically take just the folder which is in the app folder
,copy it and paste it in a new folder which is in FINAL, named the current version

"""

import os
from bmt_app.constants import VERSION, app_name 
import shutil
import os
import pathlib


class AppNotCreatedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


VERSION = VERSION
APPNAME = app_name


# path to the app folder which will be created by the pyinstaller
dist_dir = pathlib.Path(f".\\dist")
app_folder = pathlib.Path(f".\\dist\\{APPNAME}")
# directory of the final destination of the file
final_dir = pathlib.Path(f".\\FINAL\\{VERSION}")
if not final_dir.is_dir():
    os.makedirs(final_dir)


# MAKE THE APP.exe
# STARTING WITH PYINSTALLER make the app itself
yo = f'pyinstaller --noconfirm --add-data "./BMT_logo.ico":"./appdata/imgs" --noconsole -n "{
    APPNAME}" -i "BMT_logo.ico" bmt_app/bmt1.py'

# TODO: change my python file to production code automatically
print("Starting...\n")
print("\
*NOTE*: Ensure you have changed your code to \
production")
import time
time.sleep(2)

ask = input('Have you made your code production ready? (y/n):  ')

def start():    
    # GETTING THE app FOLDER to the FINAL created folder for new version
    # once the app has been created, start copying that folder to the final dir
    # this typically happens even before the
    # even the icons and the nsi will be there as well
    if app_folder.is_dir():
        try:
            print("Taking the app's folder to the final directory...")
            shutil.copytree(app_folder, f"{final_dir}\\{APPNAME}")
        except FileExistsError:
            print("Ok...it's there already")
    else:
        print(AppNotCreatedError(
            '[x] The app has not been created yet please make the app first'))
        print("Making the app...\n",yo)
        os.system(yo)
        print('Done making app...')
        
        try:
            print("Taking the app's folder to the final directory...")
            shutil.copytree(app_folder, f"{final_dir}\\{APPNAME}")
        except FileExistsError:
            print("Ok...it's there already")




    # INSTALLER SCRIPTING---------(The end result will be an installer file)
    # making the script content
    with open('.\\templates\\installer\\installer_script_template.nsi', 'r') as template_:
        template = template_.readlines()

    print('writing script from template...')
    final_template = []


    # incase i want to change anything in the script, i can do it here
    for index, line in enumerate(template):
        if line.__contains__('!define VERSION'):
            # change the version to fit the current version of the app
            line = f'!define VERSION "{VERSION}"\n'


        # add a new line after each line so that the file looks good
        final_template.insert(index, line)


    # Write the installer to the final directory
    # making the installer file
    with open(f'{final_dir}\\{APPNAME}.nsi', 'w') as installer:
        installer.writelines(final_template)
    print('Done writing installer file')

    # FINALLY TAKE THE *IMAGES* REQUIRED FOR COMPILATION
    img1 = pathlib.Path('.\\BMT_logo.ico')
    img2 = pathlib.Path('.\\BMT_logo.png')
    img3 = pathlib.Path('.\\BMT_logo.bmp')
    imgs = [img1, img2, img3]
    for img in imgs:
        try:
            shutil.copyfile(img, f"{final_dir}\\{img}")
        except FileExistsError:
            print(f'({img}) image is there already')

if 'y' in ask:
    start()
elif 'n' in ask:
    print("Then please go to your code and make it production ready!")
