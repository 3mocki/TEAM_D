import sqlite3
from aqi import *

class MySqlite:
    def __init__(self, name):
        self.dbName = name + '.db'
        self.airData = name + 'air'

    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def deleteTable(self):
        self.cursor.execute('Drop Table If Exists ' + self.airData)

    def createTable(self):
        self.cursor.execute('create table ' + self.airData +
                            ' (no INTEGER PRIMARY KEY, temp FLOAT, no2 FLOAT, o3 FLOAT, co FLOAT, so2 FLOAT, pm FLOAT, no2Aqi INT, o3Aqi INT, coAqi INT, so2Aqi INT, pmAqi INT)')

    def insertData(self, temp, no2, o3, co, so2, pm, isDisConnect):
        self.cursor.execute('insert into ' + self.airData +
                            '(temp, no2, o3, co, so2, pm, no2Aqi, o3Aqi, coAqi, so2Aqi, pmAqi,) values (?,?,?,?,?,?,?,?,?,?,?);',
                            (temp, no2, o3, co, so2, pm, 0, 0, 0, 0, 0))
        if self.GetAllDataCount() > 120:
            self.cursor.execute(
                'delete from ' + self.airData + ' where no in (select no from ' + self.airData + ' limit 1)')
        airAve = self.GetAvgData()
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

    def GetAllDataCount(self):
        self.cursor.execute('SELECT count(*) FROM ' + self.airData)
        for row in self.cursor:
            return int(row[0])

    def GetAvgData(self):
        self.cursor.execute('SELECT avg(pm), avg(co), avg(o3), avg(no2), avg(so2) FROM ' + self.airData)
        for row in self.cursor:
            return row

    def commitDB(self):
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