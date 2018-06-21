from discord import Message


def is_private(message: Message):
    return message.channel.is_private
