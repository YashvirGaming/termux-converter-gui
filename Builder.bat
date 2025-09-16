@echo off
set SCRIPT=termux_converter.py
set ICON=icon.ico

title Building Termux Converter GUI with Nuitka...
python -m nuitka %SCRIPT% ^
  --standalone ^
  --onefile ^
  --remove-output ^
  --jobs=12 ^
  --enable-plugin=tk-inter ^
  --windows-disable-console ^
  --windows-icon-from-ico=%ICON%

echo.
echo ✅ Build complete! Your EXE is ready.
pause
