#!/usr/bin/env zsh
# TODO: update host name
echo "copy $1 to thing"
cp "../m2ag-thing-builder/config/available/things/$1.json" "things/$1/$1.json"
cp "../m2ag-thing-builder/device/things/$1.py" "things/$1/$1.py"

