@echo off
REM *********************************************************************************
REM Batch file for setting up Houdini libs.
REM *********************************************************************************

ECHO.
ECHO Setting up Windows environment variables for Houdini Libs.
ECHO ==========================================================
ECHO.

REM *********************************************************************************
REM Get the location of Houdini
REM *********************************************************************************
ECHO I need to know where Houdini is installed.
ECHO Enter the path to the Houdini folder. You can use 'cut and paste'. To paste at
ECHO the command prompt, right click and select 'paste'.
set /p HFS=Path:
IF EXIST "%HFS%/bin/hython.exe" ECHO Found Houdini. Thanks...
IF NOT EXIST "%HFS%/bin/hython.exe" GOTO NO_HYTHON

REM *********************************************************************************
REM Run Pthon script.
REM *********************************************************************************
:FOUND_PYTHON
ECHO Executing Python setup script using Houdini's hython...
ECHO.
cd setenv
"%HFS%/bin/hython.exe" setenv.py
cd ..
ECHO.
GOTO :END

REM *********************************************************************************
REM HYTHON not found
REM *********************************************************************************
:NO_HYTHON
ECHO ERROR: The Houdini path you enetered was not correct. Setup failed!
ECHO.
GOTO :END

REM *********************************************************************************
REM The end.
REM *********************************************************************************
:END
ECHO Bye...
set /p dummy=Hit any key to exit.