#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

for (( i = 0 ; i < 255 ; i+=25 )) ; do
    echo "exit $i" >script.sh

    e=0
    bash-cat -d bash-cat.dat script.sh || e=$?

    [[ $e == $i ]]
done
