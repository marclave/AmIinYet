import re, mechanize, yaml, smtplib, os, platform

UVIC_URL = "https://www.uvic.ca/"
WAITLIST_URL = UVIC_URL + "BAN2P/bwyskreg.p_course_wait"
MYPAGE_URL = UVIC_URL + "cas/login?service=" + UVIC_URL + "mypage/Login"

if platform.system() == 'Windows':
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\"
else:
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/"

def login(br, profile): 
	
	br.open(MYPAGE_URL)
	br.select_form("credentials")

	userNameControl = br.form.find_control("username")
	userNameControl.value = profile['UVIC_LOGIN']['USERNAME']
	passwordControl = br.form.find_control("password")
	passwordControl.value = profile['UVIC_LOGIN']['PASSWORD']

	br.submit()

def selectTerm(br, profile):

	br.open(WAITLIST_URL)
	
	# Regex to get the correct dropdown value for the DESIRED_SEMESTER
	termSelectValue = re.search('\<OPTION VALUE\=\"([0-9]+)\"\>%s'%profile['SEMESTER'][profile['DESIRED_SEMESTER']], br.response().read())
	termSelectValue = str(termSelectValue.group(1))

	# Selecting the term select form
	br.form = list(br.forms())[1]  # Used because the form name was not named

	termSelectControl = br.form.find_control("term_in")
	termSelectControl.value = [termSelectValue]

	br.submit()

# TODO successfully register for a course
def register(br, profile):

	formNumber = 0

	for course in profile['CRN']:
		for form in br.forms():
			for control in form.controls:				
				if control.name == "wait_status_in":
					# TODO NEED TO FIND OUT REGISTER SYMBOL, ASSUMING IT IS R BUT UVIC MAY LACK LOGIC
					courseInput = "R " + str(course)
					try:
						br.form = list(br.forms())[formNumber]  # use when form is unnamed
						registerClassControl = br.form.find_control(control.name)
						registerClassControl.value = [courseInput]
						br.submit()
						#sendEmail(profile, course)
						print "REGISTERED FOR COURSE " + str(course)
					except mechanize._form.ItemNotFoundError:
						print "COULD NOT REGISTER COURSE, CHECK IF CRN IS CORRECT"
			formNumber += 1


def sendEmail(profile, course):

	sender = "AmIinYet <AmIinYet@example.com>"
	recipient = profile['UVIC_LOGIN']['USERNAME'] + "@uvic.ca"
	subject = "Registered in your course" + str(course)
	body = "You have been registered in " + str(course) 

	message = "\From: %s\nTo: %s\nSubject: %s\n\n%s "%(sender, recipient, subject, body)

	try:
		emailSession = smtplib.SMTP("smtp.gmail.com", 587)
		emailSession.ehlo()
		emailSession.starttls()

		emailSession.login(profile['GMAIL']['ADDRESS'], profile['GMAIL']['PASSWORD'])
		emailSession.sendmail(sender, recipient, message)
		emailSession.close()

		print "EMAIL SENT SUCCESSFULLY!"

	except:
		print "FAILED TO SEND EMAIL"
		print "CHECK USERNAME/PASSWORD AND NETWORK"

if __name__ == "__main__":
	
	print "================================="
	print "            AmIinYet             "
	print "    Developed by Marc Laventure  "
	print "================================="
	
	profile = yaml.safe_load(open(WORKING_DIRECTORY + "profile.yml", "r"))
	br = mechanize.Browser()

	login(br, profile)
	selectTerm(br, profile)
	register(br, profile)
