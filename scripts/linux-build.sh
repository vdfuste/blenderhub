#!/bin/bash

echo -n "Bundling Blender Hub... "

pyinstaller \
--noconsole \
--onedir \
--name "blenderhub" \
--add-data "ui/dist:ui" \
--exclude-module dev \
--exclude-module scripts \
--log-level WARN \
main.py

echo "Done!"
echo -n "Creating .tar.xz file... "

mkdir -p blenderhub-0.1.0-linux-x64/
mv dist/blenderhub/ blenderhub-0.1.0-linux-x64/app/
cp scripts/install.sh blenderhub-0.1.0-linux-x64/

tar \
--xz \
--create \
--file=blenderhub-0.1.0-linux-x64.tar.xz \
blenderhub-0.1.0-linux-x64

echo "Done!"

rm -r blenderhub.spec blenderhub-0.1.0-linux-x64/ build/ dist/

echo "Blender Hub 0.1.0 for Linux x64 successfully created!"
