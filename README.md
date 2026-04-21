# Blender Hub

Blender Hub is a modern desktop application to simplify the organization of your Blender projects and manage the installation of multiple versions in a single place.



## Installing Blender Hub

### On Windows

To install Blender Hub on Windows just download the installer from [here](https://github.com/vdfuste/blenderhub/releases/download/v0.0.1/BlenderHub-v0.0.1-Windows-Installer.exe).

### On Linux

To install Blender Hub on Linux download the tarball file from [here](https://github.com/vdfuste/blenderhub/releases/download/v0.0.1/blenderhub-v0.0.1-linux-x64.tar.xz).

Then open a terminal on the same location as the file and execute these commands:

```bash
# Extract the content of the tarball file
tar -xf blenderhub-v0.0.1-linux-x64.tar.xz

# Move to the extracted directory
cd blenderhub-v0.0.1-linux-x64

# Grant permission to the installer script
sudo chmod +x install.sh

# Execute the script
sudo ./install.sh
```

### From Source Code

```bash
# Clone the repository
git clone https://github.com/vdfuste/blenderhub.git
cd blenderhub

# Create a virtual environment and install dependencies
python -m venv virt

# Pick one based on your OS
source virt/bin/activate # Linux
virt\Scripts\activate    # Windows

python -m pip install -r requirements.txt
python -m pip install -r dev/requirements.txt

# Run build script
# Pick one based on your OS
scripts/linux/build.sh v0.0.1    # Linux
scripts\windows\build.bat v0.0.1 # Windows
```



## Roadmap

- Automatic checkout for updates.
- Support for Blender versions older than 3.0.0.
- Config page: Manage configuration, keybinds and themes files throw different versions.
- Settings page.
- MacOS support.



## License

This project is licensed under the MIT License. This means you are free to use, modify, and distribute the software as long as the original copyright notice is included. See the LICENSE file for details.
