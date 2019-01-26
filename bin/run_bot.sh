#!/usr/bin/env bash
echo "Starting Isle-Bot"
pipenv run python3.6 isle_bot.py & BPID=$(echo $!)
printf "Isle-Bot started successfully\n\tPID: $BPID\n"
echo ${BPID} > .bot_pid
