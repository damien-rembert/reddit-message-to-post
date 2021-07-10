import praw

reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    password="***REMOVED***",
    user_agent="***REMOVED***",
    username="***REMOVED***"
)

# go through unread mail
for message in reddit.inbox.unread(mark_r ead=False, limit=None):
    # TODO if sender is not banned
    # TODO if sender has enough karma
    # get sender name
    redditor1 = message.author
    # get redditor karma
    redditorKarma = redditor1.link_karma
    minKarma = 50
    # print("karma is " + redditorKarma) # not working as karma is an int

    # sender does not have enough karma
    if redditorKarma < minKarma:
        message.mark_read()
    # if the message is not a comment reply
    if message.was_comment:
        message.mark_read()
    else:
        # do stuff with the message/parse message
        # Create a submission to r/***REMOVED***
        title = message.subject
        linko = message.body
        # body = message.body
        reddit.subreddit("***REMOVED***").submit(title, url=linko)
        # mark message as read
        message.mark_read()

