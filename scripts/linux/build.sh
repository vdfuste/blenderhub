#!/bin/bash

read -p "Enter version (default 0.1.0): " VERSION
VERSION=0.1.0

echo -n "Bundling Blender Hub... "

pyinstaller \
--noconsole \
--onedir \
--name "blenderhub" \
--add-data "data:data" \
--add-data "ui/dist:ui/dist" \
--exclude-module dev \
--exclude-module scripts \
--log-level ERROR \
--noconfirm \
main.py

echo "Done!"
echo -n "Creating .tar.xz file... "

mkdir -p "blenderhub-$VERSION-linux-x64/"
mv dist/blenderhub/ "blenderhub-$VERSION-linux-x64/app/"
cp scripts/linux/install.sh "blenderhub-$VERSION-linux-x64/"

tar \
--xz \
--create \
--file="blenderhub-$VERSION-linux-x64.tar.xz" \
"blenderhub-$VERSION-linux-x64"

echo "Done!"

rm -r blenderhub.spec "blenderhub-$VERSION-linux-x64/" build/ dist/

echo "Blender Hub $VERSION for Linux x64 successfully created!"
