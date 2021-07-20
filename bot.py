#!/usr/bin/env python3
import praw
import time
import os
import re
from datetime import datetime
from datetime import timedelta



# TODO define methods using def
# TODO define method report things to mods
# TODO check length of strings from senders
# DONE supprimer le minimum de karma 
# DONE remplacer istrusted par le critère de 72h 
# DONE envoyer en modmail que les threads créés
# prévoir un thread de présentation
# add /u/ to senderName
# cleanEchoTitle
# DONE retirer trusted

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

def isOldEnough(redditor):
    # is sender old enough
    # get sender age
    # senderDob = datetime.fromtimestamp(sender.created_utc)
    senderDob = datetime.utcfromtimestamp(redditor.created_utc)
    senderIsOldEnough = False
    # min 72h old
    # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
    seventyTwoH = datetime.utcnow() - timedelta(hours=72)
    # 
    if senderDob <= seventyTwoH:
        senderIsOldEnough = True
        reddit.redditor("***REMOVED***").message("senderdob is over 72h", "sender dob is " + str(senderDob) + "seventytwo is " + str(seventyTwoH) + )
    else:
        senderIsOldEnough = False
        reddit.redditor("***REMOVED***").message("senderdob is over 72h", "sender dob is " + str(senderDob) + "seventytwo is " + str(seventyTwoH) + )
            return senderIsOldEnough
        #     tenYears = datetime.utcnow() - timedelta(days=4000)
        # # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # if senderDob >= tenYears:
        #     senderIsOlder = True
        # else:
        #     reddit.redditor("***REMOVED***").message("senderdob is under ten years", str(senderIsOlder))





def cleanUrl(dirtyUrl):
    regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/france/.+$)", dirtyUrl)
    # regexClean = re.search(r"(?:http|https)?(?:www|np.reddit.com)?(:?/)?(?P<url>r/***REMOVED***/.+$)", dirtyUrl)
    baseUrl = regexClean.group("url")
    fullUrl = "https://np.reddit.com/" + baseUrl
    return fullUrl


def cleanEchoTitle(dirtyTitle):
    regexClean = re.search(r"(?:Echo: )(?P<title>.+$)", dirtyUrl)
    cleanTitle = regexClean.group("title")
    return cleanTitle

# def adminTrust(sender,title,body):
#     global trustedList
#     global blockedList

def listToString(list):
    x = ""
    for element in list:
        redditorName = element.name
        if x == "":
            x = redditorName
        else:
            x = x + ", " + redditorName
    return x

def refreshListTrusted():
    global trustedList
    trustedList = reddit.user.trusted()
    time.sleep(1)

def refreshListBlocked():
    global blockedList
    blockedList = reddit.user.blocked()
    time.sleep(1)

def reportToLamalediction(senderName,content):
    reddit.redditor("***REMOVED***").message("/u/" + senderName + " a envoyé un message qui a rencontré une erreur", content)

def replySuccess(operation, targetName, listo):
    if operation == trustWord:
        middleString = " est maintenant sur la liste des pseudos approuvés.\n Voici la liste des pseudos approuvés:\n"
    elif operation == distrustWord:
        middleString = " a été retiré de la liste des pseudos approuvés.\n Voici la liste des pseudos approuvés:\n"
    elif operation == blockWord:
        middleString = " est maintenant sur la liste des pseudos bloqués.\n Voici la liste des pseudos bloqués:\n"
    elif operation == unblockWord:
        middleString = " a été retiré de la liste des pseudos bloqués.\n Voici la liste des pseudos bloqués:\n"
    message.reply(targetName + middleString + listToString(listo) +  helpSuggestion)

def replyAlready(operation, targetName, listo):
    if operation == trustWord:
        middleString = " est déjà sur la liste des pseudos approuvés.\n Voici la liste des pseudos approuvés:\n"
    elif operation == distrustWord:
        middleString = " n'est pas sur la liste des pseudos approuvés.\n Voici la liste des pseudos approuvés:\n"
    elif operation == blockWord:
        middleString = " est déja sur la liste des pseudos bloqués.\n Voici la liste des pseudos bloqués:\n"
    elif operation == unblockWord:
        middleString = " n'est pas sur la liste des pseudos bloqués.\n Voici la liste des pseudos bloqués:\n"
    message.reply(targetName + middleString + listToString(listo) +  helpSuggestion)

def messageModsSuccess(operation, sender, targetName, listo):
    addString = " vient d'ajouter " + targetName + " à la liste des pseudos "
    removeString = " vient de supprimer " + targetName + " de la liste des pseudos "
    approvedString = "approuvés"
    blockedString = "bloqués"
    bodyString = "Voici la liste des pseudos "
    if operation == trustWord:
        actionString = addString
        listName = approvedString
    elif operation == distrustWord:
        actionString = removeString
        listName = approvedString
    elif operation == blockWord:
        actionString = addString
        listName = blockedString
    elif operation == unblockWord:
        actionString = removeString
        listName = blockedString
    # reddit.subreddit(selectedSub).message(sender + actionString + listName + ".", bodyString + listName + ":\n\n" + listToString(listo) +  helpSuggestion)



# set minimum karma needed
# minKarma = 50
# set sub
selectedSub = "***REMOVED***"
# selectedSub = "***REMOVED***"
helpWord = "Help"
blockWord = "Block"
unblockWord = "Unblock"
trustWord = "Trust"
distrustWord = "Distrust"
adminWordList = [helpWord, blockWord, unblockWord, trustWord, distrustWord]


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
    
    
    
    # initial post
    # reddit.subreddit(selectedSub).submit(title, url=cleanedUrl)
    # reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content + helpSuggestion)
    # message.reply("Merci, votre message devrait apparaître sur r/***REMOVED*** dans moins d'une minute!")


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
        # senderIsOldEnough = False
        senderIsMod = False
        # senderKarma = 0
        senderName = ""
        helpSuggestion = "\n\n\n**********************\n\n\nPour plus de détails sur les fonctions de ce bot ou pour afficher les listes de pseudos approuvés et bloqués, envoyez-lui un message ayant pour objet **" + helpWord + "** (et n'importe quoi dans le corps du message)."
        helpMessage = "Bonjour,\n\n\nEn tant que mod de /r/***REMOVED***, vous pouvez utiliser plusieurs fonctions spéciales de ce bot.\nPour cela il suffit d'envoyer un message à ce bot avec pour objet:\n\n**" + helpWord + "**, pour recevoir ce message, qui définit les différentes options.\n\n\n\nLes autres options servent à la gestion des personnes qui utilisent le bot. Ces fonctions s'utilisent en mettant un mot-clé en objet (première lettre majuscule et le reste en minuscule) et le pseudo (sans /u/) dans le corps du message.\n\n**" + blockWord + "**, pour ajouter un pseudo à la liste de spam du bot et que ses messages soient refusés automatiquement.\n\n**" + unblockWord + "**, pour retirer une personne de cette liste.\n\nCe bot a été crée par /u/***REMOVED***, n'hésitez pas à le contacter au besoin!\n\n\nVoici la liste des pseudos bloqués:\n\n" + listToString(blockedList) +  helpSuggestion  


        # get sender name
        sender = message.author
        senderName = message.author.name

        # get redditor karma
        # senderKarma = sender.link_karma

        # getting message content
        title = message.subject
        body = message.body
        message_content = "TITRE: " + title + " - CORPS: " + body



        # is sender old enough
        # get sender age
        # senderDob = datetime.fromtimestamp(sender.created_utc)
        # senderDob = datetime.utcfromtimestamp(sender.created_utc)
        # min 72h old
        # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # if senderDob >= seventyTwoH:
        #     senderIsOldEnough = True
        #     reddit.redditor("***REMOVED***").message("senderdob is over 72h", str(senderIsOldEnough))

        # min 72h old
        # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # tenYears = datetime.utcnow() - timedelta(days=4000)
        # # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # if senderDob >= tenYears:
        #     senderIsOlder = True
        # else:
        #     reddit.redditor("***REMOVED***").message("senderdob is under ten years", str(senderIsOlder))

        # senderDob = datetime.utcfromtimestamp(redditor.created_utc)
        # senderIsOldEnough = False
        #     # min 72h old
        #     # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # seventyTwoH = datetime.utcnow() - timedelta(hours=72)
        # if senderDob >= seventyTwoH:
        #     senderIsOldEnough = True
        #     reddit.redditor("***REMOVED***").message("senderdob is over 72h", str(senderIsOldEnough))
        # else:
        #     senderIsOldEnough = False
        #     reddit.redditor("***REMOVED***").message("senderdob is not over 72h", str(senderIsOldEnough))








        # is redditor trusted
        # senderIsTrusted = isTrusted(senderName)
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
            if title == helpWord or title == "Help" or title == "help":
                message.reply(helpMessage)
                message.mark_read()
                break
            # admin command 1 Trust
            elif title == trustWord:
                if isTrusted(body):
                    replyAlready(title, body, trustedList)
                    message.mark_read()
                    break
                else:
                    reddit.redditor(body).trust()
                    refreshListTrusted()
                    replySuccess(title, body, trustedList)
                    messageModsSuccess(title, senderName, body, trustedList)
                    message.mark_read()
                    break
                    # try:
                    #     reddit.redditor(body).trust()
                    #     refreshListTrusted()
                    #     replySuccess(title, body, trustedList)
                    #     messageModsSuccess(title, senderName, body, trustedList)
                    #     message.mark_read()
                    #     break
                    # except:
                    #     reportToLamalediction(sender, message_content)
                    #     message.mark_read()
                    #     break

            # admin command 2 Distrust
            elif title == distrustWord:
                if not isTrusted(body):
                    replyAlready(title, body, trustedList)
                    message.mark_read()
                    break
                else:
                    reddit.redditor(body).distrust()
                    refreshListTrusted()
                    replySuccess(title, body, trustedList)
                    messageModsSuccess(title, senderName, body, trustedList)
                    message.mark_read()
                    break
                    # try:
                    #     reddit.redditor(body).distrust()
                    #     refreshListTrusted()
                    #     replySuccess(title, body, trustedList)
                    #     messageModsSuccess(title, senderName, body, trustedList)
                    #     message.mark_read()
                    #     break
                    # except:
                    #     reportToLamalediction(senderName, message_content)
                    #     message.mark_read()
                    #     break
                        
            # admin command 3 Block
            elif title == blockWord:
                if isBlocked(body):
                    replyAlready(title, body, blockedList)
                    message.mark_read()
                    break
                else:
                    reddit.redditor(body).block()
                    refreshListBlocked()
                    replySuccess(title, body, blockedList)
                    messageModsSuccess(title, senderName, body, blockedList)
                    message.mark_read()
                    break
                    # try:
                    #     reddit.redditor(body).block()
                    #     refreshListBlocked()
                    #     replySuccess(title, body, blockedList)
                    #     messageModsSuccess(title, senderName, body, blockedList)
                    #     message.mark_read()
                    #     break
                    # except:
                    #     reportToLamalediction(senderName, message_content)
                    #     message.mark_read()
                    #     break

            # admin command 4 unblock
            elif title == unblockWord:
                if not isBlocked(body):
                    replyAlready(title, body, blockedList)
                    message.mark_read()
                    break
                else:
                    reddit.redditor(body).unblock()
                    refreshListBlocked()
                    replySuccess(title, body, blockedList)
                    messageModsSuccess(title, senderName, body, blockedList)
                    message.mark_read()
                    break
                    # try:
                    #     reddit.redditor(body).unblock()
                    #     refreshListBlocked()
                    #     replySuccess(title, body, blockedList)
                    #     messageModsSuccess(title, senderName, body, blockedList)
                    #     message.mark_read()
                    #     break
                    # except:
                    #     reportToLamalediction(senderName, message_content)
                    #     message.mark_read()
                    #     break

                # message.mark_read()
        elif isOldEnough(sender):
            if " " in body:
                message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur /r/France.\n\n\nMerci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers /r/France")
                # reddit.subreddit(selectedSub).message(senderName + " a essayé de poster un message sans lien vers r/France:", message_content + helpSuggestion)
                message.mark_read()
                break
            # if "r/***REMOVED***/" in body:
            elif "r/france/" in body:
                cleanedUrl = cleanUrl(body)
                reddit.subreddit(selectedSub).submit(title, url=cleanedUrl)
                reddit.subreddit(selectedSub).message("/u/" + senderName + " vient de poster sur /r/" + selectedSub + ":", message_content + helpSuggestion)
                message.reply("Merci, votre message devrait apparaître sur /r/***REMOVED*** dans moins d'une minute!")
                message.mark_read()
                break
                # try:
                #     cleanedUrl = cleanUrl(body)
                #     reddit.subreddit(selectedSub).submit(title, url=cleanedUrl)
                #     reddit.subreddit(selectedSub).message(senderName + " vient de poster sur r/" + selectedSub + ":", message_content + helpSuggestion)
                #     message.reply("Merci, votre message devrait apparaître sur r/***REMOVED*** dans moins d'une minute!")
                #     message.mark_read()
                #     break
                # except:
                #     reportToLamalediction(senderName, message_content)
                #     message.mark_read()
                #     break
            else:
                message.reply("Ce bot n'accepte actuellement que les message dont le corps contient uniquement un lien vers un post ou un commentaire sur /r/France.\n\n\nMerci d'envoyer un nouveau message ayant pour objet le titre souhaité pour le post et pour corps un lien vers /r/France")
                # reddit.subreddit(selectedSub).message(senderName + " a essayé de poster un message sans lien vers r/France:", message_content + helpSuggestion)
                message.mark_read()
                break
        elif not isOldEnough(sender):
            message.reply("Votre compte est trop récent, votre message doit donc être approuvé par la modération de /r/***REMOVED***. Merci de patienter un peu!")
            reddit.subreddit(selectedSub).message("/u/" + senderName + " a essayé de poster un message mais son compte est trop récent" , "Post à contrôler et à renvoyer pour /u/" + senderName + "?) - " + message_content + helpSuggestion)
            message.mark_read()
        else:
            message.reply("Votre message doit être approuvé par la modération de /r/***REMOVED***. Merci de patienter un peu!")
            reddit.subreddit(selectedSub).message("/u/" + senderName + " a essayé de poster un message mais il y a eu un problème" , "Post à contrôler et à renvoyer pour /u/" + senderName + "?) - " + message_content + helpSuggestion)
            reportToLamalediction(senderName, message_content)
            message.mark_read()

    # sleep one minute
    time.sleep(30)
