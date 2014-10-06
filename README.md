# Lark
Lark is a menu that launches programs. It is designed to be the glue for a custom multi game arcade cabinet. 

## Usage
Lark is written using pygame and python 2.7 so they need to be installed. On linux use `sudo pip install pygame` or for windows find a friendly installer for pygame at http://www.pygame.org/download.shtml. Lark can be launched with `python menu.py games.json` where games.json is the json file containing the data to be used by the menu. templategames.json and examplegames.json are provided as samples. Any value can be left with empty quotes ("") but every game entry must have all the data keys (eg. "Name" and "Year") even if they are not filled out. This helps ensure a contract that keeps the data display for every game consistent. The "Screenshot" key expects a path to a png. This can be relative to menu.py or absolute. If the file is not found the path will be displayed. The "exe" key is the command to launch a game. The value is executed just as if it were typed in a terminal. 

It is recommended to have a games directory that has a directory for each game containing the screenshot and, if the game isn't installed, the game.
