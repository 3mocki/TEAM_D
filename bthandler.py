import asyncore, logging, time, sensor
from bterror import BTError
import threading
from MySqlite import *

logger = logging.getLogger(__name__)

reader = sensor.Reader()
lock = threading.Lock()
global bConnectApp
global gSocket
global gCurTime
global gBoardID
gBoardID = 0
bConnectApp = True

def getAir():
    mySqlite = MySqlite('sensor')
    mySqlite.connectDB()
    mySqlite.deleteTable()
    mySqlite.createTable()
    print (mySqlite.MakeCSVFormatStr(False))
    while True:
        global bConnectApp
        pm = reader.read_pm()
        co = reader.read_co()
        o3 = reader.read_o3()
        no2 = reader.read_no2()
        so2 = reader.read_so2()
        temp = reader.read_temp()
        mySqlite.insertData(temp, no2, o3, co, so2, pm)
        mySqlite.commitDB()
        strSensorData = mySqlite.MakeCSVFormatStr(True)
        if bConnectApp == True:
            mySqlite.commitDB()
            try:
                gSocket.send(str(gBoardID) + ',' + strSensorData.rstrip(','))
            except:
                bConnectApp = False
        print ('\nConnect Status : ' + str(bConnectApp))
        print ('BoardID : ' +str(gBoardID))
        splitStr = strSensorData.split(',')
        print ('temp : ' + splitStr[0] +'F')
        print ('no2 : ' + splitStr[1] +'ppm')
        print ('o3 : ' + splitStr[2] +'ppb')
        print ('co : ' + splitStr[3] +'ppm')
        print ('so2 : ' + splitStr[4] +'ppb')
        print ('pm2.5 : ' + splitStr[5] +'u/m^3')
        print ('no2_AQI : ' + splitStr[6])
        print ('o3_AQI : ' + splitStr[7])
        print ('co_AQI : ' + splitStr[8])
        print ('so2_AQI : ' + splitStr[9])
        print ('pm2.5_AQI : ' + splitStr[10])

        time.sleep(1)
    mySqlite.closeDB()

t1 = threading.Thread(target=getAir)
t1.daemon = True
t1.start()

class BTClientHandler(asyncore.dispatcher_with_send):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.server = server
        self.data = ""

    def handle_read(self):
        try:
            data = self.recv(1024).decode('ascii')
            if not data:
                return

            lf_char_index = data.find('\n')

            if lf_char_index == -1:
                # No new line character in data, so we append all.
                self.data += data
            else:
                # We see a new line character in data, so append rest and handle.
                self.data += data[:lf_char_index]
                print("received [{}]".format(self.data))

                self.send((self.data + '\n').encode('ascii'))


                # Clear the buffer
                self.data = ""
        except Exception as e:
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.data = ""
            self.handle_close()

    def handle_close(self):
        # flush the buffer
        while self.writable():
            self.handle_write()

        self.server.active_client_handlers.remove(self)
        self.close()