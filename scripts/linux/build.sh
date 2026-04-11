#!/bin/bash

read -p "Enter version (default 0.1.0): " VERSION
VERSION=0.1.0

echo -n "Bundling Blender Hub... "

pyinstaller \
--noconsole \
--onedir \
--name "blenderhub" \
--add-data "src/blender:src/blender" \
--add-data "data:data" \
--add-data "ui/dist:ui/dist" \
--exclude-module dev \
--exclude-module scripts \
--log-level ERROR \
--noconfirm \
main.py

rm -r dist/blenderhub/_internal/src/blender/__*

echo "Done!"
echo -n "Creating .tar.xz file... "

FOLDER_NAME="blenderhub-$VERSION-linux-x64"

mkdir -p "$FOLDER_NAME"
#mv dist/blenderhub/ "$FOLDER_NAME/app/"
cp -r dist/blenderhub/ "$FOLDER_NAME/app/"
cp scripts/linux/install.sh "$FOLDER_NAME"

tar \
--xz \
--create \
--file="$FOLDER_NAME.tar.xz" \
"$FOLDER_NAME"

echo "Done!"

#rm -r blenderhub.spec "$FOLDER_NAME" build/ dist/
rm -r blenderhub.spec build/

echo "Blender Hub $VERSION for Linux x64 successfully created!"
