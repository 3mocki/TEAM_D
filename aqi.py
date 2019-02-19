def CalO3Aqi(o3average):
   if o3average >= 125 and o3average <= 164 :
      o3aqi = (((o3average-125)*(150-101))/(164-125))+101
      return o3aqi
   elif o3average >= 165 and o3average <= 204 :
      o3aqi = (((o3average-165)*(200-151))/(204-165))+151
      return o3aqi
   elif o3average >= 205 and o3average <= 404 :
      o3aqi = (((o3average-205)*(300-201))/(404-205))+201
      return o3aqi
   elif o3average >= 405 and o3average <= 504 :
      o3aqi = (((o3average-405)*(300-201))/(504-405))+301
      return o3aqi
   elif o3average >= 505 and o3average <= 604 :
      o3aqi = (((o3average-505)*(300-201))/(604-505))+401
      return o3aqi
   else :
      return 150

def CalPm25Aqi(pm25average):
   if pm25average >= 0 and pm25average <= 12 :
      pm25aqi = (((pm25average-0)*(50-0))/(12-0))+0
      return pm25aqi
   elif pm25average >= 12.1 and pm25average <= 35.4 :
      pm25aqi = (((pm25average-12.1)*(100-51))/(35.4-12.1))+51
      return pm25aqi
   elif pm25average >= 35.5 and pm25average <= 55.4 :
      pm25aqi = (((pm25average-35.5)*(150-101))/(55.4-35.5))+101
      return pm25aqi
   elif pm25average >= 55.5 and pm25average <= 150.4 :
      pm25aqi = (((pm25average-55.5)*(200-151))/(150.4-55.5))+151
      return pm25aqi
   elif pm25average >= 150.5 and pm25average <= 250.4 :
      pm25aqi = (((pm25average-150.5)*(300-201))/(250.4-150.5))+201
      return pm25aqi
   elif pm25average >= 250.5 and pm25average <= 350.4 :
      pm25aqi = (((pm25average-250.5)*(400-301))/(350.4-250.5))+301
      return pm25aqi
   elif pm25average >= 350.5 and pm25average <= 500.4 :
      pm25aqi = (((pm25average-350.5)*(500-401))/(500.4-350.5))+401
      return pm25aqi
   else :
      return 501

def CalCoAqi(coaverage):
   if coaverage >= 0 and coaverage <= 4.4 :
      coaqi = (((coaverage-0)*(50-0))/(4.4-0))+0
      return coaqi
   elif coaverage >= 4.5 and coaverage <= 9.4 :
      coaqi = (((coaverage-4.5)*(100-51))/(9.4-4.5))+51
      return coaqi
   elif coaverage >= 9.5 and coaverage <= 12.4 :
      coaqi = (((coaverage-9.5)*(150-101))/(12.4-9.5))+101
      return coaqi
   elif coaverage >= 12.5 and coaverage <= 15.4 :
      coaqi = (((coaverage-12.5)*(200-151))/(15.4-12.5))+151
      return coaqi
   elif coaverage >= 15.5 and coaverage <= 30.4 :
      coaqi = (((coaverage-15.5)*(300-201))/(30.4-15.5))+201
      return coaqi
   elif coaverage >= 30.5 and coaverage <= 40.4 :
      coaqi = (((coaverage-30.5)*(400-301))/(40.4-30.5))+301
      return coaqi
   elif coaverage >= 40.5 and coaverage <= 50.4 :
      coaqi = (((coaverage-40.5)*(500-401))/(50.4-40.5))+401
      return coaqi
   else :
      return 501

def CalSo2Aqi(so2average):
   if so2average >= 0 and so2average <= 35 :
      so2aqi = (((so2average-0)*(50-0))/(35-0))+0
      return so2aqi
   elif so2average >= 36 and so2average <= 75 :
      so2aqi = (((so2average-36)*(100-51))/(75-36))+51
      return so2aqi
   elif so2average >= 76 and so2average <= 185 :
      so2aqi = (((so2average-76)*(150-101))/(185-76))+101
      return so2aqi
   elif so2average >= 186 and so2average <= 304 :
      so2aqi = (((so2average-186)*(200-151))/(304-186))+151
      return so2aqi
   elif so2average >= 305 and so2average <= 604 :
      so2aqi = (((so2average-305)*(300-201))/(604-305))+201
      return so2aqi
   elif so2average >= 605 and so2average <= 804 :
      so2aqi = (((so2average-605)*(400-301))/(804-605))+301
      return so2aqi
   elif so2average >= 805 and so2average <= 1004 :
      so2aqi = (((so2average-805)*(500-401))/(1004-805))+401
      return so2aqi
   else :
      return 501

def CalNo2Aqi(no2average):
   if no2average >= 0 and no2average <= 53 :
      no2aqi = (((no2average-0)*(50-0))/(53-0))+0
      return no2aqi
   elif no2average >= 54 and no2average <= 100 :
      no2aqi = (((no2average-54)*(100-51))/(100-54))+51
      return no2aqi
   elif no2average >= 101 and no2average <= 360 :
      no2aqi = (((no2average-101)*(150-101))/(360-101))+101
      return no2aqi
   elif no2average >= 361 and no2average <= 649 :
      no2aqi = (((no2average-361)*(200-151))/(649-361))+151
      return no2aqi
   elif no2average >= 650 and no2average <= 1249 :
      no2aqi = (((no2average-650)*(300-201))/(1249-650))+201
      return no2aqi
   elif no2average >= 1250 and no2average <= 1649 :
      no2aqi = (((no2average-1250)*(400-301))/(1649-1250))+301
      return no2aqi
   elif no2average >= 1650 and no2average <= 2049 :
      no2aqi = (((no2average-1650)*(500-401))/(2049-1650))+401
      return no2aqi
   else :
      return 501