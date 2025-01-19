#! /bin/bash

repo_root_dir=$(git rev-parse --show-toplevel)
venv_dir=${repo_root_dir}/.pyvenv

echo "Setting up development environment..."

echo "Upgrading packages..."
sudo apt-get update &&
sudo apt-get upgrade -y &&

echo "Installing requirements..." &&
sudo apt-get install -y git wget curl python3-dev python3-venv python3-setuptools build-essential gpiod libgpiod-dev &&

echo "Setting up virtual environment..." &&
python3 -m venv ${venv_dir} &&
source ${venv_dir}/bin/activate &&
python3 -m pip install -r ${repo_root_dir}/requirements.txt &&
${venv_dir}/bin/deactivate &&

echo "Done"
