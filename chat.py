
import openai

import dearpygui.dearpygui as dpg
import conparser as cp


openai.api_key = cp.config['SETTINGS']['openaiapikey']

class Status():
    running = False


def set_status(sender, app_data, user_data):
    if Status.running == False:
        dpg.configure_item("start_button", label="Stop")
        dpg.set_value(user_data, "Running: True")

    elif Status.running == True:
        dpg.configure_item("start_button", label="Start")
        dpg.set_value(user_data, "Running: False")

    Status.running = not Status.running


def save_config():
    cp.config['SETTINGS']['username'] = dpg.get_value("username")
    cp.config['SETTINGS']['gameconlogpath'] = dpg.get_value("conlog")
    cp.config['SETTINGS']['chatkey'] = dpg.get_value("chat_keybind")
    with open(cp.CONFIG_FILE, 'w') as configfile:
        cp.config.write(configfile)


def openai_interact(user: str, message: str, content="You are a csgo player, limit responses to 120 characters"):
    message = f"I'm {user}, {message}"

    messages = [{"role": "system", "content": content}, {"role": "user", "content": message}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content
    return reply


def main():
    logfile = None
    username = ""
    message = ""
    game = cp.detect_game()
    print(game)

    

    dpg.create_context()
    dpg.create_viewport(title='Chat-Strike', width=600, height=300)

    with dpg.window(label="Chat-Strike", width=600, height=300, tag="Chat-Strike"):
        dpg.add_text(f"Detected game: {game}")
        
        dpg.add_input_text(hint="Blacklisted username", default_value=cp.BLACKLISTED_USERNAME, tag="username")
        dpg.add_input_text(hint=".log file path", default_value=cp.CON_LOG_FILE_PATH, tag="conlog")
        dpg.add_input_text(hint="Openapi key", default_value=openai.api_key, password=True, tag="openapi_key")
        dpg.add_input_text(hint="Chat keybind", default_value=cp.CHAT_KEY, tag="chat_keybind")

        dpg.add_button(label="Save", callback=save_config)
        status_text = dpg.add_text("Running: False")

        dpg.add_button(label="Start", callback=set_status, user_data=status_text, tag="start_button")



    dpg.set_primary_window("Chat-Strike", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Add, callback=set_status, user_data=status_text)

    if cp.config['SETTINGS']['gameconlogpath'] != None:
        logfile = open(cp.CON_LOG_FILE_PATH, encoding='utf-8')
        logfile.seek(0, 2)

        


    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

        if Status.running == True:
            if logfile:
                
                line = cp.rt_file_read(logfile)
                
                if not line:
                    continue
                print(line)
                username, message = cp.parse_log(game, line)

                if username and message:
                    #print(f"[DEBUG] {username}: {message}:")
                    # This way we prevent chat-gpt from talking to itself
                    print(f"[DEBUG] {cp.BLACKLISTED_USERNAME}: {username}:")
                    if cp.BLACKLISTED_USERNAME != username: 
                        cp.sim_key_presses(openai_interact(username, message))
                else:
                    continue
    
    if logfile:
        logfile.close()
    dpg.destroy_context()








if __name__ == "__main__":
    main()
