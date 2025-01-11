#! /bin/bash

repo_root_dir=$(git rev-parse --show-toplevel)
version=$(cat $repo_root_dir/VERSION)

echo "This script will installing raspi-rack-frontpanel@$version"
ans=$(read -p "Continue? (y/n)")

if [[ "$ans" -eq "y" ]]; then
#     echo "Updating packages..."
#     sudo apt-get update &&
#     sudo apt-get upgrade -y &&
#     echo ""
fi

echo "Done."