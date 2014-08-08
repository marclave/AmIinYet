import re, mechanize, yaml, smtplib, os, platform, sys

UVIC_URL = "https://www.uvic.ca/"
WAITLIST_URL = UVIC_URL + "BAN2P/bwyskreg.p_course_wait"
MYPAGE_URL = UVIC_URL + "cas/login?service=" + UVIC_URL + "mypage/Login"

if platform.system() == 'Windows':
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\"
else:
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/"

def testingMode(br, profile):

	print "\nTESTING MODE ENABLED\n"	
	print "TESTING UVIC LOGIN..."
	login(br, profile)
	
	print "\nTESTING EMAIL..."
	sendEmail(profile, profile['CRN'][0])

	print "\nDISPLAYING CRNS"
	for course in profile['CRN']:
		print course
	
	print"\nDESIRED SEMESTER"
	print profile['SEMESTER'][profile['DESIRED_SEMESTER']]
	
	print "\nTESTING COMPLETE\n"
	print "REVIEW OUTPUT FOR ERRORS BEFORE IMPLEMENTATION"
	
	
def login(br, profile): 
	
	br.open(MYPAGE_URL)
	br.select_form("credentials")

	userNameControl = br.form.find_control("username")
	userNameControl.value = profile['UVIC_LOGIN']['USERNAME']
	passwordControl = br.form.find_control("password")
	passwordControl.value = profile['UVIC_LOGIN']['PASSWORD']

	br.submit()
	if bool(re.search("The credentials you entered do not match our records",br.response().read())):
		print "LOGIN FAILED!"
		print "CHECK UVIC LOGIN USERNAME AND PASSWORD"
	else:
		print "LOGIN SUCCESSFUL"

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
	print ""
	
	profile = yaml.safe_load(open(WORKING_DIRECTORY + "profile.yml", "r"))	
	br = mechanize.Browser()
	
	if len(sys.argv) > 1 and sys.argv[1] == "--test":
		testingMode(br, profile)
	else:		
		login(br, profile)
		selectTerm(br, profile)
		register(br, profile)
