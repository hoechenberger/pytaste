# pytaste

Taste threshold estimation based on a QUEST algorithm.

## Installation

The software depends on [PsychoPy](http://www.psychopy.org) (which itself 
requires numerous scientific Python packages) and 
[Matplotlib](https://matplotlib.org). Because installation of all required
dependencies is often a non-trivial endeavor, we provide `conda` environment
files for simple installation with the
[Anaconda](https://www.anaconda.com/download/) and
[Miniconda](https://conda.io/miniconda.html) Python distributions.

### Install Anaconda or Miniconda
If you don't have an existing installation of Anaconda or Miniconda, first
download and install one of them. If you are unsure, grab Miniconda, as it
is smaller download and installation. It does not matter whether you get
the 32- or 64-bit version, and both the Python 2.7 and Python 3.6 should work
just fine.

* [Download Miniconda](https://conda.io/miniconda.html)
* [Download Anaconda](https://www.anaconda.com/download/)

Once you have downloaded setup file, run the installer and accept all the
default settings.

### Download `pytaste`

If you haven't done so already, navigate to
[the `pytaste` Github page](https://github.com/hoechenberger/pytaste), click on
*Clone or download*, download the `.zip` file and unpack it, for example to
your desktop.

### Set up a conda environment for `pytaste`
To ensure `pytaste` will behave identically on different systems and you get
all required dependencies, we will now create a new virtual Python environment
just for use with `pytaste`. All dependencies and their exact version numbers
are listed in the environemt files which can be found in the `pytaste/conda`
subdirectory of the main `pytaste` folder you just extracted.
You don't have to deal with this manually, though! We created installation
scripts for Windows and macOS to ease the process.

On Windows, simply double-click on the `install_win.bat` file to execute it.
A console
window should appear and display the progress of the installation. On macOS,
open a terminal, navigate to the `pytaste` installation directory
(e.g., `cd Desktop/pytaste`), and run `./install_macos.sh`.

You are now all set to use the software!

## Run `pytaste`
`pytaste` is simply a Python script that needs to be executed inside the
Python environemt the installer just created. Again, we created convenience
scripts for Windows and macOS to simplify the process. On Windows, 
dobule-click on `run.bat`. On macOS, open a terminal, navigate to the
`pytaste` directory, and run `./run.sh`

That's it!

A window should pop up, asking for participant information. You are now ready
to run the experiment!

## Log files and figures
All log files and threshold estimates will be saved in the `Data` subdirectory
of the `pytaste` folder. Similarly, figures will be saved to the `Figures`
folder.

## Citing
If you publish research based on this software, please cite the following publication:
> Richard Höchenberger & Kathrin Ohla (2017): Rapid Estimation of Gustatory Sensitivity Thresholds with SIAM and QUEST. _Frontiers in Psychology,_ 8:981. https://doi.org/10.3389/fpsyg.2017.00981

