#!/usr/bin/env python3
import praw
import time
import os
import re


# TODO ask mods about minimum karma
# TODO replace ***REMOVED*** with ***REMOVED***
# TODO improve fault reporting

# TODO np.reddit.com instead of www.reddit.com
# TODO check that the url is on r/france

# TODO define methods using def
# TODO login without connection details in source code
# TODO define method report fault to ***REMOVED***
# TODO define method report things to mods
# TODO define method redditor.HasEnoughKarma(amountOfKarmaNeeded)
# TODO define method redditor.IsTrusted() returning bool
# TODO reply to messages confirming that this should appear on the sub shortly


while True:

    # reddit = praw.Reddit(
    # client_id="***REMOVED***",
    # client_secret="***REMOVED***",
    # password="***REMOVED***",
    # user_agent="***REMOVED***",
    # username="***REMOVED***"
    # )

    client_id1 = ""
    client_secret1 = ""
    password1 = ""
    username1 = ""
    client_id1 = os.environ['IDCLIENT']
    client_secret1 = os.environ['SECRETCLIENT']
    password1 = os.environ['MDP']
    username1 = os.environ['NOM']
    user_agent1 = "heroku:inmailtopost:v0.1 (by /u/***REMOVED***)"

reddit = praw.Reddit(
    client_id=client_id1,
    client_secret=client_secret1,
    password=password1,
    user_agent=user_agent1,
    username=username1,
)


    # go through unread mail
    for message in reddit.inbox.unread(mark_read=False, limit=None):

        # set minimum karma needed
        minKarma = 50
        # set sub
        selectedSub = "***REMOVED***"
        # selectedSub = "***REMOVED***"

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
        
        # is redditor trusted and/or mod
        for user in trusted_users:
            if senderName == user.name:
                senderIsTrusted = True
                break
        for moderator in reddit.subreddit(selectedSub).moderator():
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
                    # reddit.subreddit(selectedSub).message( senderName + " vient de poster sur r/" + selectedSub, message_content)
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
                    if " " in body:
                        # reddit.subreddit(selectedSub).submit(title, selftext=body)
                        message.reply("Ce bot n'accepte actuellement que les message dont le corps est un lien vers r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                        reddit.subreddit(selectedSub).message("Post refusé: le corps du message contient un caractère interdit n'est pas sur r/france " +senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                        message.mark_read()
                    elif "np.reddit.com/r/***REMOVED***/" in body:
                    # if "np.reddit.com/r/france/" in body:
                    # if "r/france/" in body:
                        reddit.subreddit(selectedSub).submit(title, url=body)
                        reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)
                        message.mark_read()
                    else:
                    # elif " " in body:
                        # reddit.subreddit(selectedSub).submit(title, selftext=body)
                        message.reply("Ce bot n'accepte actuellement que les message dont le corps est un lien vers r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                        reddit.subreddit(selectedSub).message("Post refusé: le corps du message ne semble pas contenir de lien vers r/france. " + senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                        message.mark_read()
                    # elif "reddit" in body
                    # elif "/r/france" in body
                except:
                    message_content = title + spacing + body
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT POSTING", message_content)
                    message.mark_read()
            elif senderKarma <= minKarma:
                # reddit.redditor("***REMOVED***").message(senderName + " n'a pas assez de karma - contrôler et poster", message_content)
                message.reply("Votre karma n'est pas assez élevé, votre message doit donc être approuvé par la modération de /r/***REMOVED***. Merci de patienter un peu!")
                reddit.subreddit(selectedSub).message("Karma trop bas, message non posté (à contrôler et poster pour ce redditeur?) - " + senderName + " vient d'essayer de poster sur r/" + selectedSub + ":", message_content)
                message.mark_read()
    # sleep one minute
    time.sleep(30)

                        # message.reply("Ce bot n'accepte actuellement que les message dont le corps est un lien vers r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps le lien vers r/France")
                        # reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)
                        # reddit.redditor("***REMOVED***").message("posting to ***REMOVED***", message_content)
                        # reddit.subreddit(selectedSub).submit(title, url=body)

