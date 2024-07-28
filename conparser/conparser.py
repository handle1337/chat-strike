import time
import os
import configparser
import typing
import keyboard
import psutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent

observer = Observer()

class ConLogEventHandler(FileSystemEventHandler):
    def __init__(self, game: str = ''):
        super().__init__()

        self.game: str = game
        self.logfile_path: str = None

        def on_any_event(self, event: FileSystemEvent) -> None:
            super().on_any_event(event)

        def on_modified(self, event: FileSystemEvent) -> None:
            super().on_modified(event)



# doesnt work on linux for some reason
    # def on_modified(self):
    #     print("modified")
    #     if self.logfile:
                    
    #         line = rt_file_read(self.logfile)

    #         username, message = parse_log(self.game, line)
    #         print(f"LINE: {line} USER: {username} MSG: {message}")



config = configparser.ConfigParser()
CONFIG_FILE = 'config.ini'

config.read(CONFIG_FILE, encoding='utf-8')

BLACKLISTED_USERNAME = config['SETTINGS']['username']
CON_LOG_FILE_PATH = config['SETTINGS']['gameconlogpath']
CHAT_KEY = config['SETTINGS']['chatkey']



def detect_game(custom_proc="customproc"):
    pname = None
    for proc in psutil.process_iter():
        match proc.name():
            case "hl.exe":
                pname = "hl"
                break
            case "hl2.exe":
                pname = "hl2"
                break
            case "cs2.exe":
                pname = "cs2"
                break
            case _:
                if proc.name() == custom_proc:
                    pname = custom_proc.strip(".exe")
                    break
                else:
                    continue
    return pname


# really hacky but it works
def parse_log(game, line: str):
    """
    Parses source console logs, if it detects

    Args:
        game (str): Specifies the game as to use the appropriate format
        line (str): String fetched from the source console log to parse

        Returns:
            list: In-game username (index 0), and message (index 1) 

    """


    if "Source2Shutdown" in line:
        exit() #TODO: make this optional

    parsed_log = ["",""]
    username = ""
    message = ""
    match game:
        case "cs2":
            if "[ALL]" in line:
                parsed_log = line.partition("[ALL] ")[2].split(": ")
            if "[TEAM]" in line:
                parsed_log = line.partition("[TEAM] ")[2].split(": ")
            if "[DEAD]" in line:
                parsed_log[0] = parsed_log[0].replace(" [DEAD]", '')
                print(f"DEAD {parsed_log}")


     
        case "hl":
            if ": " in line:
                parsed_log = line.split(": ")
                parsed_log[0] = parsed_log[0][1:] # For some reason usernames start with '☻' in this game, probably some weird unicode thing.

        case "hl2":
            if "*DEAD*" in line:
                parsed_log = line.replace("*DEAD* ", '')
            if " : " in line:
                parsed_log = line.split(" :  ")

        case _:                                                                         
            return None   

    username = parsed_log[0]
    username = username.replace(u'\u200e', '')  # This gets rid of the 'LEFT-TO-RIGHT MARK' char.
    
    message = parsed_log[1]
    
    return [username, message]





def rt_file_read(file: typing.BinaryIO):
    # Reads console.log in real time 
    try:  # catch OSError in case of a one line file 
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
    except OSError:
        file.seek(0)

    return file.readline().decode()


def sim_key_presses(text: str):
    keyboard.press_and_release(CHAT_KEY)
    time.sleep(0.01)
    keyboard.write(text)
    time.sleep(0.01)
    keyboard.press_and_release('enter')


