#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Need a product id!"
else
    ~/bin/clouddrive.js ls $1 | awk '{$1=$2=$3=$4=$5=$6=$7="";print $0}' | xargs -i ~/bin/clouddrive.js mv "$1/\{}" Apen/$1
fi
