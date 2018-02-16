---
title: Getting Started with Eddex
---

# Getting Started with Eddex

Installing Eddex either on a local network or on the Amazon is straight forward and requires minimal configuration.

The following installation procedure has been developed for Sidefx Houdini users on the Windows platform.

## Install Dexen

Before starting with Eddex, you will need to install Dexen.

- [Installing Dexen](http://design-automation.net/dexen)

## Install Eddex

- [Download the zip file from Github](https://github.com/phtj/eddex)
- Unzip the zip folder anywhere on your hard disk.
- Double-click the setup_env.bat file.

Executing the bat file will set various environment variables. Assuming that $EDDEX is the
location where you unzipped the folder, and $HFS is the location where Houdini
is installed, then you can check that the following paths have been added:

For the Windows PATH environment variable:
- `$HFS/bin`
- `$EDDEX/bin`

For the PYTHONPATH environment variable:
- `$EDDEX/python_libs`

For the HOUDINI_OTLSCAN_PATH environment variable:
- `$HLFS/otls`
- `&`

## Nodes in SideFX Houdini

Various nodes will now be available in Sidefx Houdini for running evolutionary optimisation jobs. They will be available on the Tab meny, under 'Eddex'. If Dexen is running, you will be able to execute jobs directly from within Houdini by clicking teh 'Run' button.

## View Dexen Interface

You may also access the Dexen UI through the browser. If you are running Dexen locally, you can access the UI at http://localhost:5000/.
- [Register](http://localhost:5000/register) (Any username and password.)
- [Login](http://localhost:5000/login)
- Start running jobs.
