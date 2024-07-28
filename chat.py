
import time
import typing
import openai

import dearpygui.dearpygui as dpg
import conparser.conparser as cp


openai.api_key = cp.config['SETTINGS']['openaiapikey']

class Status:
    running = False

class ChatHandler(cp.ConLogEventHandler):
    def on_any_event(self, event):
        super().on_any_event(event)
        print(self.game)
        print(self.logfile_path)
        print(event)


    def on_modified(self, event):
        super().on_modified(event)
        print(self.logfile_path)
        print(event)

        if not event.is_directory:

            with open(self.logfile_path, 'rb') as logfile:
    
                username, message = cp.parse_log(game=self.game, line=cp.rt_file_read(logfile))
                if cp.BLACKLISTED_USERNAME != username: 
                    cp.sim_key_presses(cp.openai_interact(username, message))





def set_status(sender, app_data, user_data):
    if Status.running == False:
        dpg.configure_item("start_button", label="Stop")
        dpg.set_value(user_data, "Running: True")

        file=open(cp.CON_LOG_FILE_PATH, 'r')
        chat_handler = ChatHandler(cp.detect_game())
        chat_handler.logfile_path = cp.CON_LOG_FILE_PATH
        cp.observer.schedule(chat_handler, cp.CON_LOG_FILE_PATH)
        cp.observer.start()

    elif Status.running == True:
        dpg.configure_item("start_button", label="Start")
        dpg.set_value(user_data, "Running: False")

    Status.running = not Status.running


def save_config(sender, app_data, user_data):
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

# TODO: reuse for win support?
def get_logfile() -> typing.BinaryIO:
    if cp.config['SETTINGS']['gameconlogpath']:
        logfile = open(cp.CON_LOG_FILE_PATH, encoding='utf-8')
        return logfile
    return None


def main():
    logfile = None
    game = cp.detect_game()

    dpg.create_context()
    dpg.create_viewport(title='Chat-Strike', width=600, height=300)

    with dpg.window(label="Chat-Strike", width=600, height=300, tag="Chat-Strike"):
        detected_game_text_control = dpg.add_text(f"Detected game: {game}")
        
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


    while dpg.is_dearpygui_running():
        game = cp.detect_game()
        dpg.set_value(detected_game_text_control, game)
        

        dpg.render_dearpygui_frame()
    
    if logfile:
        logfile.close()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
