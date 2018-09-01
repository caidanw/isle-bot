#!/usr/bin/env bash
BOTID=`cat .bot_pid`

kill -CONT ${BOTID}
printf "Resumed Isle-Bot\n\tPID: $BOTID\n"