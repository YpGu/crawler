'''
Created on June 6, 2014

@author Rainicy
'''

import re
from datetime import *

def writeLog(log, time, content):
	'''
	Description: Record a log in one-time crawling News Articles. 
				 And write it to the news.log

	@param: 
		log:        directory of the log file 
		time:       the starting time
                content:    content of the exception
	'''

	with open(log, 'a') as fp:
		fp.write('%s\t%s\n'% (time, str(content)))
		fp.close()

