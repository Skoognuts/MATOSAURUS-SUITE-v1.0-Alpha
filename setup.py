# coding: utf-8

from cx_Freeze import setup, Executable
  
executables = [
        Executable(script = "app_v_1_2.py",icon = "icone.ico", base = "Win32GUI", targetName = "Matosaurus Rex")
]

buildOptions = dict(
        excludes = [""],
        includes = ["PyQt5"],
        include_files = ["api_mat_v_2.py", "db_path_viewer.json", "icone.png"]
)
  
setup(
    name = "Matosaurus Rex",
    version = "1.2",
    description = "Visualisation des stocks",
    author = "Julien Labatut",
    options = dict(build_exe = buildOptions),
    executables = executables
)