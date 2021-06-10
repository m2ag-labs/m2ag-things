#!/usr/bin/env bash
echo "copy $1 to config/thing"
./put_component.sh $1
./put_thing.sh $1
