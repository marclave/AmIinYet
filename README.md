AmIinYet
========

AmIinYet is an application that lets you automate registering for a waitlisted course at UVic.

##Requirements

1. Python is installed (Tested with version Python 2.6.8)
2. mechanize library is installed [Mechanize download!](http://wwwsearch.sourceforge.net/mechanize/download.html)
3. PyYAML libray is installed [PyYAML download!](pyyaml.org/wiki/PyYAML)

##Setup
Clone this repository:
```
git clone https://github.com/marclave/AmIinYet.git
```
Modify the profile to include your information, example:
```
UVIC_LOGIN:
  USERNAME: astudent
  PASSWORD: cleverPassword
SEMESTER:
  FIRST: "First Term: Sep - Dec 2014"
  SUMMER: "Summer Session: May - Aug 2015"
  SECOND: "Second Term: Jan - Apr 2015"
DESIRED_SEMESTER:
  SECOND
GMAIL:
  ADDRESS: A.STUDENT@gmail.com
  PASSWORD: lessCleverPassword
CRN:
  - 101010
```

Then test run:
```
python AmIinYet.py
```
Now you can setup a cron to run this script, example to run everyday at midnight:
```
0 23 * * * python /path/to/script/AmIinYet/AmIinYet.py
```
If you run windows, set up a Windows Task Scheduler
 
##Description

When run, AmIinYet logs into UVic's website, checks your waitlisted courses and attempts to register. If the waitlisted course is registered successfully, you will recieve an email with this notification.

Developed for simple use, AmIinYet uses a profile where all the required information is stored and used.
