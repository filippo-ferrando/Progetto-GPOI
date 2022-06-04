import lib.config
import lib.foo

#global offsetTagDict
#offsetTagDict = {}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# LOGGING PLATFORM
logging.basicConfig(filename=config.LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)

#PID CONTROL
f = open("config.PID_FILE_NAME", "w")
f.write(f"{os.getpid()}")
f.close()

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def connection_control():
    if connect():
        logging.debug(f"Connected to internet")
    else:
        logging.debug(f"{datetime.now()} - Killing process")
        os._exit(0)

'''
class tagController(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        global offsetTagList
        while self.running:
            for element in offsetTagDict.values():
                if int((time.time() - element)) >= 30:
                    wKey = list(offsetTagDict.keys())[list(offsetTagDict.values()).index(element)]
                    offsetTagDict.pop(wKey)
'''

class raspberry():
    def __init__(self):
        #NETSONS CRED
        self.api = foo.API_LINK
        self.password = foo.RASP_PASSWORD

        #LED SETUP
        self.Rled = 11
        GPIO.setup(self.Rled,GPIO.OUT)
        self.Gled = 13
        GPIO.setup(self.Gled,GPIO.OUT)

        #BUZZER SETUP
        self.buzzer = Buzzer(26)
        self.rc522 = RFID()


        connection_control()

    def reader(self):
        #global offsetTagDict
        try:
            print("ready: ")
            #print('Waiting for the badge: ')

            self.rc522.wait_for_tag()
            (error, tag_type) = self.rc522.request()

            #if not error : 
            (error, uid) = self.rc522.anticoll()

            #if not error :
            uid = "".join(str(l) for l in uid)
            print(f'badge : {uid}')
            logging.debug(f"{datetime.now()} - Successfull read")
            time.sleep(0.5)

            return uid
        except:
            #READING FAILED
            print("chiusura")
            logging.critical(f"{datetime.now()} - killing process")
        '''
        if uid in offsetTagDict:
            uid = 403
        else:
            offsetTagDict[uid] = time.time()
            return uid
        '''

        

    def send(self, uid):
        '''
        if uid == 403:
            self.repeated_tag()
        else:
            http = requests.post(self.api,data={'uid' : uid, 'password' : self.password, 'modalita' : "modalita"})
            return http.text
        '''
        connection_control()

        http = requests.post(self.api,data={'uid' : uid, 'password' : self.password, 'modalita' : "modalita"})
        #print(http.text)
        logging.debug(f"{datetime.now()} - UID {uid} Sended")
        return http.text

    def startup(self):
        #IN HEADLESS MODE YOU CAN LISTEN TO THE STARTUP SOUND
        GPIO.output(self.Gled, GPIO.HIGH)
        GPIO.output(self.Rled, GPIO.HIGH)
        self.buzzer.on()
        time.sleep(0.7)
        self.buzzer.off()
        time.sleep(0.3)
        self.buzzer.on()
        time.sleep(0.7)
        self.buzzer.off()
        GPIO.output(self.Gled, GPIO.LOW)
        GPIO.output(self.Rled, GPIO.LOW)

    def bip(self, resp):
        #POSITIVE OR NEGATIVE RESPONSE (DEPENDS ON API RESPONSE)
        if resp == "si":
            logging.debug(f"{datetime.now()} - Positive Response")
            GPIO.output(self.Gled, GPIO.HIGH)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            time.sleep(0.3)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            GPIO.output(self.Gled, GPIO.LOW)
        elif resp == "no":
            logging.debug(f"{datetime.now()} - Negative Response")
            GPIO.output(self.Rled, GPIO.HIGH)
            self.buzzer.on()
            time.sleep(1)
            self.buzzer.off()
            GPIO.output(self.Rled, GPIO.LOW)
        elif resp == "password":
            logging.debug(f"{datetime.now()} - 500 : Internal server error ")
            print("PASSWORD SBAGLIATA")

    '''
    def repeated_tag(self):
        GPIO.output(self.Rled, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.Rled, GPIO.LOW)
    '''    


def main():
    rasp = raspberry()

    #controlList = tagController()
    #controlList.start()

    rasp.startup()


    while True:
        try: 
            time.sleep(3)
            uid = rasp.reader()
            resp = rasp.send(uid)
            rasp.bip(resp)
        except KeyboardInterrupt:
            print("chiudo")

if "__name__" == "__main__":
    main()