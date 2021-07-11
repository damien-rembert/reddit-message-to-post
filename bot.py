#!/usr/bin/env python3
import praw
import time
import os

client_id = os.environ['IDCLIENT']
client_secret = os.environ['SECRETCLIENT']
password = os.environ['MDP']
username = os.environ['NOM']


while True:
    reddit = praw.Reddit(
    client_id,
    client_secret,
    password,
    user_agent="***REMOVED***",
    username,
    )
    # go through unread mail
    for message in reddit.inbox.unread(mark_read=False, limit=None):
        # get sender name
        redditor1 = message.author
        # get redditor karma
        redditorKarma = redditor1.link_karma
        # set minimum karma needed
        minKarma = 50
        redditorIsTrusted = False
        print(redditorIsTrusted)
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            # print(f"User: {user.name}")
            if redditor1 == user.name:
                redditorIsTrusted = True
        print(redditorIsTrusted)
        # sender does not have enough karma
        if redditorKarma < minKarma:
            message.mark_read()
        # if the message is not a comment reply
        if message.was_comment:
            message.mark_read()
        else:
            # do stuff with the message/parse message
            title = message.subject
            body = message.body
            # admins can trust/untrust/block/unblock
            if title == "Testoune" and redditorIsTrusted:
                message.reply("recognised title as testoune and redditor is trusted")
            if title == "Testoune" and redditorIsTrusted:
                message.reply("recognised title as testoune")
            if title == "Testoune" and redditorIsTrusted:
                message.reply("redditor is trusted")
            if title == "Trust" and redditorIsTrusted:
                reddit.redditor(body).trust()
            if title == "Untrust" and redditorIsTrusted:
                reddit.redditor(body).untrust()
            if title == "Block" and redditorIsTrusted:
                reddit.redditor(body).block()
            if title == "Unblock" and redditorIsTrusted:
                reddit.redditor(body).unblock()
            else:           
                reddit.subreddit("***REMOVED***").submit(title, url=body)
                message.mark_read()
    # sleep one minute
    time.sleep(60)
    # time.sleep(900)

