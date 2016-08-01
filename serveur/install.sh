#!/bin/bash
clear
echo ""
echo "Requirements :"
echo "Use the AMD owner driver"
echo "Use a graphic interface (VNC and KVM work's fine)"
echo ""
echo "What do you want?"
echo "   1) Install GPU API (only for miners)"
echo "   2) Install GETH API (only for master)"
echo ""
read -p "Select an option [1-2]: " OPTION
echo ""

case $OPTION in
	1)
		read -p "Do you want install Ethminer? [y/n] " ETH
		if [ $ETH = "y" ]; then
			echo ""
			echo "Ethereum & Ethminer"
			echo ""
			ETHCURL=$(curl https://install-eth.ethereum.org -L)
			bash <$ETHCURL
			apt-get install -y ethminer
		fi
		echo ""
		echo "GPU API"
		echo ""
		apt-get install -y python3 python3-pip
		python3 -m pip install subprocess locale requests bottle json socket netifaces datetime
		wget https://raw.githubusercontent.com/CamTosh/Ethereum/master/serveur/geth.py
		echo ""
		echo "Installation is finished"
		echo "Launch script with : python3 gpu.py"
		echo ""
		read -p "Do you want overclock GPU? [y/n]" OC

		if [ $OC = "y" ]; then

			aticonfig --od-enable --adapter=all
			echo "Overclocking enable"

			read -p "MaxClock? (mHz)" MAXCLOCK
			read -p "MaxMem? (mHz)" MAXMEM
			read -p "FanSpeed? (%)" FANSPEED

			aticonfig --pplib-cmd "set fanspeed 0 $FANSPEED" --adapter=all
			amdconfig --odsc=$MAXCLOCK,$MAXMEM --adapter=all

			echo "The Fan Speed of card(s) is/are fixed to $FANSPEED"
			echo "The Card(s) is/are overclocked"
			echo "   Max clock : $MAXCLOCK"
			echo "   Max mem : $MAXMEM"
		else
			echo ""
			echo "It\'s great to stay calm"
			echo ""
		fi

	;;
	2)
		read -p "Do you want install Geth? [y/n]" GETH
		if [ $GETH = "y" ]; then
			echo ""
			echo "Ethereum & Geth"
			echo ""
			GETHCURL=$(curl https://install-geth.ethereum.org -L)
			bash <$GETHCURL
			apt-get install -y ethminer
		fi
		echo ""
		echo "GETH API"
		echo ""
		apt-get install -y python3 python3-pip
		python3 -m pip install eth_rpc_client subprocess requests bottle netifaces json socket datetime
		wget https://raw.githubusercontent.com/CamTosh/Ethereum/master/serveur/geth.py
		echo ""
		echo "Installation is finished"
		echo "Launch script with : python3 geth.py"
		echo ""
	;;
esac
read -p "Do you want install OpenSSh Server & X11VNC Server? [y/n] " OPSSH
if [ OPSSH = "y" ]; then
	echo ""
	echo "OpenSSH & X11VNC"
	echo ""
	apt-get install -y openssh-server
	apt-get install -y x11vnc
fi
echo "For more information check the readme file (only in french)"
exit 0;
