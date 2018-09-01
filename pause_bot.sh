#!/usr/bin/env bash
BOTID=`cat .bot_pid`

kill -STOP ${BOTID}
printf "Paused Isle-Bot\n\tPID: $BOTID\n"