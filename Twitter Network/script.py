import csv
import json
import time
import tweepy

# Tom Hervieu
# Python version 3.5

def loadKeys(key_file):
    # TODO: put in your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    with open(key_file, "r") as in_file:
        text = json.load(in_file)
        api_key = text['api_key']
        api_secret = text['api_secret']
        token = text['token']
        token_secret = text['token_secret']
    return (api_key, api_secret, token, token_secret)

# Q1.b - 5 Marks
def getFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
    # rtype: list containing entries in the form of a tuple (follower, root_user)
    aList = []
    for user in tweepy.Cursor(api.followers, screen_name = root_user).items(no_of_followers):
        tup1 = (user.screen_name, root_user)
        aList.append(tup1)
    return aList

# Q1.b - 7 Marks
def getSecondaryFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    bList = []
    for follower in followers_list:
        for user in tweepy.Cursor(api.followers, screen_name = follower[0]).items(no_of_followers):
            tup1 = (user.screen_name, follower[0])
            bList.append(tup1)
    return bList

# Q1.c - 5 Marks
def getFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    aList = []
    for user in tweepy.Cursor(api.friends, screen_name = root_user).items(no_of_friends):
        tup1 = (root_user, user.screen_name)
        aList.append(tup1)
    return aList

# Q1.c - 7 Marks
def getSecondaryFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    bList = []
    for friend in friends_list:
        for user in tweepy.Cursor(api.friends, screen_name = friend[1]).items(no_of_friends):
            tup1 = (friend[1], user.screen_name)
            bList.append(tup1)
    return bList

# Q1.b, Q1.c - 6 Marks
def writeToFile(data, output_file):
    # write data to output file
    # rtype: None
    file = open(output_file, 'w+')
    for i in data:
        file.write(i[0] + ',' + i[1] + '\n')
    file.close()




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'

    ROOT_USER = 'PoloChau'
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10


    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
    followers = primary_followers + secondary_followers

    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
    friends = primary_friends + secondary_friends

    writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    writeToFile(friends, OUTPUT_FILE_FRIENDS)


if __name__ == '__main__':
    testSubmission()

