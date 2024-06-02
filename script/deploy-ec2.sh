#!/bin/bash

sudo apt update
sudo apt upgrade -y

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
tar xzvf Python-3.11.9.tgz

cd Python-3.11.9
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall

cd ..
rm -r Python-3.11.9
rm Python-3.11.9.tgz

echo "Successfully installed Python3.11.9"

wget https://pip.pypa.io/en/stable/installation/#get-pip-py
python get-pip-py

cd .. 
rm get-pip.py

echo "Successfully installed pip"

requirements=(
	python-dotenv==1.0.1
	SQLAlchemy==2.0.30
	fastapi==0.111.0
	pydantic==2.7.1
	uvicorn==0.30.0
)

for i in {$requirements[@]};
	sudo pip install $i;
	echo "Successfully installed $i"

python init_db.py


