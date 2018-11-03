#!/usr/bin/env python3

import subprocess
from pathlib import Path
import re
import sys

def main():
    # Location of .pidir file, which can contain the destination path (so the
    # user doesn't have to enter it directly).
    piLocationFile = Path('./.pidir')

    # Typical format for the destination path- used to check user input.
    expectedPathFormat = re.compile('\w+@\w+:~[\w/]+')

    # piPathStr is the destination path for rsync. Loop until it is accepted.
    piPathStr = None
    while not piPathStr:

        # If there is a valid piLocationFile, read the destination path from there.
        if piLocationFile.is_file():
            with piLocationFile.open() as f:
                piPathStr = f.read().strip()

        # Otherwise, ask the user for a destination path.
        else:
            piPathStr = input('Enter destination path: ').strip()

        # If the path is different from the expectedPathFormat, verify that it was intentional.
        if not expectedPathFormat.match(piPathStr):
            print("Destination paths usually have the format '<user>@<server>:~/<path>'.")
            contStr = input("Are you sure you want '{}' to be the destination? (Y/n): ".format(
                piPathStr)).strip()
            if len(contStr) > 0 and contStr[0].lower() == 'n':
                piPathStr = None

    # Construct the command to run. (This command could be run directly in terminal.)
    cmd = 'rsync -a --delete ./ {}'.format(piPathStr)
    print('Running this command: {}'.format(cmd))

    # Run the command.
    subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSync cancelled.')
        sys.exit(0)
