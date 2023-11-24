import time
import configparser
import openai
import keyboard
import psutil

config = configparser.ConfigParser()
CONFIG_FILE_PATH = 'config.ini'

config.read(CONFIG_FILE_PATH, encoding='utf-8')

MY_USERNAME = config['SETTINGS']['username']
CON_LOG_FILE_PATH = config['SETTINGS']['gameconlogpath']
openai.api_key = config['SETTINGS']['openaiapikey']


def detect_game(custom_proc=None):
    pname = None
    for proc in psutil.process_iter():
        pname = proc.name()
        match pname:
            case "hl.exe":
                pname = "hl"
                break
            case "hl2.exe":
                pname = "hl2"
                break
            case "cs2.exe":
                pname = "cs2"
                break
            case custom_proc:
                pname = pname.strip(".exe")
    return pname


def openai_interact(user: str, message: str, content="You are an uwu egirl, limit responses to 120 characters"):
    message = f"I'm {user}, {message}"

    messages = [{"role": "system", "content": content}, {"role": "user", "content": message}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content
    return reply


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
            if "[DEAD]" in line:
                parsed_log = parsed_log[0].replace(" [DEAD]", '')
            if "!r" not in line:
                if "[ALL]" in line:
                    parsed_log = line.partition("[ALL] ")[2].split(": ")
                if "[TEAM]" in line:
                    parsed_log = line.partition("[TEAM] ")[2].split(": ")

     
        case "hl":
            if ": " in line:
                parsed_log = line.split(": ")
                parsed_log[0] = parsed_log[0][1:] # For some reason usernames start with '☻' in this game, probably unicode fuckery.

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





def rt_file_read(file: __file__):
    # Reads console.log in real time 
    line = file.readline()

    if not line:
        time.sleep(0.1)

    return line


def sim_key_presses(text: str):
    keyboard.press_and_release('y')
    time.sleep(0.01)
    keyboard.write(text)
    time.sleep(0.01)
    keyboard.press_and_release('enter')


