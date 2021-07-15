#!/usr/bin/env python3
import praw
import time
import os
import re


# TODO set karma
# TODO replace ***REMOVED*** with ***REMOVED***
# TODO automatically mark mods from ***REMOVED*** as isMod and obey them 
# TODO login without connection details in source code
# TODO check that the url is on r/france
# TODO define methods using def
# TODO define method report fault to ***REMOVED***
# TODO define method report things to mods
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

        # set minimum karma needed
        minKarma = 50
        # defaulting values
        body = ""
        title = ""
        message_content = ""
        spacing = " - "
        senderIsTrusted = False
        senderIsMod = False
        senderKarma = 0
        senderName = ""
        # get sender name
        sender = message.author
        senderName = message.author.name
        # get redditor karma
        senderKarma = sender.link_karma
        title = message.subject
        body = message.body
        message_content = "TITRE: " + title + " - CORPS: " + body
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            # print(f"User: {user.name}")
            if senderName == user.name:
                senderIsTrusted = True
                break
        for moderator in reddit.subreddit("***REMOVED***").moderator():
           # print(f"{moderator}: {moderator.mod_permissions}")
            if senderName == moderator.name:
                senderIsMod = True
                break
        # ignore comments
        if message.was_comment:
            message.mark_read()
        else:
            # admin command 1 Trust
            if title == "Trust" and senderIsMod:
                try:
                    reddit.redditor(body).trust()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT TRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 2 Distrust
            elif title == "Distrust" and senderIsMod:
                try:
                    reddit.redditor(body).distrust()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT DISTRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 3 Block
            elif title == "Block" and senderIsMod:
                try:
                    reddit.redditor(body).block()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT BLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 4 unblock
            elif title == "Unblock" and senderIsMod:
                try:
                    reddit.redditor(body).unblock()
                    message.mark_read()
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT UNBLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
                # message.mark_read()
            elif senderKarma > minKarma:
                try:
                    if "np.reddit.com/r/***REMOVED***" in body:
                    # elif "np.reddit.com/r/france" in body:
                        reddit.subreddit("***REMOVED***").submit(title, url=body)
                        reddit.subreddit("***REMOVED***").message(senderName + " vient de poster sur r/***REMOVED***: ", message_content)
                        message.mark_read()
                    else:
                    # elif " " in body:
                        # reddit.subreddit("***REMOVED***").submit(title, selftext=body)
                        # message_content = message_content + body
                        message.reply("Ce bot n'accepte actuellement que les message dont le corps est un lien vers r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps le lien vers r/France")
                        reddit.subreddit("***REMOVED***").message( senderName + " vient de poster sur r/***REMOVED***", message_content)
                        reddit.redditor("***REMOVED***").message("posting to ***REMOVED***", message_content)   
                        # reddit.redditor("***REMOVED***").message("ISSUE WITH BOT UNBLOCKING", message_content)
                        # message.reply("il y a eu un problème, u/***REMOVED*** a été informé")       
                        message.mark_read()
                    # elif "reddit" in body
                    # elif "/r/france" in body
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT POSTING", message_content)
                    message.mark_read()
            elif senderKarma <= minKarma:
                # reddit.redditor("***REMOVED***").message(senderName + " n'a pas assez de karma - contrôler et poster", message_content)
                # reddit.subreddit("test").message("TEST", "test PM from PRAW")
                reddit.subreddit("***REMOVED***").message("Karma trop bas, message non posté (à contrôler et poster pour ce redditeur?) - " + senderName + " vient d'essayer de poster sur r/***REMOVED***: ", message_content)
                message.mark_read()
                # reddit.subreddit("***REMOVED***").submit(title, url=body)
                # message_content = message_content + body
                # message.reply(message_content)                
                # message.mark_read()
    # sleep one minute
    time.sleep(30)
    # time.sleep(900)
