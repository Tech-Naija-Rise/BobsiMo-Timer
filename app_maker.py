"""Just make the app with specs and the builds and what not.
Delete all except "dist" folder then move the dist
outside the dev folder
"""
import os
from bmt_app.constants import VERSION, app_name, app_name_only
import shutil
import os
import pathlib


yo = f'''\
pyinstaller --noconfirm --add-data "./BMT_logo.ico":"./appdata/imgs" \
--noconsole -n "{app_name_only}" -i "BMT_logo.ico" --hidden-import "plyer" \
./bmt_app/bmt1.py'''


print('[x] The app has not been created yet please make the app first')
print("Making the app...\n", yo)
os.system(yo)

# When app is done cooking,
# delete all the generated files
# except for the dist folder which
# will be moved to prod folder


app_folder = pathlib.Path(f'.\\dist\\{app_name_only}')
print(f'Done making app... in ({app_folder})')


# put the icon into the folder
print('putting icon into app folder')
app_icon_img1 = pathlib.Path('.\\BMT_logo.ico')
shutil.copy(app_icon_img1, f'{app_folder}')
print(f'image is now in {app_folder}')



# make a folder in which all versions will stay
print('making FINAL folder where all versions will stay')
final_dir = pathlib.Path('..\\PROD2\\FINAL')
try:
    os.makedirs(final_dir)
except FileExistsError:
    print('FINAL folder exists')

# move the app_folder to the new prod2 inside FINAL folder
# with the version name
print(f'moving the app folder {app_folder.stem} to FINAL')
a = shutil.move(app_folder, f'{final_dir}\\{VERSION}\\{app_name}')
print(f'moved to {a}') 

# # FINALLY TAKE THE *IMAGES* REQUIRED FOR COMPILATION
# img1 = pathlib.Path('.\\BMT_logo.ico')
# img2 = pathlib.Path('.\\BMT_logo.png')
# img3 = pathlib.Path('.\\BMT_logo.bmp')
# imgs = [img1, img2]
# for img in imgs:
# try:
#     shutil.copyfile(img, f"{final_dir}\\{img}")
#     shutil.copyfile(img, f"{final_dir}\\{APPNAME_ONLY}\\{img}")
# except FileExistsError:
#     print(f'({img}) image is there already')
