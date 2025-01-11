#! /bin/bash

repo_root_dir=$(git rev-parse --show-toplevel)

echo "Setting up development environment..."

echo "Upgrading packages..."
sudo apt-get update &&
sudo apt-get upgrade -y &&

echo "Installing requirements..." &&
sudo apt-get install git wget curl python3-setuptools build-essential &&

echo "Installing pigpio..." &&
