# Blender Hub

Blender Hub is a modern desktop application to simplify the organization of your Blender projects and manage the installation of multiple versions in a single place.



## Getting Started

### For Developers (Linux Only)

Before run the project, `node` and `npm` (or any other package manager of your choice) is needed in order to run/build the GUI.

#### Installing Node and NPM

Arch Linux:
```bash
sudo pacman -S node npm 
```

#### Installing Blender Hub

```bash
#Clone the repository
git clone https://github.com/vdfuste/blenderhub.git
cd blenderhub

# Build the GUI files
cd ui
npm install
npm run build
cd ..

# Create a virtual environment and install dependencies
python -m venv virt
source virt/bin/activate
python -m pip install -r requirements.txt

# Run the application
python main.py
```



## Roadmap

- Support for Blender versions older than 3.0.0.
- Configuration, shortcuts and themes files management throw different versions.



## License

This project is licensed under the MIT License. This means you are free to use, modify, and distribute the software as long as the original copyright notice is included. See the LICENSE file for details.