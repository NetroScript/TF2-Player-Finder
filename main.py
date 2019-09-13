import psutil
import os
import re
import time
import json


steampath = ""
steamlibraries = []
tf2_path = ""
known_players = []

def tf2_steam_id_to_id64(usteamid):
    return int(usteamid) + 76561197960265728


def setup():
    global steampath
    global steamlibraries
    global tf2_path

    print("Getting Steam Path")

    for proc in psutil.process_iter():
        if proc.name() == "Steam" or proc.name() == "Steam.exe":
            steampath = os.path.dirname(proc.exe())

    if steampath == "":
        print("Steam is not running, please start Steam before trying this")
        exit(0)

    print("Found Steam at: " + steampath)

    print("Searching for Steam Games Libraries")

    steamlibraries.append(os.path.join(steampath, "steamapps", "common"))

    with open(os.path.join(steampath, "steamapps", "libraryfolders.vdf")) as file:
        paths = re.findall(r'	"\d+"		"(.+)"', file.read())
        for path in paths:
            path = path.replace("\\\\", "\\")
            steamlibraries.append(os.path.join(path, "steamapps", "common"))

    print("Found the following libraries:")

    for library in steamlibraries:
        print(" * " + library)

    print("Scanning for all installed Steam games")

    for library in steamlibraries:
        subfolders = [f.path for f in os.scandir(library) if f.is_dir()]
        for folder in subfolders:
            game = os.path.basename(folder)
            if game != "Team Fortress 2":
                print("Found game - " + game)
            else:
                print("###############Found Team Fortess###############")
                tf2_path = folder

    print("Found Team Fortress Folder: " + tf2_path)

    settings = {
        "steampath": steampath,
        "steam_libraries": steamlibraries,
        "tf2_path": tf2_path
    }

    with open("./settings", "w") as file:
        json.dump(settings, file)


print("Loading list with known players")

with open("./player_list.txt") as file:
    data = file.readlines()
    for line in data:
        try:
            player = int(line)
            if player > 0:
                known_players.append(player)

        except Exception as e:
            pass

print("Loaded " + str(len(known_players)) + " players of the list")


if os.path.isfile("./settings"):
    try:
        with open("./settings", "r") as file:
            settings = json.load(file)
            steampath = settings["steampath"]
            steamlibraries = settings["steam_libraries"]
            tf2_path = settings["tf2_path"]

            print("Loaded settings file")
    except Exception as e:
        os.remove("./settings")
else:
    print("No settings file found, doing first time setup:")
    setup()



with open(os.path.join(tf2_path, "tf", "cfg", "known_player_check.cfg"), "w") as file:
    file.write('''
echo "Starting Known Player Check Status"
status
echo "Ending Known Player Check Status"''')

config_files = [os.path.join(tf2_path, "tf", "cfg", "autoexec.cfg"), os.path.join(tf2_path, "tf", "cfg", "custom.cfg")]
exists = 0




for config_file in config_files:
    if os.path.isfile(config_file):
        exists+=1

        with open(config_file, "r+") as file:
            config = file.read()
            config = re.sub(r"\n\n\/\/##########################TF2KPC_B.+\/\/##########################TF2KPC_E", "", config, 0, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            config += """
//##########################TF2KPC_B
//Please do not change any of this - This was added by TF2KnownPlayerCheck
log on
con_logfile "console.log"
bind F9 "exec known_player_check"
//##########################TF2KPC_E
"""
            file.seek(0)
            file.write(config)

scan_log = os.path.join(tf2_path, "tf", "console.log")

if not os.path.isfile(scan_log):
    open(scan_log, 'a').close()

if not os.path.isfile("./linecount"):
    with open("./linecount", "w") as file:
        file.write(str(sum(1 for line in open(scan_log, encoding="utf8", errors='ignore'))))

started_at_line = 0

errored = False

with open("./linecount", "r") as file:
    try:
        started_at_line = int(file.read())
    except Exception as e:
        errored = True


if errored:
    print(
        "Exception happened while reading the line count, it was deleted, restart the application to"
        " try again and to regenerate it")
    os.remove("./linecount")
    exit(0)

read_to_line = 0

player_regex = re.compile("^#\s+\d+\s+?\"(.*)\"\s+\[U:1:(\d+)\]")


keep_running = True

print("Starting to parse log file")

with open(scan_log, encoding="utf8", errors='ignore') as f:
    started_status = False
    buffer = []
    read_number_of_lines = 0
    while keep_running:
        line = f.readline()
        read_to_line+=1
        if line:

            if read_to_line > started_at_line:

                if line.startswith("Shutdown function"):
                    with open("./linecount", "w") as file:
                        file.write(str(read_to_line))
                    print("TF2 closed, so we are also exiting the program c:")
                    keep_running = False

                elif started_status:
                    read_number_of_lines+=1
                    # Additional sanity check for the case of the commands not being executed in the correct order
                    if (line.startswith("Ending Known Player Check Status") and read_number_of_lines > 9) or read_number_of_lines >= 100:
                        started_status = False
                        read_number_of_lines = 0

                        # Do stuff
                        for player in buffer:
                            result = re.match(player_regex, player)
                            if result:
                                id = tf2_steam_id_to_id64(int(result.group(2)))

                                if id in known_players:
                                    print("Found Known Player: ")
                                    print(result.group(1) + " | (" + str(id) + ")")
                            else:
                                if player.startswith("map"):
                                    print("Current Map: " + player.split(": ")[1].split(" at")[0])

                        buffer = []
                    else:
                        buffer.append(line)

                elif line.startswith("Starting Known Player Check Status"):
                    started_status = True
        else:
            time.sleep(0.1)
