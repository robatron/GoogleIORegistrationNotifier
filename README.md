# Google I/O Registration Notifier

Send a barrage of notifications to the specified email addresse(s) and phone number(s) (via SMS text message) when the [Google I/O registration page](http://www.google.com/events/io/2011/register.html) changes at all, indicating that registration may have opened.

## Requirements
 * Python >= v2.6
 * pygooglevoice >= v0.5 ([http://code.google.com/p/pygooglevoice/])
 * A working Google Voice account ([http://voice.google.com])

## Installation
 1. Download the files into a directory of your choice
 1. Copy `settings.py.dist` to `settings.py`
 1. Change the settings to reflect your needs (see comments inside file)
 
## Usage
 1. Run the program with `python GoogleIORegistrationNotifier.py`
 1. Log into Google Voice when it asks

It should send text(s) and email(s) reporting that it has started. It should now be periodically checking the registration page for changes, and send email(s) and text(s) if it finds any.


