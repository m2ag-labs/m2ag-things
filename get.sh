#!/usr/bin/env zsh
# TODO: update host name
echo "copy $1 to config/thing"
./get_component.sh $1
./get_thing.sh $1
