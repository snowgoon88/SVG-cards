#!/bin/bash

for fullname in $(ls card*.svg)
do
    echo $fullname
    ext=${fullname##*.}
    filebase=${fullname%.*}
    echo "/usr/bin/inkscape --export-png=$filebase.png -w 140 -h 190 $fullname"
    /usr/bin/inkscape --export-png=$filebase.png -w 140 -h 190 $fullname
done
                    
