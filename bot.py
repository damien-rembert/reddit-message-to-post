#!/usr/bin/env python3
import praw
import time


while True:
    reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    password="***REMOVED***",
    user_agent="***REMOVED***",
    username="***REMOVED***"
    )

    # go through unread mail
    for message in reddit.inbox.unread(mark_read=False, limit=None):
        # TODO block user when asked by authorised user
        # TODO if sender has enough karma
        # get sender name
        redditor1 = message.author
        # get redditor karma
        redditorKarma = redditor1.link_karma
        minKarma = 50
        redditorIsTrusted = False
        print(redditorIsTrusted)
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            print(f"User: {user.name}")
            if redditor1 == user.name:
                redditorIsTrusted = True
        print(redditorIsTrusted)
        # sender does not have enough karma
        if redditorKarma < minKarma:
            message.mark_read()
            break
        # if the message is not a comment reply
        if message.was_comment:
            message.mark_read()
            break
        else:
            # do stuff with the message/parse message
            title = message.subject
            body = message.body
             # admins can trust/untrust/block/unblock
            if title == "Trust" and redditorIsTrusted:
                reddit.redditor(body).trust()
                break
            if title == "Untrust" and redditorIsTrusted:
                reddit.redditor(body).untrust()
                break
            if title == "Block" and redditorIsTrusted:
                reddit.redditor(body).block()
                break
            if title == "Unblock" and redditorIsTrusted:
                reddit.redditor(body).unblock()
                break
            else:           
                reddit.subreddit("***REMOVED***").submit(title, url=body)
                message.mark_read()
                break
    # sleep one minute
    time.sleep(60)
    # time.sleep(900)

