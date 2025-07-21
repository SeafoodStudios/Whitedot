# Whitedot
Whitedot is an open source, minimalistic and democratized cryptocurrency. It is mostly experimental, to show that cryptocurrencies can be a semi-centralized under a trusted authority to ensure a more connected community and simpler networking.

## How it Works
Whitedot works by a series of steps called the Whitedot Protocol. It has a semi-centralized server, which means that one person controls the server, but does not have the ability to cheat the blockchain). The server is like the "government". A blockchain is a chain of blocks, with data in it, connected by a hash (a one way encoding that cannot be decoded) of the previous block. It also has nodes, to ensure everything is fair. The nodes are like the "citizens" of the Whitedot Protocol. The steps go like this:
1. Node creates its keys (keys are a set of important data, basically your "username" and "password", but more cryptographically secure), and submits them to the server.
2. The server receives them, and delays it for a bit to protect against spam bots and accepts the keys if they are valid (the server only accepts verified users).
3. The node then may submit blocks, or listen for opportunities to vote (this is done so that the server cannot cheat the system and give a user a "cheating" amount of money).
4. Submitting blocks is like transferring money. This is done by sending a new block, connected to the blockchain to the server.
5. The server then receives the block, and adds it to the mempool (the mempool is the memory pool, which is the podium, or relay for voting between nodes) if there is space.
6. The listening nodes then vote back to the server.
7. The server will count the votes when there has been enough votes, and the server will either add it to the global blockchain, or reject it.
8. The nodes can read the blockchain by replaying the entire chain of connected blocks. The can also detect tampering by he server.
9. If tampering of the server occurs, the nodes will essentially rebel, and not work anymore.
10. Older versions of the blockchain are always saved by the nodes in case of tampering, so that theoretically, they can manually build a new server.

## Download
1. If you have not already, please download [Python](https://www.python.org/downloads/), because you need the package manager.
2. Now, to download Whitedot, run this in your command line app (for the best experience, we recommend that you go fullscreen):
```
pip3 install whitedot
```
3. Run this command to verify the download. (if it asks you to download the blockchain and repository, it is recommended to accept, although this is not strictly required, this is just a precaution and a backup):
```
whitedot
```
4. Now, run this command to create your account:
```
whitedot create_keys
```
5. Copy the text given and save it safely and securely, the text looks something like this:
```
Saved private key as private_key.der
Saved public key as {really_long_string}
```
6. It is very recommend to download [Encrypto by MacPaw](https://macpaw.com/encrypto). Use this to always encrypt your private key when you are finished using it, and always decrypt the key when you are going to use it. Always keep a backup of your private key somewhere private and secure! The private key is usually located in your home directory, so you may have to do some searching. This may be a bit of a complicated step, so we split it into smaller steps:

- Download [MacPaw's Encrypto](https://macpaw.com/encrypto).

- Drop the private key file into Encrypto, and follow the steps in it to encrypt it.

- If the app leaves behind the unencrypted file, please remove the unencrypted file (SAVED SOMEWHERE ELSE, SAFELY), but keep the encrypted one.

- When you need to do something that requires your private key, decrypt the file using Encrypto, and provide the path.

- That's it! If you don't keep backups, and you lose your private or public key, you won't be able to access your account anymore, so be careful! Never share your private key, only share your public key.

## Command Line Tools
- whitedot transfer

This command allows you to transfer Whitedots with your account.


- whitedot listen

This command listens for any new transactions to be voted for. It is very encouraged you run this indefinitely to contribute to the community, but always monitor your laptop for any signs of wear and/or damage.


- whitedot create_keys

This command create your keys. Your public key is like your 'username' and your private key is like your 'password'. It then submits it to the server to be verified. You keys should be verified in around 1-2 days.


- whitedot get_balance

This command gets the balance, based on the public key you provide.


- whitedot info

This command gives information about the commands. You can also run the command 'whitedot' to do the same thing.

## Thanks
Whitedot is an experimental cryptocurrency, and you should never put too much expectation into it, because it is very fragile and unstable. Please don’t expect full reliability. It is more of a concept, although it is recommended that you contribute by hosting a listening node, because the more nodes there are, the less likely anybody is able to take over. Thanks again!
