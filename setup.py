from cx_Freeze import setup, Executable
import sys, os

includefiles=["etc"]
if sys.platform == "win32":
    exe = Executable(
        script="src/main.py",
        #icon="sbb-tree.ico,"
        base="Win32GUI",
        appendScriptToExe=True,
        appendScriptToLibrary=False
        )
else:
    exe = Executable(
        script="src/main.py",
        #appendScriptToExe=True,
        #appendScriptToLibrary=False
        )
    includefiles.append("run")
buildOptions = dict(create_shared_zip=False, include_files=includefiles)
setup(
    name = "Blind-Cassi",
    version = "0.1.x",
    description = "None",
    author = "Rafael Trindade",
    options=dict(build_exe=buildOptions),
    executables = [exe]
    )
