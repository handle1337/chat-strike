
import conparser as cp
import openai

openai.api_key = cp.config['SETTINGS']['openaiapikey']

def openai_interact(user: str, message: str, content="You are an uwu egirl, limit responses to 120 characters"):
    message = f"I'm {user}, {message}"

    messages = [{"role": "system", "content": content}, {"role": "user", "content": message}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content
    return reply

def main():
    username = ""
    message = ""

    game = cp.detect_game()
    print(game)

    with open(cp.CON_LOG_FILE_PATH, encoding='utf-8') as logfile:
        logfile.seek(0, 2)  # Point cursor to the end of console.log to retrieve latest line
        while True:
            line = cp.rt_file_read(logfile)
            if not line:
                continue
            print(line) # Print each new line
            username, message = cp.parse_log(game, line)
            
            if username and message:
                print(f"[DEBUG] {username}: {message}:")
                # This way we prevent chat-gpt from talking to itself
                if cp.BLACKLISTED_USERNAME != username: 
                    cp.sim_key_presses(openai_interact(username, message))


if __name__ == "__main__":
    main()
