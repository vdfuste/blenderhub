@echo off
setlocal enabledelayedexpansion

:: Get the version
if "%~1"=="" (
	echo No version especified. Exiting now...
	exit /b 1
)

set "VERSION=%~1"
set "NO_BUILD="
set "NO_INSTALLER="

:: Get the flags
for %%a in (%*) do (
	if /i "%%~a"=="--no-build" set "NO_BUILD=1"
	if /i "%%~a"=="--no-installer" set "NO_INSTALLER=1"
)

:: If all flags are used, just exit the script.
if defined NO_BUILD if defined NO_INSTALLER (
	echo Uhm... Ok, all set I guess.
	exit /b 0
)

:: Building the project
if defined NO_BUILD (
	echo Skipping pyinstaller build.
) else (
	set /p="Building Blender Hub %VERSION% with pyinstaller... "<nul

	pyinstaller ^
	--onedir ^
	--noconsole ^
	--name "blenderhub" ^
	--add-data "data;data" ^
	--add-data "ui/dist;ui/dist" ^
	--add-data "src/blender;src/blender" ^
	--exclude-module dev ^
	--exclude-module scripts ^
	--log-level ERROR ^
	--noconfirm ^
	main.py

	del /s "dist\blenderhub\_internal\src\blender\__*" >nul

	if not exist "output\" mkdir "output\"
	move /y "blenderhub.spec" "output\" >nul
	if exist "build\" move /y "build\" "output\" >nul
	if exist "dist\" move /y "dist\" "output\" >nul

	echo Done!
)

:: Creating the installer
if defined NO_INSTALLER (
	echo Skipping installer creation.
) else (
	if not exist "output\dist\blenderhub" (
		echo Build not found. Skipping installer.
		exit /b 1
	)
	
	set /p="Creating installer... "<nul
	iscc /Q /DVersion=%VERSION% /O"output\" "scripts\windows\installer.iss"
	echo Done!
)

echo Blender Hub %VERSION% for Windows successfully created!
