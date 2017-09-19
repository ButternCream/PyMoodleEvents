# Py Moodle Events

## Packages
```
pip3 install BeautifulSoup selenium twilio
```
or
```
easy_install BeautifulSoup selenium twilio
```

## Fill In Information
```
import TwilInfo # Remove

''' Twilio Information '''
ACCOUNT_SID 	= TwilInfo.ACCOUNT_SID 		# Change
AUTH_TOKEN 		= TwilInfo.AUTH_TOKEN 		# Change
TWILIO_NUMBER 	= TwilInfo.TWILIO_NUMBER 	# Change
CELL_NUMBER 	= TwilInfo.CELL_NUMBER 		# Change
''' Login Info '''
USERNAME 		= TwilInfo.USERNAME 		# Change
PASSWORD 		= TwilInfo.PASSWORD 		# Change
```

*Note: Built using SSU's moodle*

Change thr URL's in get_html() to adjust to your moodle domain