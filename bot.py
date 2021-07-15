#!/usr/bin/env python3
import praw
import time
import os
import re


# TODO automatically mark mods from ***REMOVED*** as Trusted
# TODO replace ***REMOVED*** with ***REMOVED***
# TODO set karma
# TODO login without connection details in source code
# TODO check that the url is on r/france
# TODO define methods using def
# TODO define method report fault to ***REMOVED***
# TODO define method redditor.HasEnoughKarma(amountOfKarmaNeeded)
# TODO define method redditor.IsTrusted() returning bool
# TODO improve fault reporting returning error to ***REMOVED***
# TODO np.reddit.com instead of www.reddit.com
# TODO reply to messages confirming that this should appear on the sub shortly


while True:

    reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    password="***REMOVED***",
    user_agent="***REMOVED***",
    username="***REMOVED***"
    )

    # client_id = os.environ['IDCLIENT']
    # client_secret = os.environ['SECRETCLIENT']
    # password = os.environ['MDP']
    # username = os.environ['NOM']
    # user_agent = "heroku:inmailtopost:v0.1 (by /u/***REMOVED***)"

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
        sender = message.author.name
        # senderSaid = sender + " vient de poster sur r/***REMOVED***"
        # get redditor karma
        senderKarma = sender.link_karma
        # set minimum karma needed
        minKarma = 5000
        senderIsTrusted = False
        body = ""
        title = ""
        message_content = ""
        spacing = " - "
        title = message.subject
        body = message.body
        message_content = "titre: " + title + " - corps: " + body
        # print(senderIsTrusted)
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            # print(f"User: {user.name}")
            if sender == user.name:
                senderIsTrusted = True
        # print(senderIsTrusted)
        # sender does not have enough karma
        if senderKarma < minKarma:
            reddit.redditor("***REMOVED***").message(sender + " n'a pas assez de karma - contrôler et poster", message_content)
            # reddit.subreddit("test").message("TEST", "test PM from PRAW")
            reddit.subreddit("***REMOVED***").message("Karma trop bas, message non posté - " + sender + " vient d'essayer de poster sur r/***REMOVED***", message_content)
            message.mark_read()
        # if the message is not a comment but a reply
        if message.was_comment:
            message.mark_read()
        else:
            # do stuff with the message/parse message
            if title == "Trust" and senderIsTrusted:
                try:
                    reddit.redditor(body).trust()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT TRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            elif title == "Distrust" and senderIsTrusted:
                try:
                    reddit.redditor(body).distrust()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT DISTRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
                # reddit.redditor(body).distrust()
                # message.mark_read()
            elif title == "Block" and senderIsTrusted:
                try:
                    reddit.redditor(body).block()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT BLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
                # reddit.redditor(body).block()
                # message.mark_read()
            elif title == "Unblock" and senderIsTrusted:
                try:
                    reddit.redditor(body).unblock()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT UNBLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
                # reddit.redditor(body).unblock()
                # message.mark_read()
            else:
                try:
                    if " " in body:
                        # reddit.subreddit("***REMOVED***").submit(title, selftext=body)
                        # message_content = message_content + body
                        reddit.subreddit("***REMOVED***").message( sender + " vient de poster sur r/***REMOVED***", message_content)
                        reddit.redditor("***REMOVED***").message("posting to ***REMOVED***", message_content)   
                        # reddit.redditor("***REMOVED***").message("ISSUE WITH BOT UNBLOCKING", message_content)
                        # message.reply("il y a eu un problème, u/***REMOVED*** a été informé")       
                        message.mark_read()
                    elif "np.reddit" in body:
                        reddit.subreddit("***REMOVED***").submit(title, url=body)
                        reddit.subreddit("***REMOVED***").message(sender + " vient de poster sur r/***REMOVED***", message_content)
                        message.mark_read()
                    # elif "reddit" in body
                    # elif "/r/france" in body
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT POSTING", message_content)
                    message.mark_read()
                # reddit.subreddit("***REMOVED***").submit(title, url=body)
                # message_content = message_content + body
                # message.reply(message_content)                
                # message.mark_read()
    # sleep one minute
    time.sleep(30)
    # time.sleep(900)
