import pycurl
import json
import cStringIO
import urllib

class DrupalRest:
	host = ''
	endpoint = ''
	username = ''
	password = ''
	session = ''
	csrf_token = ''
	
	def __init__(self, host, endpoint, username, password):
		self.host = host
		self.endpoint = endpoint
		self.username = username
		self.password = password
	
	def drupalLogin(self):
		user = {'username': self.username, 'password': self.password}
		postData =  urllib.urlencode(user)
		
		response = cStringIO.StringIO()
		login_request_url = self.host + self.endpoint + 'user/login.json'
		c = pycurl.Curl()
		c.setopt(pycurl.URL, login_request_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
		c.setopt(pycurl.HTTPHEADER, ['Content-type: application/x-www-form-urlencoded'])
		c.setopt(pycurl.WRITEFUNCTION, response.write)
		c.setopt(pycurl.POST, 1)

		c.setopt(pycurl.POSTFIELDS, postData)
		c.perform()
		c.close()
		
		result_json = response.getvalue()
		result = json.loads(response.getvalue())
		self.session = str(result['session_name'] + '=' + result['sessid'])
		
		csrf_token_str = cStringIO.StringIO()
		#very important is that here the URL is without the endpoint
		csrf_token_request_url = self.host + 'services/session/token'
		z = pycurl.Curl()
		z.setopt(pycurl.URL, csrf_token_request_url)
		z.setopt(pycurl.WRITEFUNCTION, csrf_token_str.write)
		cookie = 'Cookie: ' + self.session
		z.setopt(pycurl.COOKIE, self.session)

		z.perform()
		z.close()
		self.csrf_token = str(csrf_token_str.getvalue())

		
	def retrieveNode(self, nid):
		response = cStringIO.StringIO()
		
		c = pycurl.Curl()
		node_request_url = self.host + self.endpoint + 'node/' + str(nid) + '.json'
		c.setopt(pycurl.URL, node_request_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])

		c.setopt(pycurl.COOKIE, self.session)
		c.setopt(pycurl.WRITEFUNCTION, response.write)
		c.perform()
		c.close()
		
		result_json = response.getvalue()
		result = json.loads(response.getvalue())
		return result

	def createNode(self, node):
		
		response = cStringIO.StringIO()
		
		request_url = self.host + self.endpoint + 'node.json'
		postData = urllib.urlencode(node)

		c = pycurl.Curl()
		c.setopt(pycurl.URL, request_url)
		
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
		c.setopt(pycurl.HTTPHEADER, ['Content-type: application/x-www-form-urlencoded'])
		
		c.setopt(pycurl.COOKIE, self.session)
		
		csrf_token_header = 'X-CSRF-Token: ' + self.csrf_token
		c.setopt(pycurl.HTTPHEADER, [csrf_token_header])
		c.setopt(pycurl.WRITEFUNCTION, response.write)

		c.setopt(pycurl.POST, 1)
		#c.setopt(pycurl.VERBOSE, 1)
		

		c.setopt(pycurl.POSTFIELDS, postData)
		c.perform()
		c.close()
		
		result_json = response.getvalue()
		result = json.loads(response.getvalue())
		
		return result

	def createFile(self, file_data):
		
		response = cStringIO.StringIO()
		
		file_request_url = self.host + self.endpoint + 'file.json'
		postData = urllib.urlencode(file_data)

		c = pycurl.Curl()
		c.setopt(pycurl.URL, file_request_url)
		
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
		c.setopt(pycurl.HTTPHEADER, ['Content-type: application/x-www-form-urlencoded'])
		
		c.setopt(pycurl.COOKIE, self.session)
		csrf_token_header = 'X-CSRF-Token: ' + self.csrf_token
		c.setopt(pycurl.HTTPHEADER, [csrf_token_header])
		c.setopt(pycurl.WRITEFUNCTION, response.write)
		c.setopt(pycurl.POST, 1)

		c.setopt(pycurl.POSTFIELDS, postData)
		c.perform()
		c.close()
		
		result_json = response.getvalue()
		result = json.loads(response.getvalue())
		
		return result
