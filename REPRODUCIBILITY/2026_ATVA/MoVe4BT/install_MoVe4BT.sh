#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install git make cmake gcc-11 g++-11 -y

sudo apt-get install libzmq3-dev libboost-dev qtbase5-dev libqt5svg5-dev libdw-dev qtwebengine5-dev qtpositioning5-dev mono-complete -y
sudo apt-get install libncurses-dev build-essential -y
git clone --branch v3.8 https://github.com/BehaviorTree/BehaviorTree.CPP.git
cd BehaviorTree.CPP
mkdir build
cd build
cmake ..
make -j8
sudo make install

cd ~
git clone https://github.com/Huangps/MoVe4BT.git
