@echo off
setlocal enabledelayedexpansion

:: Get the flags
set "VERSION=Build_Test"
set "NO_BUILD="
set "NO_INSTALLER="
set "OUTPUT_DIR="

for %%a in (%*) do (
	if /i "%%~a"=="--no-build" ( set "NO_BUILD=1"
	) else if /i "%%~a"=="--no-installer" ( set "NO_INSTALLER=1"
	) else if /i "%%~a"=="--output-dir" ( set "OUTPUT_DIR=1"
	) else ( set "VERSION=%%a" )
)

echo %VERSION%

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
	--clean ^
	main.py

	echo %VERSION% > "dist\blenderhub\_internal\data\version.txt"
	del /s "dist\blenderhub\_internal\src\blender\__*" >nul

	echo Done!
)

:: Creating the installer
if defined NO_INSTALLER (
	echo Skipping installer creation.
) else (
	if not exist "dist\blenderhub" (
		echo Build not found. Skipping installer.
		exit /b 1
	)
	
	set /p="Creating installer... "<nul
	iscc /Q /DVersion=%VERSION% "scripts\windows\installer.iss"
	echo Done!
)


# Moving generated files to output directory
if defined OUTPUT_DIR (
	rmdir /s /q "output" 2>nul
	mkdir "output"

	move /y "blenderhub.spec" "output" >nul
	if exist "build" move /y "build" "output" >nul
	if exist "dist" move /y "dist" "output" >nul
)

echo Blender Hub %VERSION% for Windows successfully created!
