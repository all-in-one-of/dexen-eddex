Eddex
=====

The following installation procedure has been developed for windows. 

Installation
------------

* make sure you have Python installed.
* unzip the zip folder anywhere on your hard disk. 
* double-click the setup_env.bat file.

More details
------------

If you want to know what the bat files does, then read on. 

The bat files will set various environment variables. Assuming that $EDDEX is the 
location where you unzipped the folder, and $HFS is the location where Houdini
is installed, then the following paths are added:

For the Windows PATH envioronment variable:
* $HFS/bin
* $EDDEX/bin

For the PYTHONPATH environment variable:
* $EDDEX/python_libs

For the HOUDINI_OTLSCAN_PATH environment variable:
* $HLFS/otls
* &

