#!/bin/bash
sudo python3 ioPlayer.py -d /dev/xvdb -s 193273528320 -r r1.csv -tc -tf ./Exchange-Server-Traces/Exchange/Exchange.12-12-2007.02-39-PM.trace.csv
sudo python3 ioPlayer.py -d /dev/xvdb -s 193273528320 -r r1.csv -tc -tf ./Exchange-Server-Traces/Exchange/Exchange.12-12-2007.02-54-PM.trace.csv
sudo python3 ioPlayer.py -d /dev/xvdb -s 193273528320 -r r1.csv -tc -tf ./Exchange-Server-Traces/Exchange/Exchange.12-12-2007.03-09-PM.trace.csv
sudo python3 ioPlayer.py -d /dev/xvdb -s 193273528320 -r r1.csv -tc -tf ./Exchange-Server-Traces/Exchange/Exchange.12-12-2007.03-24-PM.trace.csv
sudo python3 ioPlayer.py -d /dev/xvdb -s 193273528320 -r r1.csv -tc -tf ./Exchange-Server-Traces/Exchange/Exchange.12-12-2007.03-39-PM.trace.csv