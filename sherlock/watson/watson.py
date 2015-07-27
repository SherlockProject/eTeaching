import inspect, os, requests
from copy import copy

# Instantiate a BlueMix Watson service API
class WatsonService:
	def __init__( self, **kwargs ):
		self.auth		= kwargs['auth'];
		self.api_url	= kwargs['url'];

		for name, obj in kwargs['operations'].items():
			def request(
				self,
				method = obj['method'].upper(),
				path = obj['path'],
				headers = None,
				params = None,
				files = None,
				data = None,
				name = name
			):
				# Set parameters in 'path'
				if params is not None:
					for i in params:
						path = path.replace( '{' + i + '}', params[i] );

				if( method == 'POST' ):
					data = params;
					params = None;

				response = requests.request(
					method,
					self.api_url + path,
					auth = self.auth,
					params = params,
					files = files,
					data = data );

				return response.content;

			setattr( WatsonService, name, request );