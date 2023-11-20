
import time
import configparser
import openai
import keyboard

config = configparser.ConfigParser()

config.read('config.ini', encoding='utf-8') 


MY_USERNAME = config['SETTINGS']['username']
CS2_LOG_FILE_PATH = config['SETTINGS']['gameconlogpath']
openai.api_key = config['SETTINGS']['openaiapikey']




def openai_interact(user: str, message: str, content="You are an intelligent assistant, limit your responses to 120 characters."):

    message = f"I'm {user}, {message}"

    messages = [ {"role": "system", "content": content} ]
    messages.append( 
        {"role": "user", "content": message}, 
    )
    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    )
    reply = chat.choices[0].message.content 
    return reply


#really hacky but it works
def parse_log(line: str):
    if "!r" not in line:
        if "[ALL]" in line:
            split_log = line.partition("[ALL] ")[2].split(": ")
            username = split_log[0].replace(u'\u200e', '') # This gets rid of the 'LEFT-TO-RIGHT MARK' char.
            message = split_log[1]
            # This way we prevent chat-gpt from talking to itself
            if MY_USERNAME != username:
                print(f"[CS2FUN-DEBUG] (user){username}: (message){MY_USERNAME}:")
                return split_log
            
    if "Source2Shutdown" in line:
        exit()

    return None
    

def rt_file_read(file: __file__):
    # Reads console.log in real time 
    line = file.readline()
    
    if not line:
        time.sleep(0.1)
    
    return line


def sim_key_presses(text: str):
    keyboard.press_and_release('y')
    time.sleep(0.1)
    keyboard.write(text)
    time.sleep(0.1)
    keyboard.press_and_release('enter') 

def main():
    username = ""
    message = ""
    with open(CS2_LOG_FILE_PATH, encoding='utf-8') as logfile:
        logfile.seek(0, 2) # Point cursor to the end of console.log to retrieve latest line
        while True:
            line = rt_file_read(logfile)
            if not line:
                continue
            print(line)
            parsed_log = parse_log(line)
            if parsed_log:
                username = parsed_log[0]
                message = parsed_log[1]
                sim_key_presses(openai_interact(username, message))

if __name__ == "__main__":
    main()