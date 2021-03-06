# -*- coding: utf-8 -*-
import logging

from browserdriver import BrowserDriver
from requestsloader import RequestsLoader
from processagent import ProcessAgent
from utils.mk_dir import mk_dir

# Global Vars
from vars_setting import PARMFILE_NAME, DEF_SHEET_NAME, \
						 USERNAME, PASSWORD, BASE_URL, \
						 IS_REMOTE, IS_USER_NEEDED, \
						 HOSTNAME, PORT

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    #filename='app.log',
                    filemode='w'
	)


def download_report(parameter_file=PARMFILE_NAME, host=HOSTNAME, port=PORT, is_remote=IS_REMOTE, \
					username=USERNAME, password=PASSWORD, url=BASE_URL):
	# init the request object from excel parameter file
	try:
		logging.debug('load parameter file')
		loadrequest = RequestsLoader(parameter_file)
	except FileNotFoundError as e:
		logging.error(e)
		raise
	except Exception as e:
		logging.error(e)
		raise

	# get the requests from the request objects, type is list
	# the single request is a dict
	logging.debug('get request reocrds')
	requests = loadrequest.get_requests()

	#init process agent object
	process_agent = ProcessAgent()

	# make up the dirctory in selenium server to store the report for user
	# and return the dirctory name 
	dir_name = mk_dir(username, host)

	# for each of request in the parameter file:
	for request in requests:
		# generate the selenium functions from the request, the funcion
		# is to be executed in selenium server
		request_functions = process_agent.makeup_functions(request)

		#init the browser driver object
		with BrowserDriver(host=host, port=port, is_remote=is_remote, \
					username=username, password=password, url=url, \
					dirname=dir_name) as driver:

			#loop the functions for  the request and involve browser drvier 
			# to run the functions
			for func, value in request_functions.items():
				try:
					process_agent.process_request(driver, func, value)
				except Exception as e:
					raise

if __name__ == '__main__':
	download_report()