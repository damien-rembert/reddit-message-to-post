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

        # getting message content
        title = message.subject
        body = message.body
        message_content = "TITRE: " + title + " - CORPS: " + body
        
        # is redditor trusted
        trusted_users = reddit.user.trusted()
        for user in trusted_users:
            if senderName == user.name:
                senderIsTrusted = True
                break

        # is redditor a mod
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
                    # is target already trusted
                    trusted_users = reddit.user.trusted()
                    for user in trusted_users:
                        if body == user.name:
                            targetIsTrusted = True
                        break
                    if targetIsTrusted:
                        message.reply(body + " est déjà sur la liste des redditeurs approuvés.")
                    else:
                        reddit.redditor(body).trust()
                        message.reply(body + " est maintenant sur la liste des redditeurs approuvés.")
                    # reddit.subreddit(selectedSub).message( senderName + " vient de poster sur r/" + selectedSub, message_content)
                    message.mark_read()
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT TRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 2 Distrust
            elif title == "Distrust" and senderIsMod:
                try:
                    # is target already trusted
                    trusted_users = reddit.user.trusted()
                    for user in trusted_users:
                        if body == user.name:
                            targetIsTrusted = True
                        break
                    if targetIsTrusted:
                        reddit.redditor(body).distrust()
                        message.reply(body + " n'est plus sur la liste des redditeurs approuvés.")
                    else:
                        message.reply(body + " n'était pas sur la liste des redditeurs approuvés.")
                    # reddit.subreddit(selectedSub).message( senderName + " vient de poster sur r/" + selectedSub, message_content)
                    message.mark_read()
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT DISTRUSTING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 3 Block
            elif title == "Block" and senderIsMod:
                try:
                    # is target already blocked
                    blocked_users = reddit.user.blocked()
                    for user in blocked_users:
                        if body == user.name:
                            targetIsBlocked = True
                        break
                    if targetIsBlocked:
                        message.reply(body + " est déjà sur la liste des redditeurs bloqués.")
                    else:
                        reddit.redditor(body).block()
                        message.reply(body + " est maintenant sur la liste des redditeurs bloqués.")
                    # reddit.subreddit(selectedSub).message( senderName + " vient de poster sur r/" + selectedSub, message_content)
                    message.mark_read()
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT BLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 4 unblock
            elif title == "Unblock" and senderIsMod:
                try:
                    # is target blocked
                    blocked_users = reddit.user.blocked()
                    for user in blocked_users:
                        if body == user.name:
                            targetIsBlocked = True
                        break
                    if targetIsBlocked:
                        reddit.redditor(body).unblock()
                        message.reply(body + " n'est plus sur la liste des redditeurs bloqués.")
                    else:
                        message.reply(body + " n'était pas sur la liste des redditeurs bloqués.")
                    # reddit.subreddit(selectedSub).message( senderName + " vient de poster sur r/" + selectedSub, message_content)
                    message.mark_read()
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT UNBLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
                # message.mark_read()
            elif senderKarma > minKarma:
                try:
                    if " " in body:
                        # reddit.subreddit(selectedSub).submit(title, selftext=body)
                        message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                        reddit.subreddit(selectedSub).message("Post refusé, le corps du message contient un caractère interdit: " +senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                        message.mark_read()
                    elif "r/***REMOVED***/" in body:
                    # elif "r/france/" in body:
                        # regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/france/.+$)", body)
                        regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/***REMOVED***/.+$)", body)
                        baseUrl = regexClean.group("url")
                        fullUrl = "https://np.reddit.com/" + baseUrl
                        reddit.subreddit(selectedSub).submit(title, url=fullUrl)
                        reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)
                        message.reply("Merci, votre message devrait apparaître sur r/***REMOVED*** dans moins d'une minute!")
                        message.mark_read()
                    else:
                    # elif " " in body:
                        # reddit.subreddit(selectedSub).submit(title, selftext=body)
                        message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                        reddit.subreddit(selectedSub).message("Post refusé: le corps du message ne semble pas contenir de lien vers r/france. " + senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                        message.mark_read()
                    # elif "reddit" in body
                    # elif "/r/france" in body
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT POSTING", message_content)
                    message.mark_read()
            elif senderKarma <= minKarma:
                # reddit.redditor("***REMOVED***").message(senderName + " n'a pas assez de karma - contrôler et poster", message_content)
                message.reply("Votre karma n'est pas assez élevé, votre message doit donc être approuvé par la modération de /r/***REMOVED***. Merci de patienter un peu!")
                reddit.subreddit(selectedSub).message("Karma de " + senderName + " trop bas, message non posté (à contrôler et poster pour ce redditeur?) - " + senderName + " vient d'essayer de poster sur r/" + selectedSub + ":", message_content)
                message.mark_read()
    # sleep one minute
    time.sleep(30)

                        # message.reply("Ce bot n'accepte actuellement que les message dont le corps est un lien vers r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps le lien vers r/France")
                        # reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)
                        # reddit.redditor("***REMOVED***").message("posting to ***REMOVED***", message_content)
                        # reddit.subreddit(selectedSub).submit(title, url=body)

