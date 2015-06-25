#!/bin/bash

for x in 8*.bin; do
    mv "$x" "$(echo $x | cut -c2-)"
done
