@echo off
setlocal

:: Get the version
if "%~1"=="" (
	echo No version especified. Exiting now...
	exit /b 1
) else (
	set VERSION=%1
)


:: Get the flags
set NO_BUILD=
set NO_INSTALLER=

for %%a in (%*) do (
	if /i "%%~a"=="--no-build" set NO_BUILD=1
	if /i "%%~a"=="--no-installer" set NO_INSTALLER=1
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
	echo|set /p="Building Blender Hub %VERSION% with pyinstaller... "

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

	if not exists "output\" mkdir "output\" >nul
	move /y "blenderhub.spec" "output\" >nul
	move /y "build\" "output\" >nul
	move /y "dist\" "output\" >nul

	echo Done!
)


:: Creating the installer
if defined NO_INSTALLER (
	echo Skipping installer creation.
) else (
	if not exist "output\dist\blenderhub\blenderhub" (
		echo No Blender Hub build found. The installer was not made.
		exit /b 1
	)
	
	echo|set /p="Creating installer..."

	:: Only for local testing purposes
	:: C:\Program Files\Inno Setup 7\ISCC.exe
	
	iscc /Q ^
	/DVersion=%VERSION% ^
	/O"output\" ^
	scripts\windows\installer.iss

	echo Done!
)

echo Blender Hub %VERSION% for Windows successfully created!
