import os

os.system("rm -rf ./dist")
os.system('pyinstaller -w -n PicketPuzzle -i assets/icon_2_256.icns --osx-bundle-identifier com.example.test main.py')
os.system("mkdir dist/PicketPuzzle.app/Contents/MacOS/assets")
os.system("mkdir dist/PicketPuzzle.app/Contents/MacOS/levels")
os.system("cp assets/*.png dist/PicketPuzzle.app/Contents/MacOS/assets/")
os.system("cp assets/*.ttf dist/PicketPuzzle.app/Contents/MacOS/assets/")
os.system("cp assets/*.wav dist/PicketPuzzle.app/Contents/MacOS/assets/")
os.system("cp assets/*.ogg dist/PicketPuzzle.app/Contents/MacOS/assets/")
os.system("cp -r levels/*.csv dist/PicketPuzzle.app/Contents/MacOS/levels/")