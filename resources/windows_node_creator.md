# How to Host a Whitedot Node on the Windows Operating System.
## Host a Node
1. Prevent your PC from sleeping by going to Settings > System > Power & sleep. Set Sleep to Never for both "On battery power" and "When plugged in" Alternatively, use a utility like Caffeine to keep your PC awake.
2. Download [Python](https://www.python.org/downloads/) if you have not already.
3. Open Command Prompt or PowerShell and run:
```
pip install whitedot
```
4. Run this command inside your terminal:
```
whitedot listen
```
5. Follow the prompts to enter your node details.
6. To keep the node running, just keep the terminal window open. You may close or open your PC.

## Shut Down a Node
1. To stop your node, simply close the terminal window or press Ctrl + C in the terminal.
2. Then, open Settings, Navigate to System > Power & sleep. Under Sleep, change the dropdown menus for:

- On battery power, PC goes to sleep after:

- When plugged in, PC goes to sleep after:

- Choose a time you prefer (e.g., 15 minutes, 30 minutes, or any time interval), or select Never if you want it to stay awake.
3. That's it! You can host the node again from "Host a Node"'s step 4.
