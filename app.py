from selenium import webdriver
import time
from bs4 import BeautifulSoup
from twilio.rest import Client
import threading

''' Twilio Information '''
ACCOUNT_SID = '' 	# Fill in
AUTH_TOKEN = '' 	# Fill in
TWILIO_NUMBER = '' 	# Fill in
CELL_NUMBER = '' 	# Fill in
''' Login Info '''
USERNAME = '' 		# Fill in
PASSWORD = '' 		# Fill in

__client = Client(ACCOUNT_SID, AUTH_TOKEN)

def check():
	"""
	Checks for messages to get assignments
	:return:
	"""
	print("Checking for texts")
	messages = __client.messages.list()
	for msg in messages:
		msg_low = msg.body.lower()
		if msg.from_ == CELL_NUMBER and ("homework" in msg_low or "hw" in msg_low):
			print("Found text, getting assignments...")
			get_assignments()
			msg.update(body="") # Redact message
			return

def get_assignments():
	"""
	Get the assignments and send the formatted text
	:return:
	"""
	text = get_events()
	send_text(text, CELL_NUMBER)

def send_text(text, number):
	"""
	Sends the specified text to the specified number
	:param text: The text to send
	:param number: Who to send it to
	:return:
	"""
	print("Sending text")
	__client.messages.create(body=text,from_=TWILIO_NUMBER, to=number)

def format_assignments(assignments, dates):
	"""
	Format the assignments for a text
	:param assignments: The dictionary of assignments { class 1: [assignment 1, ..., assignment n], class 2 ...etc }
	:param dates: The dictionary of due dates { class+assignment (in case of 2 class with the same assignment name) : date, etc... }
	:return: Formatted text
	"""
	print("Formatting...")
	format_text = "Assignments\n"
	for key in assignments:
		format_text += "Class: " + key + "\n"
		for t in assignments[key]:
			format_text += " - " + t + " (Due: " + dates[key+t] + ")\n"
		format_text += "\n"
	return format_text



def get_html():
	"""
	Returns the html from selenium for beautiful soup to parse
	:return: HTML source from selenium
	"""
	URL = 'https://moodle.sonoma.edu/C/calendar/view.php'

	browser = webdriver.Chrome(r'driver\chromedriver.exe')
	browser.get('http://login.sonoma.edu')
	username = browser.find_element_by_id('username')
	password = browser.find_element_by_id('password')

	username.send_keys(USERNAME)
	password.send_keys(PASSWORD)

	browser.find_element_by_name("submit").click()
	time.sleep(2)
	browser.get('https://moodle.sonoma.edu/C/login/')
	browser.find_element_by_link_text('CAS users').click()
	browser.get(URL)

	html = browser.page_source

	soup = BeautifulSoup(html, "html.parser")
	return soup

def get_events():
	"""
	Gets the events from the html source and formats them
	:return: The formatted text
	"""
	print("Getting events...")
	assignments = dict()
	dates = dict()
	events = get_html().findAll("div", { 'class' : 'event' })

	for e in events:
		title = e.find_all("h3")[0]
		course = e.find_all("div")[0]
		d = e.findAll("span", { 'class' : 'date' })[0]
		if course.text + title.text not in dates:
			dates[course.text + title.text] = d.text
		if course.text not in assignments:
			assignments[course.text] = [title.text]
		else:
			assignments[course.text].append(title.text)

	return format_assignments(assignments, dates)

def init():
	"""
	Init the thread to check every minute
	:return:
	"""
	threading.Timer(60, init).start()
	print('\nChecking message history for videos about every minute. Currently:',
		  time.strftime("%c"))
	check()

if __name__ == "__main__":
	""" Start the program """
	init()

