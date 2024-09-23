sed -n '/<jdbc-store>/,/<\/jdbc-store>/ { /<target>/p }' config.xml


grep -n 'persistent-store' <file> | awk -F: '{print $1+3}' | xargs -I {} sed -n '{}p' <file>


awk '/<jdbc-store>/,/<\/jdbc-store>/ { if ($0 ~ /<target>/) print $0 }' config.xml



#!/bin/bash

# Provided timestamp (replace with the actual timestamp you want to check)
timestamp_to_check=1693592400

# Get the current timestamp
current_timestamp=$(date +%s)

# Calculate the absolute difference in seconds
time_difference=$(( current_timestamp - timestamp_to_check ))

# Use absolute value for the difference
if [ $time_difference -lt 0 ]; then
  time_difference=$(( -time_difference ))
fi

# Check if the difference is within 3 minutes (180 seconds)
if [ $time_difference -le 180 ]; then
  echo "The timestamp is within 3 minutes of the current time."
else
  echo "The timestamp is NOT within 3 minutes of the current time."
fi



