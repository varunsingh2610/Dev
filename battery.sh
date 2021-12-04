#!/bin/bash
while true
    do
        export DISPLAY=:0.0
        battery_level=`acpi -b | grep -P -o '[0-9]+(?=%)'`
        if on_ac_power; then                                #check if AC is plugged in
            if [ $battery_level -ge 99 ]; then              #check if the battery level is over 90%
                notify-send -u critical "Please unplug your AC adapter" "Battery level: ${battery_level}% (charged above 90%)" -i battery-full-charged
             fi
        fi
      sleep 300                                             #wait for 300 seconds before checking again

    done
