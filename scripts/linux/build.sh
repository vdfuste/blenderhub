#!/bin/bash

# Get the flags
VERSION="Build_Test"
NO_BUILD=0
NO_TAR=0

while [[ "$#" -gt 0 ]]; do
	case $1 in
		--no-build) NO_BUILD=1 ;;
		--no-tar) NO_TAR=1 ;;
		*) VERSION=$1 ;;
	esac
	shift
done

# If all flags are used, just exit the script.
if [ "$NO_BUILD" -eq 1 ] && [ "$NO_TAR" -eq 1 ]; then
	echo "Uhm... Ok, all set I guess."
	exit 0
fi


# Building the project
if [ "$NO_BUILD" -eq 1 ]; then
	echo "Skipping pyinstaller build."
else
	echo -n "Building Blender Hub $VERSION with pyinstaller... "

	pyinstaller \
	--onedir \
	--noconsole \
	--name "blenderhub" \
	--add-data "data:data" \
	--add-data "ui/dist:ui/dist" \
	--add-data "src/blender:src/blender" \
	--exclude-module dev \
	--exclude-module scripts \
	--log-level ERROR \
	--noconfirm \
	--clean \
	main.py

	echo "$VERSION" > dist/blenderhub/_internal/data/version.txt
	rm -r dist/blenderhub/_internal/src/blender/__*
	
	mkdir -p output/
	mv blenderhub.spec build/ dist/ output/

	echo "Done!"
fi


# Compressing the project in a tarball
if [ "$NO_TAR" -eq 1 ]; then
	echo "Skipping the tarball file compression."
else
	if [ ! -f "output/dist/blenderhub/blenderhub" ]; then
		echo "No pyinstaller build found. Tarball file was not made."
		exit 1
	fi

	echo -n "Creating .tar.xz file... "

	FOLDER_NAME="blenderhub-$VERSION-linux-x64"

	mkdir -p "output/$FOLDER_NAME/app"
	rm -rf "output/$FOLDER_NAME/app/*"
	
	cp -r output/dist/blenderhub/* "output/$FOLDER_NAME/app/"
	cp scripts/linux/install.sh "output/$FOLDER_NAME"

	tar \
	--xz \
	--create \
	--file="output/$FOLDER_NAME.tar.xz" \
	"output/$FOLDER_NAME"

	echo "Done!"
fi


echo "Blender Hub $VERSION for Linux successfully created!"
