import os

os.system("rm -rf ./dist")
os.system("pyinstaller -F -w main.py")
os.system("mkdir dist/assets")
os.system("mkdir dist/levels")
os.system("cp assets/*.png dist/assets/")
os.system("cp assets/*.ttf dist/assets/")
os.system("cp assets/*.wav dist/assets/")
os.system("cp -r levels/*.csv dist/levels/")