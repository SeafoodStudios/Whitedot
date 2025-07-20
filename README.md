# Whitedot
Whitedot is an open source, minimalistic and democratized cryptocurrency. It is mostly experimental, to show that cryptocurrencies can be a semi-centralized under a trusted authority to ensure a more connected community and simpler networking.

## How it Works
Whitedot works by a series of steps. It has a semi-centralized server, which does not have the abillity to cheat the blockchain. It also has nodes, to ensure everything is fair. The steps go like this:
1. Node creates its keys, and submits them to the server.
2. The server recieves them, and delays it for a bit to protect against spam bots and accepts the keys if they are valid.
3. The node then may submit blocks, or listen for opportunities to vote.
4. Submitting blocks is like transfering money. This is done by sending a new block, connected to the blockchain to the server.
5. The server then recieves the block, and adds it to the mempool (mempool is the memory pool, which is the podium, or relay for voting between nodes) if there is space.
6. The listening nodes then vote back to the server.
7. The server will count the votes when there has been enough votes, and the server will either add it to the global blockchain, or reject it.
8. The nodes can read the blockchain by replaying the entire chain of connected blocks (connected by the last block's hash). The can also detect tampering by he server.
9. If tampering of the server occurs, the nodes will essentially rebel, and not work anymore.
10. Older versions of the blockchain are always saved by the nodes in case of tampering, so that theoretically, they can manually build a new server.

## Download
To download Whitedot, run this:
```
pip3 install whitedot
```
Documentation for the commands will be added soon. If you want some documentation or you want to test it out, run this after downloading:
```
whitedot info
```
