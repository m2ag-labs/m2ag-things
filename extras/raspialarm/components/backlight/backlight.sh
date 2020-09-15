#!/usr/bin/env bash
sudo sh -c 'echo "0" > /sys/class/backlight/soc\:backlight/brightness'
gpio -g mode "$1" pwm
gpio pwmc 1000
gpio -g pwm "$1" 512 #set display to half bright as default
