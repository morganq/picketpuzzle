import os

os.system("rm -rf ./dist")
os.system('pyinstaller -w -n main --osx-bundle-identifier com.example.test main.py')
os.system("mkdir dist/main.app/Contents/MacOS/assets")
os.system("mkdir dist/main.app/Contents/MacOS/levels")
os.system("cp assets/*.png dist/main.app/Contents/MacOS/assets/")
os.system("cp assets/*.ttf dist/main.app/Contents/MacOS/assets/")
os.system("cp assets/*.wav dist/main.app/Contents/MacOS/assets/")
os.system("cp -r levels/*.csv dist/main.app/Contents/MacOS/levels/")