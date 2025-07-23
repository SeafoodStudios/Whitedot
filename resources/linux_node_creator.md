# How to Create a Node on the Linux Operating System
## Creating the Node
1. Prevent your machine from sleeping or suspend (depends on your distro and desktop environment). For servers, usually no problem.
2. Install Python and pip if you haven’t already. For example, on Ubuntu:
```
sudo apt update
sudo apt install python3 python3-pip
```
3. Install Whitedot if you have not already:
```
pip3 install whitedot
```
4. Install tmux to keep the node running in the background:
```
sudo apt install tmux
```
5. Start a new tmux session with this command:
```
tmux new -s whitedot
```
6. Enter this command in and fill in the prompts:
```
whitedot listen
```
7. Detach with Ctrl + B, then D.

## Shutting the Node Down
1. To shut down a node, attach back to the session:
```
tmux attach -t whitedot
```
2. Then press Control + C and run "exit".
3. Allow your machine to sleep (depends on your distro and desktop environment). For servers, you can usually skip this step.
