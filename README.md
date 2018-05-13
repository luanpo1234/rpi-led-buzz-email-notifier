# Email notifier for Raspberry Pi with LEDs and buzzer

Used on Raspberry Pi 3 B+, should work with earlier versions.

The two different LEDs are meant to differentiate email notification according to filters; more LEDs and filters could be added.

Coded on Python 3.6.

## Prerequisites

* Raspberry Pi (tested on Raspberry Pi 3 and 3 B+, should work with earlier versions)
* Breadboard
* 2 LEDs (preferably with different colors)
* 1 buzzer
* 2 330 Ohm resistors
* 4 jumper wires

## Layout for LEDs and buzzer
I used the exact layout from the CamJam Edukit #2, worksheet 2: 
https://github.com/CamJam-EduKit/EduKit2/blob/master/CamJam%20Edukit%202%20-%20RPi.GPIO/CamJam%20EduKit%202%20-%20Sensors%20Worksheet%202%20(RPi.GPIO)%20-%20LEDs%20and%20Buzzer.pdf

## Motivation

I found similar projects available online, but there were some issues I tried to address:
1. Having a visible countdown on the monitor and being able to kill the program immediately when I'm done.
2. Having different filters for the e-mails.
3. Having a blinking light to indicate errors on headless mode; during my tests, sometimes the connection failed and I didn't realize it because there was no way of telling from the LEDs.

## Setup
The variables FROM_FILTER_1, HOSTNAME, USERNAME have placeholders as values in the email_notifier.py. Change them accordingly.

imap.gmail.com is set as default for the HOSTNAME: please note that gmail blocks this kind of access unless you change the security settings.

You can read more about this here: https://support.google.com/accounts/answer/6010255?hl=en.

## Contributions
Suggestions and useful additions will be much appreciated.
