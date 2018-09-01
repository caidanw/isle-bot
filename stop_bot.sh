#!/usr/bin/env bash
BOTID=`cat .bot_pid`
HEADER="-----------------------------------------------------------"

kill ${BOTID}
printf "Shutting down Isle-Bot\n\tPID: $BOTID\n"

printf "\n$HEADER\n" >> logs.txt
echo "Appended new lines to logs.txt"

rm .bot_pid
echo "Removed .bot_pid"