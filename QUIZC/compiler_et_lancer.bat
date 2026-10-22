@echo off
gcc quiz.c -o quiz.exe
if errorlevel 1 (
    echo Erreur pendant la compilation.
    pause
    exit /b
)
quiz.exe
pause
