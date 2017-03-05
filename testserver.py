import unittest, datetime, time
import server
 
class TestServer(unittest.TestCase):
 
	def setUp(self):
		self.app = server.app.test_client()
 
	def test_date_9999999999999(self):
		self.assertEqual( server.convert_to_date(9999999999999), 0)

	def test_get_home(self):
		response = self.app.get('/')
		assert response.data == 'This is the home page, access the "/items/?subredit= your-subreddit-here &from=your-start-time-here &to=your-end-time-here" to get a list of submissions and their comments from your subreddit in the interval you defined. You can also enter something like "/items/?subredit= your-subreddit-here &from=your-start-time-here &to=your-end-time-here &keyword=your-keyword" to get a list of submissions and their comments from your subreddit containing your keyword.'

	def test_get_not_enough_arguments(self):
		response = self.app.get('/items/?from=lalalala')
		assert response.data == 'Invalid data format.'

		response = self.app.get('/items/?subreddit=lalalala&from=lalala')
		assert response.data == 'Invalid data format.'

		response = self.app.get('/items/?subreddit=lalalala&to=1488724383&keyword=asas')
		assert response.data == 'Invalid data format.'

		response = self.app.get('/items/?from=1488724383&to=1488724383&keyword=asas')
		assert response.data == 'Not enough arguments provided.'

	def test_get_no_data_available(self):
		response = self.app.get('/items/?subreddit=python&from=1488724383&to=1488724383')
		assert response.data == 'No data currently available.'

	def test_get_data_available(self):
		response = self.app.get('/items/?subreddit=Python&from=1488378783&to=1488724383')
		assert response.data != 'No data currently available.'

	def test_get_data_available_keyword(self):
		response = self.app.get('/items/?subreddit=Python&from=1488378783&to=1488724383&keyword=python')
		assert response.data != 'No data currently available.'


 
if __name__ == '__main__':
    unittest.main()