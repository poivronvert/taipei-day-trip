#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# 安裝 Python 3.11
echo "安裝 Python 3.11..."

wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
tar xzvf Python-3.11.9.tgz

cd Python-3.11.9
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall

cd ..
rm -rf Python-3.11.9
rm Python-3.11.9.tgz
# 確認安裝成功
echo "確認 Python 版本..."
python3.11 --version
echo "Python 3.11 安裝完成"

# wget https://bootstrap.pypa.io/get-pip.py
# python3.11 ./get-pip-py
# echo "Successfully installed pip"


sudo apt update && sudo apt install mysql-server
# sudo service mysql start
sudo service mysql status


pip3.11 install -r ../requirements.txt

python3.11 ../app/init_table.py


