# MacOS Guide for Creating a 24/7 Node on the Whitedot Network
## Host a Node
1. Download [Amphetamine](https://apps.apple.com/us/app/amphetamine/id937984704) if you don't have it yet.
2. Download Homebrew if you don't have it yet by running this command in your Terminal app:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
3. Now, install tmux by running this in your Terminal app:
```
brew install tmux
```
3. Now, if you have not installed Python yet, please install [it](https://www.python.org/downloads/).
4. If you have not installed Whitedot yet, run this:
```
pip3 install whitedot
```
5. To set up the process, run this:
```
tmux new -s whitedot
```
6. It will then show an editor, and you should type this command into it:
```
whitedot listen
```
7. Enter the details Whitedot asks for.
8. You can now keep the program running, by type Control + B, and then press D.
9. Remember to monitor your laptop's heating and place it in a dry, ventilated place to ensure it does not break.

## Shut Down a Node
1. If you would like to shut down your node, run this first in your Terminal app:
```
tmux attach -t whitedot
```
2. Then, press Control + C, and type "exit" and press return into the text terminal prompt. You may now close the Terminal window.
3. That's it! You can set up the node again by starting from "Host a Node"'s 5th step.
