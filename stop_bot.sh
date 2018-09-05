#!/usr/bin/env bash
if [ "$1" == "-d" ]; then
    echo "Logging out Isle-Bot | dev-build"
    bash discord.sh --webhook-url `cat webhooks_discord/dev_webhook_url` --text "?create"
    bash discord.sh --webhook-url `cat webhooks_discord/dev_webhook_url` --text "?logout"
    echo "Logged out Isle-Bot | dev-build"
else
    echo "Logging out Isle-Bot"
    bash discord.sh --webhook-url `cat webhooks_discord/webhook_url` --text "?create"
    bash discord.sh --webhook-url `cat webhooks_discord/webhook_url` --text "?logout"
    echo "Logged out Isle-Bot"
fi