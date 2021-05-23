#!/usr/bin/env zsh
# TODO: update host name
echo "copy $1 to config"
cp "../m2ag-thing-builder/config/available/components/$1.json" "components/$1/$1.json"
cp "../m2ag-thing-builder/device/hardware/components/$1.py" "components/$1/$1.py"
