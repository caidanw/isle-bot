echo "Starting Isle-Bot"
nohup pipenv run python3.6 isle_bot.py >> logs.txt & BPID=$(echo $!)
printf "Isle-Bot started successfully\n\tPID: $BPID\n"
echo $BPID > .bot_pid
