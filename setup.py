from cx_Freeze import setup, Executable

setup(
    name="SansCarpalFlasks",
    version="",
    description='',
    executables=[Executable("flasks.py")],
    options={
        'build_exe': {
            'packages': ['pynput', 'json', 'idna', 'queue'],
            'include_files': ['utils/']
        },
    }
)
