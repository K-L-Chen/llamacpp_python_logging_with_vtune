#!/bin/bash

#concat the log file name, current date (YearMonthDayHourMinute)
#check "man date" for details
dt=$(date +"%Y%m%d%H%M")
fullfile="log_token_use_""${dt}"".log"

echo "Saving to: $fullfile"

if test -f "./main.log"
then
	echo "main.log found! Condensing..."
	grep "time =" main.log > $fullfile
else
	echo "main.log does not exist!"
fi