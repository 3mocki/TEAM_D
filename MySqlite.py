import sqlite3
from datetime import timedelta
from aqi import *

class MySqlite:
    def __init__(self, name):
        self.dbName = name + '.db'
        self.airData = name + 'air'
        self.hisAir = name + 'his'

    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def DeleteTable(self):
        self.cursor.execute('Drop Table If Exists ' + self.airData)
        self.cursor.execute('Drop Table If Exists ' + self.hisAir)

    def DeleteAllDataAtTable(self, idx):
        if idx == 'sensorair':
            self.cursor.execute('delete from ' + self.airData)
        if idx == 'sensorhis':
            self.cursor.execute('delete from ' + self.hisAir)

    def CreateTable(self):
        self.cursor.execute('create table ' + self.airData +
                            ' (no INTEGER PRIMARY KEY, pm FLOAT, co FLOAT, o3 FLOAT, no2 FLOAT, so2 FLOAT, temp FLOAT, pmAqi INT, coAqi INT, o3Aqi INT, no2Aqi INT, so2Aqi INT)')
        self.cursor.execute('create table ' + self.hisAir +
                            ' (no INTEGER PRIMARY KEY, pm FLOAT, co FLOAT, o3 FLOAT, no2 FLOAT, so2 FLOAT, temp FLOAT, pmAqi INT, coAqi INT, o3Aqi INT, no2Aqi INT, so2Aqi INT, time DATETIME)')

    def InsertAirData(self, pm, co, o3, no2, so2, temp, isDisConnect):
        self.cursor.execute('insert into ' + self.airData +
                            '(pm, co, o3, no2, so2, temp, pmAqi, coAqi, o3Aqi, no2Aqi, so2Aqi) values (?,?,?,?,?,?,?,?,?,?,?);',
                            (pm, co, o3, no2, so2, temp, 0, 0, 0, 0, 0))
        if self.GetAllDataCount() > 120:
            self.cursor.execute(
                'delete from ' + self.airData + ' where no in (select no from ' + self.airData + ' limit 1)')
        airAve = self.GetAveData()
        calResPm = 0
        calResCo = 0
        calResO3 = 0
        calResNo2 = 0
        calResSo2 = 0
        for x in range(0, 5):
            if x == 0:
                calResPm = int(CalPm25Aqi(airAve[0]))
            elif x == 1:
                calResCo = int(CalCoAqi(airAve[1]))
            elif x == 2:
                calResO3 = int(CalO3Aqi(airAve[2]))
            elif x == 3:
                calResNo2 = int(CalNo2Aqi(airAve[3]))
            elif x == 4:
                calResSo2 = int(CalSo2Aqi(airAve[4]))
        self.cursor.execute('update ' + self.airData +
                            ' set pmAqi = ' + str(calResPm) + ',coAqi = ' + str(calResCo) + ',o3Aqi = ' + str(
            calResO3) + ',no2Aqi = ' + str(calResNo2) +
                            ',so2Aqi = ' + str(
            calResSo2) + ' where no = (SELECT MAX(no)  FROM ' + self.airData + ');')
        if isDisConnect == True:
            self.cursor.execute('insert into ' + self.hisAir +
                                '(pm, co, o3, no2, so2, temp, pmAqi, coAqi, o3Aqi, no2Aqi, so2Aqi, time) values (?,?,?,?,?,?,?,?,?,?,?,?);',
                                (pm, co, o3, no2, so2, temp, calResPm, calResCo, calResO3, calResNo2, calResSo2,
                                 '0000-00-00 00:00:00'))

    def PrintTableData(self):
        self.cursor.execute('select * from ' + self.airData)
        print('\nallair')
        for row in self.cursor:
            print(row)
        self.cursor.execute('select * from ' + self.hisAir)
        print('\nhisair')
        for row in self.cursor:
            print(row)

    def GetAllDataCount(self):
        self.cursor.execute('SELECT count(*) FROM ' + self.airData)
        for row in self.cursor:
            return int(row[0])

    def GetAveData(self):
        self.cursor.execute('SELECT avg(pm), avg(co), avg(o3), avg(no2), avg(so2) FROM ' + self.airData)
        for row in self.cursor:
            return row

    def SetTimeToHisData(self, dateTime):
        rowCount = 0
        intForRepeat = 0
        self.cursor.execute('SELECT count(*) FROM ' + self.hisAir)
        for row in self.cursor:
            rowCount = int(row[0])
        intForRepeat = rowCount + 1
        for x in range(1, intForRepeat):
            tempTime = dateTime + timedelta(seconds=-rowCount)
            rowCount -= 1
            self.cursor.execute('update ' + self.hisAir +
                                ' set time = \'' + str(tempTime) + '\' where no = ' + str(x) + ';')

    def CommitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()

    def MakeCSVFormatStr(self, alldata):
        if alldata == True:
            airDataCSV = ''
            self.cursor.execute(
                'select * from ' + self.airData + ' where no = (SELECT MAX(no)  FROM ' + self.airData + ');')
            for row in self.cursor:
                for x in range(1, 12):
                    airDataCSV += str(row[x]) + ','
            return airDataCSV
        else:
            self.cursor.execute('select * from ' + self.hisAir)
            a = 0
            airDataCSV = ''
            hisAirDAtaArr = []
            for row in self.cursor:
                if a == 1:
                    hisAirDAtaArr.append(airDataCSV.rstrip(','))
                    airDataCSV = ''
                    a = 0
                for x in range(1, 13):
                    airDataCSV += str(row[x]) + ','
                a += 1
            if airDataCSV != '':
                hisAirDAtaArr.append(airDataCSV.rstrip(','))
            return hisAirDAtaArr
            # return airDataCSV.rstrip(',')