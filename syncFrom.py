#!/usr/bin/env python3

import subprocess
from pathlib import Path
import re
import sys

def main():
    dataDestinationFile = Path('./.data_destination_dir')
    with dataDestinationFile.open() as f:
        localPathStr = f.read().strip()

    # Location of .pi_data_dir file, which can contain the source path (so the
    # user doesn't have to enter it directly).
    piLocationFile = Path('./.pi_data_dir')

    # Typical format for the source path- used to check user input.
    expectedPathFormat = re.compile('\w+@\w+:~[\w/]+')

    # piPathStr is the source path for rsync. Loop until it is accepted.
    piPathStr = None
    while not piPathStr:

        # If there is a valid piLocationFile, read the source path from there.
        if piLocationFile.is_file():
            with piLocationFile.open() as f:
                piPathStr = f.read().strip()

        # Otherwise, ask the user for a source path.
        else:
            piPathStr = input('Enter source path: ').strip()

        # If the path is different from the expectedPathFormat, verify that it was intentional.
        if not expectedPathFormat.match(piPathStr):
            print("source paths usually have the format '<user>@<server>:~/<path>'.")
            contStr = input("Are you sure you want '{}' to be the source? (Y/n): ".format(
                piPathStr)).strip()
            if len(contStr) > 0 and contStr[0].lower() == 'n':
                piPathStr = None

    # Construct the command to run. (This command could be run directly in terminal.)
    cmd = 'rsync -a --delete {} {}'.format(piPathStr, localPathStr)
    print('Running this command: {}'.format(cmd))

    # Run the command.
    subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSync cancelled.')
        sys.exit(0)
