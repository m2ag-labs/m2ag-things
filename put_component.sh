#!/usr/bin/env bash
# TODO: update host name
echo "copy $1 to config"
cp "components/$1/$1.json" "../m2ag-thing-builder/config/available/components/$1.json"
cp "components/$1/$1.py" "../m2ag-thing-builder/device/hardware/components/$1.py"
