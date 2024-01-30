#!/bin/bash

mkdir BehaviorTree.cpp
cd BehaviorTree.cpp
git clone https://github.com/BehaviorTree/BehaviorTree.CPP 
mkdir build
cd build
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install conan
conan profile detect
conan install ../BehaviorTree.CPP --output-folder=. --build=missing
cmake ../BehaviorTree.CPP -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"
cmake --build . --parallel
