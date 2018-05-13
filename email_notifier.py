from imapclient import IMAPClient
import time
import RPi.GPIO as GPIO

#Set up LEDs and buzzer
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 22
RED_LED = 24
BUZZER = 18
GPIO.setup(GREEN_LED,GPIO.OUT)
GPIO.setup(RED_LED,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)

GPIO.output(GREEN_LED, False)
GPIO.output(RED_LED, False)
GPIO.output(BUZZER, False)


FROM_FILTER_1 = ["sender1","sender2","sender3"] #"FROM" filter of senders that will have their own LED.
HOSTNAME = "imap.gmail.com"
USERNAME = "user@email.com" #Placeholder for username.
PASSWORD = "" # For security reasons, PASSWORD is inserted as an input when the program runs; see below.

def buzz(duration=1):
    """
    Buzzer is activated for "duration" seconds.
    """
    GPIO.output(BUZZER, True)
    time.sleep(duration)
    GPIO.output(BUZZER, False)

def blink_red(step=.5, total_time=60):
    """
    Red LED is switched on and off in "step" steps for "total_time" seconds.
    Used to indicate there is an error, so it can be spotted even in the headless mode.
    """
    print("Connection failed.")
    print("Retrying...")
    while total_time > 0:
        GPIO.output(RED_LED, True)
        time.sleep(step)
        GPIO.output(RED_LED, False)
        time.sleep(step)
        total_time -= step*2
        print(int(total_time))


def loop(total_time=120):
    """
    Checks email every "total_time" seconds.
    Applies filter, activates corresponding LEDs and buzzer, displays number of
    unread messages from the filter and the rest on the screen.
    The LEDs remain active as long as the messages are unread; the buzzer only buzzes once.
    """
    print("Trying to connect...")
    server = IMAPClient(HOSTNAME, use_uid = True, ssl = True)
    server.login(USERNAME,PASSWORD)
    print("Logging in as " + USERNAME)
    select_info = server.select_folder("Inbox", readonly = True)

    messages_filter_1 = []
    other_messages = server.search(["UNSEEN"])

    for sender in FROM_FILTER_1:
        messages_filter_1 += server.search(["UNSEEN","FROM",sender])

    other_messages = [x for x in other_messages if x not in messages_filter_1]
    print("Unread messages from filter:" + str(len(messages_filter_1)))
    print(("Other unread messages:" + str(len(other_messages))))

    server.logout()
    print("Logged out")
    
    if messages_filter_1:
        #Check if the green light is already on; the buzzer only buzzes when the unread
        #emails are seen for the first time.

        if GPIO.input(GREEN_LED) == 0:
            GPIO.output(GREEN_LED, True)
            buzz()

    else:
        GPIO.output(GREEN_LED, False)
    if other_messages:
        GPIO.output(RED_LED, True)
    else:
        GPIO.output(RED_LED, False)

    #Check emails every "total_time" seconds.
    print("Checking again in {} seconds...".format(total_time))
    while total_time > 0:
        print(total_time)
        time.sleep(1)
        total_time -= 1
        
if __name__== "__main__":
    PASSWORD = input("Password: ") #Password not stored for security reasons.
    try:
        while True:
            try:
                    loop()
            except Exception as e:
                print(e)
                blink_red()
    finally:
        GPIO.cleanup()
