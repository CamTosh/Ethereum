![Dashboard](panel.png)


# Quelques commandes : 

## Sur le serveur : 
```
geth --rpc --rpcaddr adresseIpDeVotreServeur --rpcport lePort console
```
Lance le serveur Geth avec un accés console.

## Sur les machines (possédent 4 CG) :

```
ethminer -G --opencl-device 0,1,2,3 --no-precompute -F ip:portDuServeurGeth
```
Lance ethminer sur les 4 cartes graphiques sur le serveur Geth. Si ça ne fonctionne pas il faut lancer ethminer sur 4 terminal différents avec à chaque fois un device différents.

# API

> python3 api.py

## Require

- Python 3
	- eth_rpc_client 
	- subprocess
	- locale
	- re
	- requests
	- sys
	- os
	- bottle
	- json
	- socket
	- netifaces

## Exemple Json

```Json
{
	CurrentClock: "1100",
	Name: "MiningRig001",
	Uptime: "1 day, 0:02:12.990000",
	MaxClock: "1100",
	Load: "100",
	FanSpeed: "100",
	Heat: "81",
	MaxMem: "1500",
	Euro: "541.38",
	Information: " Adapter 0 - Supported device 67B1 Core (MHz) Memory (MHz) Current Clocks : 1100 1500 Current Peak : 1100 1500 Configurable Peak Range : [300-1500] [150-2000] GPU load : 100% ",
	Ip: "10.42.69.42",
	CurrentMem: "1500",
	Balance: 42694269420000000000,
	Hash: 127810954
}
```
