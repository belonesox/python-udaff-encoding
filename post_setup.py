from distutils.sysconfig import get_python_lib
from shutil import copyfile
from os import path

def main():
    here = path.abspath(path.dirname(__file__))
    copyfile(
        path.join(here, 'udaff.pth'),
        path.join(get_python_lib(), 'udaff.pth')
    )

if __name__ == '__main__':
    main()
