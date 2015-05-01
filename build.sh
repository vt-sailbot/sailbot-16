#!/bin/bash

print_message() {
	echo '\033[36m\033[1m'$1'\033[0m\033[39m'
}

print_message 'Starting SailBOT Build Script...'

print_message 'Updating Raspberry Pi...'
sudo apt-get update

print_message 'Installing Python 3, GPSD, and I2C Dependencies...'
sudo apt-get install build-essential python3-dev gpsd gpsd-clients python-gps i2c-tools python-smbus python3-pip

print_message 'Refreshing packages...'
sudo apt-get update

print_message 'Setting up Tornado Web Server...'
sudo pip-3.2 install tornado

print_message 'Pulling project from repository...'
cd ~/
mkdir SailBOT
cd SailBOT
git clone https://github.com/jamestaylr/sailbot.git
