
import praw
import datetime
import time
import json
import creds
import os

rootpath = os.getcwd()

reddit = praw.Reddit(client_id=creds.creds['client_id'],
                     client_secret=creds.creds['client_secret'],
                     password=creds.creds['password'],
                     user_agent=creds.creds['user_agent'],
                     username=creds.creds['username'])


def search():
    prev_ids = open(os.path.join(rootpath, 'commentid.txt'), "a+")
    reply_log = open(os.path.join(rootpath, "reply_log.txt"), "a+")
    for results in reddit.subreddit(
            'Seahawks').comments():  # Grab all the Recent Comments in every subreddit. This will return 100 of the newest comments on Reddit
        body = results.body.lower()   # Grab the Comment
        comment_id = results.id  # Get the Comment ID
        author = results.author
        if comment_id in prev_ids:  # Check if we already replied to this comment
            continue
        else:
            found = str(body.find('lockette'))
            ricardo = str(body.find('ricardo'))
            #print(body)
            if found != '-1' and ricardo == '-1' and author != 'Seahawks_Bot12':  # Looks like the comment references the wrong player
                try:
                    results.reply("I'm the Seahawks bot, here to help you spell player names and maybe do other useful things in the future."
                                  ""
                                  "You typed Lockett**e** but you might have meant to type **Lockett** (no 'e')\n\n"
                                  "**[Ricardo Lockette](https://en.wikipedia.org/wiki/Ricardo_Lockette)** was on the superbowl winning team but last played in 2015 before suffering a neck injury\n\n"
                                  "**[Tyler Lockett](https://en.wikipedia.org/wiki/Tyler_Lockett)** Is the current #1 Receiver on the team, he also spells his name differently."
                                  )
                    replied_to = {
                        'comment_id': comment_id,
                        'author': author,
                        'body': body
                    }
                    reply_log.write(json.dumps(replied_to))
                    prev_ids.write(json.dumps(comment_id))
                except:
                    continue

    reply_log.write(f'{datetime.datetime.now()} - End of loop\n')
    prev_ids.close()
    reply_log.close()

search()
