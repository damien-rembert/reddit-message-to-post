#!/usr/bin/env python3
import praw
import time
import os




while True:
    # client_id = os.environ['IDCLIENT']
    # client_secret = os.environ['SECRETCLIENT']
    # password = os.environ['MDP']
    # username = os.environ['NOM']
    # user_agent = "heroku:inmailtopost:v0.1 (by /u/***REMOVED***)"

    reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    password="***REMOVED***",
    user_agent="***REMOVED***",
    username="***REMOVED***"
    )

    # reddit = praw.Reddit(client_id,client_secret,password,user_agent,username)

    # reddit = praw.Reddit(
    # client_id,
    # client_secret,
    # user_agent,
    # username,
    # password,
    # )

    # go through unread mail
    for message in reddit.inbox.unread(mark_read=False, limit=None):
        # get sender name
        sender = message.author
        # get redditor karma
        senderKarma = sender.link_karma
        # set minimum karma needed
        minKarma = 50
        senderIsTrusted = False
        body = ""
        title = ""
        # print(senderIsTrusted)
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            # print(f"User: {user.name}")
            if sender == user.name:
                senderIsTrusted = True
        # print(senderIsTrusted)
        # sender does not have enough karma
        if senderKarma < minKarma:
            message.mark_read()
        # if the message is not a comment reply
        if message.was_comment:
            message.mark_read()
        else:
            # do stuff with the message/parse message
            title = message.subject
            body = message.body
            if title == "Trust" and senderIsTrusted:
                message_content = "body of the message: "
                message_content = body
                message.reply(message_content)
                reddit.redditor(body).trust()
                message.mark_read()
            elif title == "Untrust" and senderIsTrusted:
                reddit.redditor(body).distrust()
                message.mark_read()
            elif title == "Block" and senderIsTrusted:
                reddit.redditor(body).block()
                message.mark_read()
            elif title == "Unblock" and senderIsTrusted:
                reddit.redditor(body).unblock()
                message.mark_read()
            else:           
                reddit.subreddit("***REMOVED***").submit(title, url=body)
                message_content = message_content + body
                message.reply(message_content)                
                message.mark_read()
    # sleep one minute
    time.sleep(60)
    # time.sleep(900)

