# Ink2SmartCanvas

Ink2SmartCanvas is an Inkscape extension written in Python that exports SVG to HTML5 Canvas in a flavor that Smart Mobile Studio can handle the data. The extension is based on based on Ink2cavas. It aims on providing a way to ease the creation of Canvas graphics by avoiding writing code by hand through Inkscape drawing interface.

## Project files
* **Ink2SmartCanvas** - This folder holds the project main files:
    * **main.py** - Reads and parse the SVG file, creating objects and calling the respective methods to handle it.
    * **canvas.py** - A class responsible for producing Canvas code.
    * **svg.py** - Abstracts SVG elements parsed by the main.py file.
    * **lib/** - This folder contains some Python modules provided by Inkscape and useful for building extensions. These are being used just for development and testing, so it is recomended in a production enviroment to use the already provided by the system.
* **Ink2SmartCanvas.inx** - A XML file that describes the interface between Inkscape and the extension. It must be put in the */extensions* folder to Inkscape be aware of this extension.

## How to install on Inkscape
If you want a system wide install, put just the file **Ink2SmartCanvas.inx** and the folder **Ink2SmartCanvas** at */usr/share/inkscape/extensions* folder (or similar), if you have permission to do this. Alternatively, you can put the files in the local Inkscape extensions folder:  *$HOME/.config/inkscape/extensions* (or similar).

## How to use:
**Extension**

Open Inkscape file and choose "HTML5 (Smart) Output" option at "Save as" menu.

## Project Map

### TODO
* Add missing path sub-commands
* Refactor and fix style methods error handling
* Masks
* Radial Gradient 
* Group style must prevail over grouped objects
* Linear gradient (initial)
* Clones
* Images
* Patterns

### Working
* Lines, rects, circles, ellipses, paths (partial), text (basic)
* Polylines and polygons
* Basic text attributes support
* Fill and stroke
* Clips (needs more tests :-)
* Transformations (translating, rotating, scaling, etc)
* Iterating through groups and layers