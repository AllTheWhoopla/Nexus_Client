#!/bin/bash

# Copy the Modules, Resources and Core directories, as well as Icon.ico, Nexus.py and requirements.txt to a new directory along with this file.
# Then, run the script.

python3.9 -m venv buildEnv

source buildEnv/bin/activate

python3.9 -m pip install --upgrade -r requirements.txt

python3.9 -m pip install --upgrade pyinstaller

python3.9 -m PyInstaller --clean --icon="./Icon.ico" --noconsole --noconfirm --onedir --windowed --add-data "./Modules:Modules/" --add-data "./Resources:Resources/" --add-data "./Core:Core/" --collect-all "PySide6" --collect-all "networkx" --collect-all "pydot" --collect-all "msgpack" --hidden-import "_cffi_backend" --collect-all "folium" --collect-all "shodan" --collect-all "vtapi3" --collect-all "docker" --collect-all "exif" --collect-all "dns" --collect-all "pycountry" --collect-all "tldextract" --collect-all "requests_futures" --collect-all "branca" --collect-all "bs4" --hidden-import "pandas" --collect-all "docx2python" --collect-all "tweepy" --collect-all "PyPDF2" --collect-all "Wappalyzer" --collect-all "email_validator" --collect-all "seleniumwire" --add-data "./buildEnv/lib/python3.9/site-packages/social-analyzer:social-analyzer/" --hidden-import "PIL" --hidden-import "lz4" --hidden-import "lxml" --hidden-import "jellyfish" --hidden-import "logging"  "./Nexus.py"


deactivate
