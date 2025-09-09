#!/bin/bash

for i in {1..100}; do
    let var=$i%2
    if [[ var -eq 0 ]]; then
        echo -n "$i "
    fi
done
