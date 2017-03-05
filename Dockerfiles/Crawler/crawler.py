#!/usr/bin/python

from pprint import pprint
import sys
import praw, datetime
import json, time
from pymongo import MongoClient

class Comment(object):
    subreddit 	= ""
    text 		= ""
    commentId	= ""
    created 	= datetime.datetime.now()

    def __init__(self, text, commentId, subreddit, created):
        self.text 	    = text
        self.commentId 	= commentId
        self.subreddit  = subreddit
        self.created 	= created

class Submission(object):
    subreddit 	= ""
    title 		= ""
    postId 		= ""
    created 	= datetime.datetime.now()

    def __init__(self, title, postId, subreddit, created):
        self.title 	    = title
        self.postId 	= postId
        self.subreddit  = subreddit
        self.created 	= created

def delete_old_data(collection):
	try:
		collection.delete_many({})
		return 1
	except:
		print 'An error occured while deleting data.'
		return 0

def check_valid_subreddit(subredditName):
	try:
		for comment in reddit.subreddit(subredditName).comments(limit=1):
			return 1
	except:
		print subredditName + 'is not a valid subreddit.'
		return 0

def get_subreddit_list(data):
	counter = 0
	try:
		for data in data['subreddits']:
			if counter == 0:
				if check_valid_subreddit(data['name']) == 1:
					subredditList = data['name']
			else:
				if check_valid_subreddit(data['name']) == 1:
					subredditList = subredditList + '+' + data['name']
			counter = counter + 1
		return subredditList
	except:
		return ''

		

def start_crawling(subredditList, reddit, coms, subs):
	while True:
		try:
			submissionData 	= [];
			commentData 	= [];
			try:
				for submission in reddit.subreddit(subredditList).new():
					sub = Submission(submission.title, submission.id, str(submission.subreddit), submission.created)
					submissionData.append(sub)

				for comment in reddit.subreddit(subredditList).comments(limit=75):
					com = Comment(comment.body, comment.id, str(comment.subreddit), comment.created)
					commentData.append(com)

				for com in commentData:
					post = {"text": com.text,
							"commentId": com.commentId,
							"subreddit": com.subreddit,
							"created": datetime.datetime.fromtimestamp(com.created)}
					coms.insert_one(post)

				for sub in submissionData:
					post = {"title": sub.title,
							"submissionId": sub.postId,
							"subreddit": sub.subreddit,
							"created": datetime.datetime.fromtimestamp(sub.created)}
					subs.insert_one(post)
			except:
				print 'An error occured while retreiving data.'
	   	except:
	   		print 'An error occured, continuing script,'
		time.sleep(300)

client = MongoClient();
client = MongoClient('localhost', 27017)
subs   = client.reddit.submission
coms   = client.reddit.comment
reddit = praw.Reddit(client_id='p4EKw4zNfSbqrw',
                    client_secret='ucmkavZm68q-aeILcR5WLJBxFmA',
                    user_agent='testingPythonCrawler',
                    password='Kartier666',
                    username='Rockersquid')


if __name__ == "__main__":
	if delete_old_data(subs) and delete_old_data(coms):
		with open('crawler.json') as data_file:    
		    data = json.load(data_file)
		subredditList = get_subreddit_list(data)
		if subredditList != '':
			start_crawling(subredditList, reddit, coms, subs)



