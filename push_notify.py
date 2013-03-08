#!/usr/bin/env python
#tryboxcar.py

import boxcar
import datetime
import sys

boxcar = boxcar.BoxcarApi('wM85GfAILCaobtRJgTyZ', 
		'hEXeN0ASeJP1XXv5XzhkabhYn4VXT7GaFIzreNn2',
		'http://banrai.com/images/nycfun_logo_57x57.png')

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print 'USAGE: %s to_email subject msg' % sys.argv[0]
		sys.exit()
	msg_to = sys.argv[1]
	msg_subject = sys.argv[2]
	msg_body = ' '.join(sys.argv[3:])
	boxcar.notify(msg_to, msg_subject, msg_body)
		#message_id=int(datetime.now().strftime('%f')) % 1000))