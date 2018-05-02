import json
import logging
import string
import re



logger = logging.getLogger(__name__)

class Properties:

	PATTERN_EXISTS = re.compile(".*$[^$].*")
	def __init__(self,properties_file):
		self.filename = properties_file
		self.props = {}	
		self.load_properties()


	def load_properties(self):
		logger.debug("[Loading]Loading properties from %s", self.filename)
		with open(self.filename) as f:
			for line in f:
				try:
					k,v = line.split("=")
					k ,v= k.strip(),v.strip()
					self.props[k] = v
				except:
					logger.error("[Loading] Skipping line: %s", line)
					pass
		logger.debug("[Loading]Completed loading properties: %s", json.dumps(self.props, indent=1))
		
	def get_property(self,key):
		'''TODO: handle escape sequence'''
		ret = string.Template(self.props[key]).substitute(self.props)
		while '$' in ret: 
			ret = string.Template(ret).substitute(self.props)

		logger.debug("[Eval] %s = %s",key, ret)
		return ret

class Actions:
	def execute(self):
		pass
	
class RESTAction(Actions):
	def __init__(method, url, headers={}, body=None):
		self.method = method
		self.url = url
		self.headers = headers
		self.body = body

	def execute(self):
		req_handle= None
		if method == GET:
			req_handle = requests.get
		if method == POST:
			req_handle = requests.post
		if method == PUT:
			req_handle = requests.put
		if method == DELETE:
			req_handle = requests.delete


		resp = req_handle(url, headers=headers, data=body)

		print resp.status_code
		print resp.text

		

if __name__ == "__main__":
	logging.basicConfig(filename='logs.log', level=logging.DEBUG)
	props = Properties("/home/rahul/Documents/props.properties")
	print props.get_property('key1.sub1')
