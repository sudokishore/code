#!/bin/bash

# cond1 && cond2 || cond 3

read -p "Enter your age : " age

[[ $age -ge 18 ]] && echo "Adult" || echo "Minor"
