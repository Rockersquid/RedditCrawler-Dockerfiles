import unittest, datetime, time, json, crawler

 
class TestCrawler(unittest.TestCase):
 
	def setUp(self):
		pass

	def test_check_valid_subreddit(self):
		self.assertEqual(crawler.check_valid_subreddit('python'), 1)
		self.assertEqual(crawler.check_valid_subreddit('maneadadale'), 0)

	def test_get_subreddit_list(self):
		with open('test.json') as data_file:    
		    data = json.load(data_file)
		self.assertEqual(crawler.get_subreddit_list(data), 'python+manele')
		self.assertEqual(crawler.get_subreddit_list('asdfadf'), '')

	def test_deleteOldData(self):
		self.assertEqual(crawler.delete_old_data(crawler.coms), 1)
		self.assertEqual(crawler.delete_old_data(''), 0)

 
if __name__ == '__main__':
    unittest.main()