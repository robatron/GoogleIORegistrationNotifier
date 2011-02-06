#! /usr/bin/env python
'''
Google IO Registration Notifier

Send a barrage of notifications to the specified email addresse(s) and phone
number(s) (via SMS text message) when the Google IO registration page changes 
at all, indicating that registration might be open.

You'll need a Google Voice account to for sending SMS notifications.

Dependencies:
    * Python >= v2.6
    * pygooglevoice >= v0.5 (http://code.google.com/p/pygooglevoice/)
'''
import time
import urllib
import smtplib
from email.mime.text import MIMEText
from googlevoice import Voice
from googlevoice.util import LoginError as GVLoginError
from settings import *

# --------
# globals
# --------
# I know, I know... Don't judge me. Google Voice complains if you try to use an
# authenticated Voice object passed by value into a function.
SMTPServ = smtplib.SMTP()   # temporary, local SMTP server
GVoice = Voice()            # Google Voice object for texting

# -----
# main
# -----
def main():
    ''' main '''
    print '---------------------------------'
    print ' Google IO Registration Notifier '
    print '---------------------------------'
    print 'page check interval set to %s seconds'%INTERVAL_SEC
    print 'connecting to local SMTP server...'
    print 'emails will be sent as %s.'%FROM_EMAIL
    SMTPServ.connect()
    print 'please log in to Google Voice:'
    try:
        GVoice.login()
    except GVLoginError:
        print 'Google Voice login failed. Exiting.'
        exit(1)
    print 'sending text(s) and email(s) reporting notifier start...'
    sendEmails('Google IO Registration Notifier started.',
            'What it says on the label. (%s)'%timestamp())
    sendTexts('Google IO Registration Notifier started. (%s)'%timestamp())
    print 'entering main page checker loop...'
    checker()
    print 'stopping local SMTP server...'
    SMTPServ.quit()
    print 'done!'
    exit(0)

# ------------------
# page checker loop
# ------------------
def checker():
    ''' 
    Continually check the registration page for changes at the specified
    interval. If anything changes, send notifications.
    '''
    oldPage = urllib.urlopen(REGISTRATION_URL).read()
    print '%s starting to check page %s...'%(timestamp(), REGISTRATION_URL)
    while True:
        try:
            time.sleep(INTERVAL_SEC)
            newPage = urllib.urlopen(REGISTRATION_URL).read()
            if newPage != oldPage:
                print '%s ** REGISTRATION PAGE HAS CHANGED!! **'%timestamp()
                print 'sending barrage of notifications...'
                sendEmails('Google IO registration page has changed!!',
                        'Google IO registration page has changed!! ' +
                        'Get your butt over to the Google IO registration ' +
                        'page (%s) '%REGISTRATION_URL + 
                        'and get those tickets! (%s)'%timestamp())
                sendTexts('Google IO registration page has changed!! Get ' +
                        'your butt over to the Google IO registration page ' +
                        '(%s) '%REGISTRATION_URL + 
                        'and get those tickets! (%s)'%timestamp())
                oldPage = newPage
            else:
                print '%s Registration page is the same.'%timestamp() 
                print 'Checking again in %s seconds...'%INTERVAL_SEC
                oldPage = newPage
        except KeyboardInterrupt:
            print 'aught Ctrl-c.'
            print 'stopping page checking...'
            break

# ----------
# notifiers
# ----------
def sendEmails(subject, message):
    ''' send an email to specified addresses '''
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = str(EMAIL_RECIPIENTS)
    print 'sending email(s) "%s" to %s'%(msg['Subject'],EMAIL_RECIPIENTS)
    SMTPServ.sendmail(FROM_EMAIL, EMAIL_RECIPIENTS, msg.as_string())

def sendTexts(message, nrCopies=1, sleepInterval=1):
    ''' 
    Send specified number of texts to the specified numbers.

    ``message`` is the text message to send, ``nrCopies`` is the number of 
    copies of texts to send, and ``sleepInterval``  is the time between the 
    texts in seconds, which only matters if nrCopies > 1.
    '''
    print 'sending %s text(s) to %s...'%(nrCopies, TEXT_RECIPIENTS)
    for i in range(nrCopies):
        for number in TEXT_RECIPIENTS:
            print 'sending text "%s" to %s...'%(message, number)
            GVoice.send_sms(number, message)
        if nrCopies > 1 and i < nrCopies - 1:
            print 'sleeping for %d second(s) before sending another copy...'\
                    %sleepInterval
            time.sleep(sleepInterval)

# -------------
# misc helpers
# -------------
def timestamp():
    ''' return the current timestamp '''
    return time.strftime("%Y-%m-%d %H:%M:%S") 

# start the prog once it's fully loaded
if __name__ == '__main__':
    main()
