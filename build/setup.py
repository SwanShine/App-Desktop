import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["customtkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SwanShine",
    version="0.1",
    description="Primeiro app da swanshine",
    options={"build_exe": build_exe_options},
    executables=[Executable("App_swanshine.py", base=base)]
)