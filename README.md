# Blender Hub

Blender Hub is a modern desktop application to simplify the organization of your Blender projects and manage the installation of multiple versions in a single place.



## Getting Started

### For Developers

#### Installing Blender Hub

```bash
#Clone the repository
git clone https://github.com/vdfuste/blenderhub.git
cd blenderhub

# Create a virtual environment and install dependencies
python -m venv virt

# Pick one based on your OS
source virt/bin/activate # Linux and MacOS
virt\Scripts\activate    # Windows

python -m pip install -r requirements.txt

# Run the application
python main.py

# Or run the app in development mode
python dev
```
#### Running the UI

```bash
# Go to the UI directory
cd blenderhub/ui

# Install all the packages
npm install

# Normal mode:
# Build the UI. No need to keep the terminal open.
npm run build

# Development mode:
# Use this to run the UI and make changes on real-time.
# Needs to keep the terminal open.
npm run dev

# Then run the app
python dev --local-gui
```

> [!NOTE]
> Both `node` and `npm` (or any other package manager of your choice) is required in order to run/build the GUI.



## Roadmap

- Automatic checkout for updates.
- Support for Blender versions older than 3.0.0.
- Config page: Manage configuration, keybinds and themes files throw different versions.
- Settings page.
- MacOS support.



## License

This project is licensed under the MIT License. This means you are free to use, modify, and distribute the software as long as the original copyright notice is included. See the LICENSE file for details.
