@echo off
setlocal

set NO_BUILD=
set NO_INSTALLER=
set KEEP_OUTPUT=
for %%a in (%*) do (
	if /i "%%~a"=="--no-build" set NO_BUILD=1
	if /i "%%~a"=="--no-installer" set NO_INSTALLER=1
	if /i "%%~a"=="--keep-output" set KEEP_OUTPUT=1
)

if defined NO_BUILD if defined NO_INSTALLER if defined KEEP_OUTPUT (
	echo Umh... Ok, all set I guess. 
	exit /b 0
)

set /p VERSION="Enter version (default 0.1.0): "
set VERSION=0.1.0

if defined NO_BUILD (
	echo Skipping Blender Hub build.
) else (
	echo|set /p="Building Blender Hub %VERSION%... "

	pyinstaller ^
	--noconsole ^
	--onedir ^
	--name "blenderhub" ^
	--add-data "data;data" ^
	--add-data "ui/dist;ui/dist" ^
	--exclude-module dev ^
	--exclude-module scripts ^
	--log-level ERROR ^
	--noconfirm ^
	main.py

	echo Done!
)

if defined NO_INSTALLER (
	echo Skipping installer creation.
) else (
	if not exist "dist" (
		echo No Blender Hub build found. The installer was not made.
		exit /b 1
	)
	
	echo|set /p="Creating installer..."

	"C:\Program Files\Inno Setup 7\ISCC.exe" /Q ^
	/DVersion=%VERSION% ^
	/O"." ^
	scripts\windows\installer.iss

	echo Done!
)

if not defined KEEP_OUTPUT (
	if exist "blenderhub.spec" del /s /q "blenderhub.spec" >nul
	if exist "build" rmdir /s /q "build" >nul

	if not defined NO_INSTALLER if not defined NO_BUILD (
		if exist "dist" rmdir /s /q "dist" >nul
	)
)

echo Blender Hub %VERSION% for Windows x64 successfully created!
