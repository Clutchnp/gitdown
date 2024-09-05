@echo off

setlocal
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing PyInstaller...
    pip install pyinstaller
)
pip install -r .\requirements.txt 

echo Creating executable from gitdown.py ...
pyinstaller --onefile --distpath dist gitdown.py  

set SCRIPT_NAME=gitdown.py 
if not exist "dist\%SCRIPT_NAME%.exe" (
    echo Failed to create executable.
    exit /b 1
)


set DEST_DIR="C:\Users\%username%\AppData\Local\Programs\Python\Python312\Scripts\"

if not exist "%DEST_DIR%" (
    echo The directory "%DEST_DIR%" does not exist.
    exit /b 1
)

copy "dist\%SCRIPT_NAME%.exe" "%DEST_DIR%"

if exist "%DEST_DIR%\%SCRIPT_NAME%.exe" (
    echo Executable %SCRIPT_NAME%.exe successfully copied to %DEST_DIR%.
) else (
    echo Failed to copy executable to %DEST_DIR%.
    exit /b 1
)

endlocal
exit /b 0

