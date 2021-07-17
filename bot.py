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
        helpSuggestion = "\n\nPour plus de détails sur les fonctions de ce bot ou pour afficher les listes de redditeurs approuvés et bloqués, envoyez-lui un message ayant pour objet " + helpWord + "."
        helpMessage = "Bonjour,\nEn tant que mod de r/***REMOVED***, vous pouvez utiliser plusieurs fonctions spéciales de ce bot.\nPour cela il suffit d'envoyer un message à ce bot avec pour objet:\n" + helpWord + ", pour recevoir ce message, qui définit les différentes options.\nLes autres options servent à la gestion des redditeur qui utilisent le bot. Ces fonctions s'utilisent en mettant un mot-clé en objet (première lettre majuscule et le reste en minuscule) et le nom du redditeur (sans /u/) dans le corps du message.\n" + trustWord + ", pour ajouter quelqu'un à la liste des Redditors autorisés à poster sans signalement au modmail.\n" + distrustWord + " pour retirer une personne de cette liste.\n" + blockWord + ", pour ajouter un redditeur à la liste de spam du bot et que ses messages soient refusés automatiquement.\n" + unblockWord + ", pour retirer une personne de cette liste.\n\nCe bot a été crée par /u/***REMOVED***, n'hésitez pas à le contacter au besoin!\n\n\nVoici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  " \n\n\nVoici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion  


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
            elif title == "Trust":
                if isTrusted(body):
                    message.reply(body + " est déjà sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).trust()
                        refreshList("trusted")
                        message.reply(body + " est maintenant sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs approuvés." , "Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        reddit.redditor("***REMOVED***").message(sender + " a envoyé un message qui a rencontré une erreur", message_content)
                        # message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break

            # admin command 2 Distrust
            elif title == "Distrust":
                if not isTrusted(body):
                    message.reply(body + " n'est pas sur la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).distrust()
                        refreshList("trusted")
                        message.reply(body + " est maintenant supprimé de la liste des redditeurs approuvés.\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs approuvés." , " Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        reddit.redditor("***REMOVED***").message(sender + " a envoyé un message qui a rencontré une erreur", message_content)
                        # message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break
                        
            # admin command 3 Block
            elif title == "Block":
                if isBlocked(body):
                    message.reply(body + " est déjà sur la liste des redditeurs bloqués.\n Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).block()
                        refreshList("blocked")
                        message.reply(body + " est maintenant sur la liste des redditeurs bloqués.\n Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs bloqués." , "Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        reddit.redditor("***REMOVED***").message(sender + " a envoyé un message qui a rencontré une erreur", message_content)
                        # message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break

            # admin command 4 unblock
            elif title == "Unblock":
                if not isBlocked(body):
                    message.reply(body + " n'est pas sur la liste des redditeurs bloqués.\n Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                    message.mark_read()
                    break
                else:
                    try:
                        reddit.redditor(body).unblock()
                        refreshList("blocked")
                        message.reply(body + " n'est plus sur la liste des redditeurs bloqués.\n Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                        reddit.subreddit(selectedSub).message(senderName + " vient d'ajouter " + body + " à la liste des redditeurs bloqués." , "Voici la liste des redditeurs bloqués:\n" + listToString(blockedList) +  helpSuggestion)
                        message.mark_read()
                        break
                    except:
                        reddit.redditor("***REMOVED***").message(sender + " a envoyé un message qui a rencontré une erreur", message_content)
                        # message.reply("Trust n'a pas fonctionné. " + body + " est peut-être déjà sur la liste des redditeurs approuvés?\n Voici la liste des redditeurs approuvés:\n" + listToString(trustedList) +  helpSuggestion)
                        message.mark_read()
                        break

                # message.mark_read()
        elif senderKarma >= minKarma:
            try:
                # if " " in body:
                #         # reddit.subreddit(selectedSub).submit(title, selftext=body)
                #         message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                #         reddit.subreddit(selectedSub).message("Post refusé, le corps du message contient un caractère interdit: " +senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                #         message.mark_read()
                if "r/***REMOVED***/" in body:
                # elif "r/france/" in body:
                    reddit.subreddit(selectedSub).submit(title, url=cleanUrl(body))
                    reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content)
                    message.reply("Merci, votre message devrait apparaître sur r/***REMOVED*** dans moins d'une minute!")
                    message.mark_read()
                    break
                else:
                    # elif " " in body:
                        # reddit.subreddit(selectedSub).submit(title, selftext=body)
                    message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur r/France. Merci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers r/France")
                    reddit.subreddit(selectedSub).message("Post refusé: le corps du message ne semble pas contenir de lien vers r/france. " + senderName + " vient d'essayer de poster anonymement sur r/" + selectedSub + ":", message_content)
                    message.mark_read()
                    break
                    # elif "reddit" in body
                    # elif "/r/france" in body
                except:
                    reddit.redditor("***REMOVED***").message(sender + " a envoyé un message qui a rencontré une erreur", message_content)
                    message.mark_read()
                    break
        elif senderKarma < minKarma:
            # reddit.redditor("***REMOVED***").message(senderName + " n'a pas assez de karma - contrôler et poster", message_content)
            message.reply("Votre karma n'est pas assez élevé, votre message doit donc être approuvé par la modération de /r/***REMOVED***. Merci de patienter un peu!")
            reddit.subreddit(selectedSub).message("Karma de " + senderName + " trop bas, message non posté (à contrôler et poster pour ce redditeur?) - " + senderName + " vient d'essayer de poster sur r/" + selectedSub + ":", message_content)
            message.mark_read()

    # sleep one minute
    time.sleep(30)
