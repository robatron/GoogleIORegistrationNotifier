#! /usr/bin/env python
'''
Google I/O Registration Notifier

Send a barrage of notifications to the specified email addresse(s) and phone
number(s) (via SMS text message) when the Google I/O registration page changes 
at all, indicating that registration might be open.

All settings are in ``settings.py`` (or ``settings.py.dist``).

Requirements:
    * Python >= v2.6
    * pygooglevoice >= v0.5 (http://code.google.com/p/pygooglevoice/)
    * A working Google Voice account (http://voice.google.com)

By Rob McGuire-Dale (http://robmd.net), Feb. 2011
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

    if EMAIL_ENABLE:
        print 'email notifications enabled.'
        print 'emails will be sent as %s.'%FROM_EMAIL
        print 'connecting to local SMTP server...'
        SMTPServ.connect()
    else:
        print 'email notifications DISABLED.'

    if TEXT_ENABLE:
        print 'text (SMS) notifications enabled.'
        print 'please log in to Google Voice:'
        try:
            GVoice.login()
        except GVLoginError:
            print 'Google Voice login failed. Exiting.'
            exit(1)
    else:
        print 'text notifications DISABLED'

    if not EMAIL_ENABLE and not TEXT_ENABLE:
        print '** WARNING ** Both text and email notifications are DISABLED.'
    else:
        print 'sending text(s) and email(s) reporting notifier start...'
    
    if EMAIL_ENABLE:
        sendEmails('Google IO Registration Notifier started.',
                'What it says on the label. (%s)'%timestamp())

    if TEXT_ENABLE:
        sendTexts('Google IO Registration Notifier started. (%s)'%timestamp())
    
    print 'entering main page checker loop...'
    checker()
    
    if EMAIL_ENABLE:
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
    iterations = 0
    print '%s starting page-checks on %s...'%(timestamp(), REGISTRATION_URL)
    while True:
        try:
            time.sleep(INTERVAL_SEC)
            print '%s On check #%d (zero-indexed)'%(timestamp(),iterations)
            newPage = urllib.urlopen(REGISTRATION_URL).read()
            if newPage != oldPage:
                print '%s *** REGISTRATION PAGE HAS CHANGED!! ***'%timestamp()
                print '%s sending barrage of notifications...'%timestamp()
                if EMAIL_ENABLE:
                    sendEmails('Google IO registration page has changed!!',
                            'Google IO registration page has changed!! ' +
                            'Get your butt over to the Google IO ' +
                            'registration page (%s) '%REGISTRATION_URL + 
                            'and get those tickets!')
                if TEXT_ENABLE:
                    sendTexts('Google IO registration page has changed!! ' +
                            'Get your butt over to the Google IO ' +
                            'registration page (%s) '%REGISTRATION_URL + 
                            'and get those tickets!',
                            nrCopies=TEXT_COPIES, textInterval=TEXT_INTERVAL)
                oldPage = newPage
            else:
                print '%s registration page is the same.'%timestamp() 
                print '%s checking again in %s seconds...'%(timestamp(),
                        INTERVAL_SEC)
                oldPage = newPage
            iterations += 1
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

def sendTexts(message, nrCopies=1, textInterval=1):
    ''' 
    Send specified number of texts to the specified numbers.
    '''
    print 'sending %s text(s) to %s...'%(nrCopies, TEXT_RECIPIENTS)
    for i in range(nrCopies):
        for number in TEXT_RECIPIENTS:
            print 'sending text "%s" to %s...'%(message, number)
            GVoice.send_sms(number, message)
        if nrCopies > 1 and i < nrCopies - 1:
            print 'sleeping for %d second(s) before sending another copy...'\
                    %textInterval
            time.sleep(textInterval)

# -------------
# misc helpers
# -------------
def timestamp():
    ''' return the current timestamp '''
    return time.strftime("%Y-%m-%d %H:%M:%S") 

# start the prog once it's fully loaded
if __name__ == '__main__':
    main()
