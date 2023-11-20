# chat-strike

Inspired by Isaac Duarte's https://github.com/Isaac-Duarte/source_cmd_parser this script integrates chat-gpt into Counter-Strike 2 allowing people in the same server to interact with it.

## Usage

First, you must enable console logging, to achieve this you can do one of the following:

+ Type the following into the cs2 developer console: ``con_logfile <filename>; con_timestamp 1``

or

+ Add `-condebug` to your cs2 launch options on Steam.

If you used the latter option your path probably looks something like this: ``C:\Program Files\SteamLibrary\steamapps\common\Counter-Strike Global Offensive\game\csgo\console.log``

Now open `config.ini` and set `gameconlogpath` to the appropriate path, there you will also set your in-game username and your openai api key.


## How it works

Very similar to Isaac's framework this script reads the console log file. New entries are parsed and sent to chat-gpt to generate a response which is then sent back in game chat through simulated keystrokes.

Ironically enough this script has not been tested on Linux but it has been on Windows while the opposite is true for Isaac's framework 😂
