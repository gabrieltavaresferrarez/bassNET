import shutil
from myPath import Path
import platform
import os
import sys


def copy_directory(str_pathDir, str_pathTarget):
    str_system = platform.system()
    path_pathDir = Path(str_pathDir)
    path_pathTarget = Path(str_pathTarget)
    str_folderName = path_pathDir[-1]
    path_folderCopy = path_pathTarget + str_folderName

    if path_folderCopy.exists():
        print(f'Folder {path_folderCopy} already exists. Erasing')
        if str_system == 'Windows':
            cmd = f'rmdir {path_folderCopy}'
        else:
            cmd = f'rm -r {path_folderCopy}'
        os.system(cmd)
        print(f'Folder {path_folderCopy} erased.')

    print(f'Writing {path_folderCopy[-1]} in folder {path_pathTarget} ')
    if str_system == 'Windows':
        cmd = f'xcopy {path_pathDir.path} {path_pathTarget.path} /E/H/I'
    else:
        cmd = f'cp -r {path_pathDir.path} {path_pathTarget.path}'
    os.system(cmd)   

if __name__ == '__main__':
    list_pathsLib = sys.path
    list_pathsLib = [str_path for str_path in list_pathsLib if 'site-packages' in str_path]
    str_pathLibs = list_pathsLib[0]

    str_modulePath = os.getcwd()

    copy_directory(str_modulePath, str_pathLibs)