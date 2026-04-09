#!/bin/bash

# Creates blenderhub/ directory if not exists.
sudo mkdir -p /opt/blenderhub/

# Removes app/ directory keeping versions/ if it already exists.
sudo rm -rf /opt/blenderhub/app/

# Moves the new version to /opt/blenderhub/ directory.
sudo cp -r app/ /opt/blenderhub/

# Creates a symlink so blenderhub can be called via terminal.
ln -sf /opt/blenderhub/app/blenderhub /usr/bin/blenderhub
