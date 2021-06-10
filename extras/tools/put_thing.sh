#!/usr/bin/env bash
# TODO: update host name
echo "copy $1 to thing"
cp "things/$1/$1.json" "../m2ag-thing-builder/config/available/things/$1.json"
cp "things/$1/$1.py" "../m2ag-thing-builder/device/things/$1.py"
