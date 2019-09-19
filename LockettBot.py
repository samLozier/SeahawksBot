import csv
import praw
import datetime
import creds
import os

rootpath = os.getcwd()

reddit = praw.Reddit(client_id=creds.creds['client_id'],
                     client_secret=creds.creds['client_secret'],
                     password=creds.creds['password'],
                     user_agent=creds.creds['user_agent'],
                     username=creds.creds['username'])

def search():
    try:
        with open(os.path.join(rootpath, 'commentid.csv'), "r") as prev_ids_file:
            data = csv.reader(prev_ids_file)
            prev_id_list = []
            for row in data:
                prev_id_list.append(row[0])
            prev_ids_file.close()
    except:
        prev_id_list = []

    reply_log = open(os.path.join(rootpath, "reply_log.txt"), "a+")
    prev_ids_file = open(os.path.join(rootpath, 'commentid.csv'), "a+")
    for results in reddit.subreddit(
            'Seahawks').comments():  # Grab all the Recent Comments in every subreddit. This will return 100 of the newest comments on Reddit
        body = results.body.lower()   # Grab the Comment
        comment_id = results.id  # Get the Comment ID
        author = results.author
        if comment_id in prev_id_list:  # Check if we already replied to this comment
            continue
        else:
            found = str(body.find('lockette'))
            ricardo = str(body.find('ricardo'))
            if found != '-1' and ricardo == '-1' and author != 'seahawks_bot12':  # Looks like the comment references the wrong player
                try:
                    results.reply("I'm the Seahawks bot, here to help you spell player names and maybe do other useful things in the future.\n\n"
                                  "\n\n"
                                  "You typed Lockett**e** but you might have meant to type **Lockett** (no 'e')\n\n"
                                  "**[Ricardo Lockette](https://en.wikipedia.org/wiki/Ricardo_Lockette)** was on the superbowl winning team but last played in 2015 before suffering a neck injury\n\n"
                                  "**[Tyler Lockett](https://en.wikipedia.org/wiki/Tyler_Lockett)** Is the current #1 Receiver on the team, he also spells his name differently."
                                  )
                    replied_to = {
                        'comment_id': comment_id,
                        'author': author,
                        'body': body
                    }
                    reply_log.write(str(replied_to)+',\n')
                    prev_ids_file.write(str(comment_id)+',\n')
                except:
                    continue

    prev_ids_file.close()
    reply_log.close()


search()
