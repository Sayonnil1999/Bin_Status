#!/bin/bash
while true
do
    if [[ "$(pgrep python | wc -l)" -eq 0 ]]; then
        echo "Starting sensors...."
        python /home/pi/Desktop/iot/run.py
    else
        echo "Already running"
    fi
    sleep 5
done
