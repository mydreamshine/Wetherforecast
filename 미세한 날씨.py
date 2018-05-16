import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = ".\\SDL2\\x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = ".\\SDL2\\x64"

import Framework
import main_state
from pico2d import *

open_canvas(300, 427, 60)
Framework.run(main_state)
close_canvas()
