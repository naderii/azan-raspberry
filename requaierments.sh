#!/bin/bash

# Install required packages
sudo apt-get update
sudo apt-get install -y vim wget tar htop telnet tcptraceroute mtr bash-completion chrony python3 python3-venv

# Create and activate the virtual environment
python3 -m venv env
source env/bin/activate

# Install Python packages
pip3 install csv
pip3 install os
pip3 install random
pip3 install datetime
pip3 install pygame
pip3 install time
pip3 install daemonize
pip3 install praytimes
pip3 install sys
pip3 install psutil

# Navigate to the project directory
cd /home/nader/azan

# Run the Python script
python3 main.py

echo "All required packages have been installed in the virtual environment."
echo "The Python script has been executed."

# Create a systemd service file
sudo tee /etc/systemd/system/azan.service <<EOF
[Unit]
Description=Azan Service
After=network.target

[Service]
ExecStart=/home/nader/azan/env/bin/python3 /home/nader/azan/main.py
Type=oneshot
RemainAfterExit=yes
User=nader
Group=nader
Environment=PATH=/home/nader/azan/env/bin

[Install]
WantedBy=multi-user.target

EOF


# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable azan.service
sudo systemctl start azan.service

echo "The Azan service has been enabled and started."