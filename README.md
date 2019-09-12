TF2-Player-Finder
================================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a python script which notifies you (it shows it in the console window.) If there are any players on your current TF2 server, which are contained within the `player_list.txt`.
By default you can check for that using the F9 key in TF2. But you can also change the script file (the `main.py`) to use any other key.

This was made to support multiple platforms, but only windows was actually tested.

To add players about which you want to be notified just add their `steamID64` to the `player_list.txt` as a new line.

This application needs to find your TF2 installation, to do that it just needs Steam as a currently running process.

The by default list is a list of "cheaters" because my friend wanted to quickly check if any cheater (of the ones he encountered before) is on the current server. 
This method isn't dependant on player name or avatar so it is quicker than manually checking all players.

The script should automatically also close when you close TF2.

## Installation

* Download this as zip and extract it to the folder where you want it to be
* Get Python (>=3.3)
* If you are using a macOS/Linux system where `python` is by default python 2.x, replace `python` with `python3`. Also instead of creating a .bat file, create a .sh file.
* Install dependencies using `python -m pip install -r requirements.txt`.
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Enjoy

## Screenshot

Adding myself to the list, starting up the script for the first time, starting TF2 and then joining a random server and pressing F9 looks like this:

![Preview](https://i.imgur.com/ppvNn8j.png)

## Changelog

/

## Planned Features

/


