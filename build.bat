@echo off

pip install -r build-requirements.txt

python -m PyInstaller --onefile --noconsole --name GalacticTransliterator --clean --strip galactic_transliterator.py

set /p confirm="Do you want to delete 'build', 'env' and '*.spec'? (y/n): "

if /i "%confirm%"=="y" (
    echo Deleting 'build', 'env' and '*.spec' directories...
    rmdir /s /q build
    rmdir /s /q env
    del /q *.spec
    echo Directories deleted.
) else (
    echo Operation cancelled.
)