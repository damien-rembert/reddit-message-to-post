#!/usr/bin/env python3
import praw
import time
import os
import re


# TODO ask mods about minimum karma
# TODO ask mods if they want to be notified about list changes
# TODO ask mods if they want the approved lists to skip modmail
# TODO ask mods if they want other subreddits

# TODO replace ***REMOVED*** with ***REMOVED***

# TODO define methods using def
# TODO define method report fault to ***REMOVED***
# TODO define method report things to mods
# TODO define method redditor.HasEnoughKarma(amountOfKarmaNeeded)
# TODO define method redditor.IsTrusted() returning bool
# TODO add reply to failed admin that prints the lists
# TODO add helpsuggestion as a footer to all mail to mods

def isAdminWord(messageTitle):
    global adminWordList
    titleIsAdminWord = False
    for adminWord in adminWordList:
        if adminWord == messageTitle:
           titleIsAdminWord = True
           break
    return titleIsAdminWord

def isMod(redditorName):
    global modList
    senderIsMod = False
    for moderator in modList:
        if redditorName == moderator.name:
           senderIsMod = True
           break
    return senderIsMod

def isTrusted(redditorName):
    global trustedList
    redditorIsTrusted = False
    for user in trustedList:
        if redditorName == user.name:
           redditorIsTrusted = True
           break
    return redditorIsTrusted

def isBlocked(redditorName):
    global blockedList
    redditorIsBlocked = False
    for user in blockedList:
        if redditorName == user.name:
           redditorIsBlocked = True
           break
    return redditorIsBlocked

def cleanUrl(dirtyUrl):
    # regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/france/.+$)", dirtyUrl)
    regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/***REMOVED***/.+$)", dirtyUrl)
    baseUrl = regexClean.group("url")
    fullUrl = "https://np.reddit.com/" + baseUrl
    return fullUrl

def adminTrust(sender,title,body):
    global trustedList
    global blockedList

def listToString(list):
    x = ""
    for element in list:
        redditorName = element.name
        x = x + ", " + redditorName
    return x

def refreshList(listName):
    global modList
    global trustedList
    global blockedList
    if listName == "trusted":
        trustedList = reddit.user.trusted()
    elif listName == "blocked":
        blockedList = reddit.user.blocked()






# set minimum karma needed
minKarma = 50
# set sub
selectedSub = "***REMOVED***"
# selectedSub = "***REMOVED***"
helpWord = "Help"
blockWord = "Block"
unblockWord = "Unblock"
trustWord = "Trust"
distrustWord = "Distrust"
adminWordList = [helpWord, blockWord, unblockWord, trustWord, distrustWord]

helpMessage = "Bonjour,\nEn tant que mod de r/***REMOVED***, vous pouvez utiliser plusieurs fonctions spéciales de ce bot.\nPour cela il suffit d'envoyer un message à ce bot avec pour objet:\n" + helpWord + ", pour recevoir ce message, qui définit les différentes options.\nLes autres options servent à la gestion des redditeur qui utilisent le bot. Ces fonctions s'utilisent en mettant un mot-clé en objet (première lettre majuscule et le reste en minuscule) et le nom du redditeur (sans /u/) dans le corps du message.\n" + trustWord + ", pour ajouter quelqu'un à la liste des Redditors autorisés à poster sans signalement au modmail.\n" + distrustWord + " pour retirer une personne de cette liste.\n" + blockWord + ", pour ajouter un redditeur à la liste de spam du bot et que ses messages soient refusés automatiquement.\n" + unblockWord + ", pour retirer une personne de cette liste.\n\nCe bot a été crée par /u/***REMOVED***, n'hésitez pas à le contacter au besoin!"


# put try/except at lowest level only
# loop forever
# if comment: mark as read
# elif title is adminWord:
#     if mod: do adminTask
#     else: send warning to mods and ***REMOVED***
# elif body contains r/france:
#     if approved redditor: do post (with message to mods?)
#     elif enough karma: do post with message to mods
# else:
#     if mod: "only accepting r/france links + format atm" + help suggestion
#     else: send message "only accepting r/france links + format atm" and notify mods




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

        # get lists
        modList = reddit.subreddit(selectedSub).moderator()
        trustedList = reddit.user.trusted()
        blockedList = reddit.user.blocked()

        # defaulting values
        body = ""
        title = ""
        message_content = ""
        spacing = " - "
        senderIsTrusted = False
        senderIsMod = False
        senderKarma = 0
        senderName = ""
        helpSuggestion = "\n\nPour plus de détails sur les fonctions de ce bot, envoyez-lui un message ayant pour objet " + helpWord + "."

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
        senderIsTrusted = isTrusted(senderName)
        # is redditor a mod
        senderIsMod = isMod(senderName)
        adminMode = isMod(senderName) and isAdminWord(title)

        # ignore comments
        if message.was_comment:
            message.mark_read()
            break
        elif adminMode:
            # admin command 0 Help
            # adminTask(sender,title,body)
            if title == "Help":
                message.reply(helpMessage)
                message.mark_read()
                break
            # admin command 1 Trust
            if title == "Trust":
                if isTrusted(body):
                    message.reply(body + " est déjà sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).trust()
                        refreshList("trusted")
                        message.reply(body + " est maintenant sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs approuvés." , "Voici la liste des redditeurs approuvés:\n" + trustedList +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break

            # admin command 2 Distrust trial
            if title == "Distrust":
                if not isTrusted(body):
                    message.reply(body + " n'est pas sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).distrust()
                        refreshList("trusted")
                        message.reply(body + " est maintenant supprimé de la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs approuvés." , " Voici la liste des redditeurs approuvés:\n" + trustedList +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break
                        
            # admin command 3 Block
            elif title == "Block" and senderIsMod:
                try:
                    # is target already blocked
                    for user in blockedList:
                        if body == user.name:
                            targetIsBlocked = True
                        break
                    if targetIsBlocked:
                        message.reply(body + " est déjà sur la liste des redditeurs bloqués.")
                    else:
                        reddit.redditor(body).block()
                        message.reply(body + " est maintenant sur la liste des redditeurs bloqués.")
                    message.mark_read()
                except:
                    reddit.redditor("***REMOVED***").message("ISSUE WITH BOT BLOCKING", message_content)
                    message.reply("il y a eu un problème, u/***REMOVED*** a été informé")
                    message.mark_read()
            # admin command 4 unblock
            elif title == "Unblock" and senderIsMod:
                try:
                    # is target blocked
                    for user in blockedList:
                        if body == user.name:
                            targetIsBlocked = True
                        break
                    if targetIsBlocked:
                        reddit.redditor(body).unblock()
                        message.reply(body + " n'est plus sur la liste des redditeurs bloqués.")
                    else:
                        message.reply(body + " n'était pas sur la liste des redditeurs bloqués.")
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
                        reddit.subreddit(selectedSub).submit(title, url=cleanUrl(body))
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
    reddit.subreddit(selectedSub).message("essai modmail", "avec un objet et un corps")
    reddit.subreddit(selectedSub).message("essai pied" ,  helpSuggestion)
    reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)

