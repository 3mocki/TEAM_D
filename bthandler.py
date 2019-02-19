import asyncore, logging, time, sensor
from bterror import BTError
import threading
from MySqlite import *

logger = logging.getLogger(__name__)

reader=sensor.Reader()
lock = threading.Lock()
global bConnectApp
global gSocket
global gCurTime
global gBoardID
gBoardID = 0
bConnectApp = False;

def realTimedAirData():
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
        mySqlite.InsertAirData(pm, co, o3, no2, so2, temp, not bConnectApp)
        mySqlite.commitDB()
        strSensorData = mySqlite.MakeCSVFormatStr(True)
        if bConnectApp == True:
            mySqlite.commitDB()
            try:
                gSocket.send(str(gBoardID) + ',' + strSensorData.rstrip(','))
            except:
                bConnectApp = False
        print ('\nIsAppConnect : ' + str(bConnectApp))
        print ('BoardID : ' +str(gBoardID))
        splitStr = strSensorData.split(',')
        print ('pm : ' + splitStr[0] +'u/m^3')
        print ('co : ' + splitStr[1] +'ppm')
        print ('o3 : ' + splitStr[2] +'ppb')
        print ('no2 : ' + splitStr[3] +'ppb')
        print ('so2 : ' + splitStr[4] +'ppb')
        print ('temp : ' + splitStr[5] +'F')
        print ('pmaqi : ' + splitStr[6])
        print ('coaqi : ' + splitStr[7])
        print ('o3aqi : ' + splitStr[8])
        print ('no2aqi : ' + splitStr[9])
        print ('so2aiq : ' + splitStr[10])

        time.sleep(1)
    mySqlite.closeDB()

t1 = threading.Thread(target=realTimedAirData)
t1.daemon = True
t1.start()

class BTClientHandler(asyncore.dispatcher_with_send):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.server = server
        self.data = ""
        global gSocket
        gSocket = self

    def handle_read(self):
        try:
            data = self.recv(1024)
            if not data:
                return

            print (data)
            curTime = data.split(',')[1]
            curTime = datetime.datetime.strptime(curTime.strip('\n'), "%Y-%m-%d %H:%M:%S")
            global gCurTime
            gCurTime = curTime
            global gBoardID
            gBoardID = int(data.split(',')[2])
            lf_char_index = data.find('\n')

            if lf_char_index == -1:
                # No new line character in data, so we append all.
                self.data += data
            else:
                self.data += data[:lf_char_index]
                #a = []
                if self.data.split(',')[0] == "sensor":
                    with lock:
                        global bConnectApp
                        bConnectApp = True
                        global bSensHisOnce
                        bSensHisOnce = True

                # Clear the buffer
                self.data = ""

        except Exception as e:
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.data = ""
            lf_char_index = -1
            with lock:
                global testValue
                testValue = False
            self.handle_close()

    def handle_close(self):
        # flush the buffer
        while self.writable():
            self.handle_write()
        global bConnectApp
        bConnectApp = False
        self.server.active_client_handlers.remove(self)
        self.close()