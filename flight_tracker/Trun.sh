#!/bin/bash

SLEEP_TIME=30

while true;
do python FTMain.py;
   sleep $SLEEP_TIME;
   reset;
done
