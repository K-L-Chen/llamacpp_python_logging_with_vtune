@echo off
title Condensing output log...

set dt=%DATE:~10,4%%DATE:~7,2%%DATE:~4,2%%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%

IF EXIST main.log (
	echo main.log found! Condensing...
	findstr "timings" main.log > "log_token_use_%dt%.log"
	findstr "." "log_token_use_%dt%.log"
) ELSE (
	echo main.log does not exist!
)
exit 0