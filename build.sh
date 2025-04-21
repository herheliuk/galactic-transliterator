#!/bin/bash

if [[ "$(uname)" == "Darwin" ]]; then
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Python 3 is not installed. Installing..."
        brew install python
    fi
else
    if ! dpkg -l | grep -q python3-venv; then
        echo "python3-venv is not installed. Installing..."
        sudo apt install -y python3-venv
    fi
fi

if [ ! -d "env" ]; then
    echo "Directory 'env' does not exist. Creating virtual environment..."
    python3 -m venv env
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is not active. Activating now..."
    source env/bin/activate
fi

pip install -r build-requirements.txt

pyinstaller --onefile --noconsole --name GalacticTransliterator --clean --strip galactic_transliterator.py

deactivate

read -p "Do you want to delete 'build', 'env' and '*.spec'? (y/n): " confirm

if [[ $confirm == "y" || $confirm == "Y" ]]; then
    echo "Deleting 'build', 'env' and '*.spec' directories..."
    rm -rf build
    rm -rf env
    rm *.spec
    echo "Directories deleted."
else
    echo "Operation cancelled."
fi