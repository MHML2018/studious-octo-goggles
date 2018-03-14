#!/bin/bash

# A quick script to move existing longhistory.csv to another locoation
# and create a blank new csv

mv longhistory.csv historylog-$(date "+%Y%m%dT%H%M%SZ").csv
touch longhistory.csv
