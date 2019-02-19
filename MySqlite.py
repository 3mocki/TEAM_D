import sqlite3
from datetime import timedelta
import datetime
from aqi import *


class MySqlite:
    def __init__(self, name):
        self.dbNameWithFileType = name + '.db'
        self.allAirDataTableName = name + 'All'
        self.hisAirDataTableName = name + 'His'

    def ConnectToDB(self):
        self.db = sqlite3.connect(self.dbNameWithFileType)
        self.cursor = self.db.cursor()

    def DeleteTable(self):
        self.cursor.execute('Drop Table If Exists ' + self.allAirDataTableName)
        self.cursor.execute('Drop Table If Exists ' + self.hisAirDataTableName)

    def DeleteAllDataAtTable(self, idx):
        if idx == 'allair':
            self.cursor.execute('delete from ' + self.allAirDataTableName)
        if idx == 'hisair':
            self.cursor.execute('delete from ' + self.hisAirDataTableName)

    def CreateTable(self):
        self.cursor.execute('create table ' + self.allAirDataTableName +
                            ' (no INTEGER PRIMARY KEY, pm FLOAT, co FLOAT, o3 FLOAT, no2 FLOAT, so2 FLOAT, temp FLOAT, pmAqi INT, coAqi INT, o3Aqi INT, no2Aqi INT, so2Aqi INT)')
        self.cursor.execute('create table ' + self.hisAirDataTableName +
                            ' (no INTEGER PRIMARY KEY, pm FLOAT, co FLOAT, o3 FLOAT, no2 FLOAT, so2 FLOAT, temp FLOAT, pmAqi INT, coAqi INT, o3Aqi INT, no2Aqi INT, so2Aqi INT, time DATETIME)')

    def InsertAirData(self, pm, co, o3, no2, so2, temp, isDisConnect):
        self.cursor.execute('insert into ' + self.allAirDataTableName +
                            '(pm, co, o3, no2, so2, temp, pmAqi, coAqi, o3Aqi, no2Aqi, so2Aqi) values (?,?,?,?,?,?,?,?,?,?,?);',
                            (pm, co, o3, no2, so2, temp, 0, 0, 0, 0, 0))
        if self.GetAllDataCount() > 120:
            self.cursor.execute(
                'delete from ' + self.allAirDataTableName + ' where no in (select no from ' + self.allAirDataTableName + ' limit 1)')
        airAve = self.GetAveData()
        calResPm = 0
        calResCo = 0
        calResO3 = 0
        calResNo2 = 0
        calResSo2 = 0
        for x in xrange(0, 5):
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
        self.cursor.execute('update ' + self.allAirDataTableName +
                            ' set pmAqi = ' + str(calResPm) + ',coAqi = ' + str(calResCo) + ',o3Aqi = ' + str(
            calResO3) + ',no2Aqi = ' + str(calResNo2) +
                            ',so2Aqi = ' + str(
            calResSo2) + ' where no = (SELECT MAX(no)  FROM ' + self.allAirDataTableName + ');')
        if isDisConnect == True:
            self.cursor.execute('insert into ' + self.hisAirDataTableName +
                                '(pm, co, o3, no2, so2, temp, pmAqi, coAqi, o3Aqi, no2Aqi, so2Aqi, time) values (?,?,?,?,?,?,?,?,?,?,?,?);',
                                (pm, co, o3, no2, so2, temp, calResPm, calResCo, calResO3, calResNo2, calResSo2,
                                 '0000-00-00 00:00:00'))

    def PrintTableData(self):
        self.cursor.execute('select * from ' + self.allAirDataTableName)
        print
        '\nallair'
        for row in self.cursor:
            print
            row
        self.cursor.execute('select * from ' + self.hisAirDataTableName)
        print
        '\nhisair'
        for row in self.cursor:
            print
            row

    def GetAllDataCount(self):
        self.cursor.execute('SELECT count(*) FROM ' + self.allAirDataTableName)
        for row in self.cursor:
            return int(row[0])

    def GetAveData(self):
        self.cursor.execute('SELECT avg(pm), avg(co), avg(o3), avg(no2), avg(so2) FROM ' + self.allAirDataTableName)
        for row in self.cursor:
            return row

    def SetTimeToHisData(self, dateTime):
        rowCount = 0
        intForRepeat = 0
        self.cursor.execute('SELECT count(*) FROM ' + self.hisAirDataTableName)
        for row in self.cursor:
            rowCount = int(row[0])
        intForRepeat = rowCount + 1
        for x in xrange(1, intForRepeat):
            tempTime = dateTime + timedelta(seconds=-rowCount)
            rowCount -= 1
            self.cursor.execute('update ' + self.hisAirDataTableName +
                                ' set time = \'' + str(tempTime) + '\' where no = ' + str(x) + ';')

    def CommitDB(self):
        self.db.commit()

    def CloseDB(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()

    def MakeCSVFormatStr(self, alldata):
        if alldata == True:
            airDataCSV = ''
            self.cursor.execute(
                'select * from ' + self.allAirDataTableName + ' where no = (SELECT MAX(no)  FROM ' + self.allAirDataTableName + ');')
            for row in self.cursor:
                for x in xrange(1, 12):
                    airDataCSV += str(row[x]) + ','
            return airDataCSV
        else:
            self.cursor.execute('select * from ' + self.hisAirDataTableName)
            a = 0
            airDataCSV = ''
            hisAirDAtaArr = []
            for row in self.cursor:
                if a == 1:
                    hisAirDAtaArr.append(airDataCSV.rstrip(','))
                    airDataCSV = ''
                    a = 0
                for x in xrange(1, 13):
                    airDataCSV += str(row[x]) + ','
                a += 1
            if airDataCSV != '':
                hisAirDAtaArr.append(airDataCSV.rstrip(','))
            return hisAirDAtaArr
            # return airDataCSV.rstrip(',')