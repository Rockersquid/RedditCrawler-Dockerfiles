import json, time, datetime
from itertools import chain
from flask import Flask, request, Response
from pymongo import MongoClient
from bson.json_util import dumps


client = MongoClient();
client = MongoClient('localhost', 27017)
subs   = client.reddit.submission
coms   = client.reddit.comment
app    = Flask(__name__)


class WatchRequest(object):
    subreddit 	= ""
    fromTime 	= datetime.datetime.now()
    toTime 		= datetime.datetime.now()
    keyword     = ''

    def __init__(self, subreddit, fromTime, toTime, keyword):
        self.subreddit 	= subreddit
        self.fromTime 	= fromTime
        self.toTime 	= toTime
        self.keyword    = keyword


def convert_to_date(time):
	try:
		tmpTime = datetime.datetime.fromtimestamp(float(time))
		return tmpTime
	except ValueError :
		print 'Value of time out of range.'
		return 0
	except:
		return 0

def get_query_params():
	subreddit = request.args.get('subreddit')
	fromTime  = request.args.get('from')
	toTime    = request.args.get('to')
	keyword   = request.args.get('keyword')
	counter   = 0;
	response  = 'Not enough arguments provided.'

	if subreddit is not None:
		counter += 1

	if toTime is not None and convert_to_date(toTime) and fromTime is not None and convert_to_date(fromTime):
		counter += 	2
	else:
		response = 'Invalid data format.'

	if keyword is not None and subreddit is not None:
		counter += 1

	if counter == 3:
		return WatchRequest(subreddit, convert_to_date(fromTime), convert_to_date(toTime), '')

	if counter == 4:
		return WatchRequest(subreddit, convert_to_date(fromTime), convert_to_date(toTime), keyword)

	return response


def get_query_data(query):
	submissionCount = subs.count({"subreddit": query.subreddit, "created": {'$gte': query.fromTime, '$lte': query.toTime}})
	if (submissionCount):
		submissions = subs.find({"subreddit": query.subreddit, 'created': {'$gte': query.fromTime,'$lte': query.toTime}}).sort('created', -1)


	commentCount    = coms.count({"subreddit": query.subreddit, "created": {'$gte': query.fromTime, '$lte': query.toTime}})
	if (commentCount):
		comments    = coms.find({"subreddit": query.subreddit, 'created': {'$gte': query.fromTime,'$lte': query.toTime}}).sort('created', -1)

	if commentCount and submissionCount:
		data 		= [x for x in chain(comments, submissions)]
		dataList 	= list(data)
		x 			= dumps(dataList)
		return x

	if commentCount:
		commentData	= list(comments)
		x 			= dumps(commentData)
		return x

	if submissionCount:
		submissionData	= list(submissions)
		x 				= dumps(submissionData)
		return x

	return 'No data currently available.'


def get_query_data_keyword(query):
	submissionCount = subs.count({"subreddit": query.subreddit, "created": {'$gte': query.fromTime, '$lte': query.toTime}, '$text':{'$search': query.keyword}})
	if (submissionCount):
		submissions = subs.find({"subreddit": query.subreddit, 'created': {'$gte': query.fromTime,'$lte': query.toTime}, '$text':{'$search': query.keyword}}).sort('created', -1)


	commentCount    = coms.count({"subreddit": query.subreddit, "created": {'$gte': query.fromTime, '$lte': query.toTime}, '$text':{'$search': query.keyword}})
	if (commentCount):
		comments    = coms.find({"subreddit": query.subreddit, 'created': {'$gte': query.fromTime,'$lte': query.toTime}, '$text':{'$search': query.keyword}}).sort('created', -1)

	if commentCount and submissionCount:
		data 		= [x for x in chain(comments, submissions)]
		dataList 	= list(data)
		x 			= dumps(dataList)
		return x

	if commentCount:
		commentData	= list(comments)
		x 			= dumps(commentData)
		return x

	if submissionCount:
		submissionData	= list(submissions)
		x 				= dumps(submissionData)
		return x

	return 'No data currently available.'

@app.route('/')
def show_home_instructions():
	return 'This is the home page, access the "/items/?subredit= your-subreddit-here &from=your-start-time-here &to=your-end-time-here" to get a list of submissions and their comments from your subreddit in the interval you defined. You can also enter something like "/items/?subredit= your-subreddit-here &from=your-start-time-here &to=your-end-time-here &keyword=your-keyword" to get a list of submissions and their comments from your subreddit containing your keyword.'



@app.route('/items/', methods=['GET'])
def show_args():
	watch = get_query_params()
	if not isinstance(watch, basestring):
		if watch.keyword == '':
			return get_query_data(watch)
		else:
			return get_query_data_keyword(watch)
	else:
		return watch



