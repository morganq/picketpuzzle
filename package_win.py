import os

os.system("rmdir /Q /S dist")
os.system('pyinstaller -w -n PicketPuzzle -i assets\\icon_2_256.ico main.py')
os.system("mkdir dist\\PicketPuzzle\\assets")
os.system("mkdir dist\\PicketPuzzle\\levels")
os.system("copy assets\\*.png dist\\PicketPuzzle\\assets\\")
os.system("copy assets\\*.ttf dist\\PicketPuzzle\\assets\\")
os.system("copy assets\\*.wav dist\\PicketPuzzle\\assets\\")
os.system("copy assets\\*.ogg dist\\PicketPuzzle\\assets\\")
os.system("copy levels\\*.csv dist\\PicketPuzzle\\levels\\")