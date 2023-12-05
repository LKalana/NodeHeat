"""
PROGRAM : PYTHON CLIENT FOR ESP8266 DRONE SERVER WITH HEATMAP (SINGLE HEATMAP)
AUTHOR  : LIYANAGE KALANA PERERA
DATE    : 2023.12.4 --> 14:46 PM


NOTE_ :- THIS PYTHON SCRIPT ACT AS THE CLIENT SIDE FOR THE ESP8266 THERMAL TELEMETRY SYSTEM.
         SIMPLY RUN THE SCRIPT AND REMEMBER TO CHANGE THE IP ADDRESS ON LINE 19.
         ALSO THIS PROGRAM WILL CREATE A HEATMAP ACCORDING TO THE SERVER DATA.

         THIS SCRIPT WILL READ DATA FROM SERVER SIDE AND THEN STORE IT IN A FILE. BECAUSE THE
         REQUEST IS IN TEXT FORMAT. THEREFORE STORE THE DATA IN TXT FILE AND THEN CONVERT THEM 
         INTO FLOAT AND STORE THEM IN AN ARRAY. THEN PLOT IN HEATMAP.
"""

import numpy as np
import matplotlib.pyplot as plt
import requests # INSTALL THIS MODULE USING PIP INSTALL REQUESTS.
import time

#-------------------------------------------------------------------- INITIALIZING PART.
theRequest = None
line = 0
RAWDATA_ = [] # RAW DATA FROM SERVER SIDE.
HEATDATA_ = [] # FILTERED DATA LIST.
PLOTDATA_ = [] # DATA TO BE PROCESS FOR PRINT.
TEMP = " "
#-------------------------------------------------------------------- OPEN THE TXT FILE PART.
f = open("HeatmapData.txt", "w")
#-------------------------------------------------------------------- CALIBRATION DELAY PART.
print("STARTING ESP8266 THERMAL TELEMETRY SYSTEM")
time.sleep(2)
print("THERMAL SCAN ON PROGRES...")
print(" ")
for count in range(5):
  a = '*'
  print(a)
  time.sleep(2)
print(" ")
print("THERMAL SCAN IN PROGRES...")
print(" ")
#-------------------------------------------------------------------- RECIEVING DATA PART.
# AMOUNT OF DATA TO BE RECIEVED.
for count in range(1):
  # YOU CAN GET THE ESP8266 IP ADDRESS AFTER UPLOADING THE ESP8266 SERVER SCKETCH TO THE 
  # BOARD AND RUN SERIAL MONITOR.
  theRequest = requests.get('http://ESP8266_IP_ADDRESS/ClientSayingHello')
  # WRITING DATA TO THE FILE.
  f.write(theRequest.text)
  # print(theRequest.text)# DEBUG.
  # HEATMAP PLOTTING AND DISPLAY PART.
  time.sleep(2)
#-------------------------------------------------------------------- CLOSE THE FILE.
f.close()
#-------------------------------------------------------------------- READ FROM THE TXT FILE PART.
f = open("HeatmapData.txt","r")
# READING FIRST 64 LINES. (130)
for line in range(130):
  # REMOVE NEW LINES.
  RAWDATA_.insert(line,f.readline())
#-------------------------------------------------------------------- CLOSE THE FILE.
f.close()
#---------------------------------------------------------------------- DEBUG.
print(len(RAWDATA_))
print("RawData i")
print(RAWDATA_)
print(" ")
#---------------------------------------------------------------------- DEBUG.
# LAST TWO LIST ELEMENTS ARE NULL, REFER THE TXT FILE.
# NOW IN HERE THERE A BIT CATCH. INITIAL LIST SIZE IS 130 BUT AFTER POP FUNCTION
# IT REDUCED TO 64 BECAUSE AFTER EACH VALUE IT HAVE A "NEW LINE" CHARACTER.
# AFTER REMOVE ALL THOSE "NEW LINES" THERE ARE ONLY 64 ELEMENTS IN LIST. HENCE 64.
for line in range(0,66):
  # REMOVE NEW LINES.
  if RAWDATA_[line] == "\n": 
   RAWDATA_.pop(line)
#---------------------------------------------------------------------- DEBUG.
print(" ")
print("RawData ii")
print(RAWDATA_)
print(len(RAWDATA_))
#---------------------------------------------------------------------- DEBUG.
# REMOVING THAT UNWANTED ELEMENTS FROM THE LIST.
while(' ' in RAWDATA_):
    RAWDATA_.remove(' ')

# CREATE SIZE FOR HEATDATA_
for line in range(0,64):
  HEATDATA_.insert(line,0)
#---------------------------------------------------------------------- DEBUG.
print(len(HEATDATA_))
print(" ")
# EXTRACTIBG FOR HEATDARA_
for line in range(0,64):
  TEMP = RAWDATA_[line]
  TEMP = float(TEMP)
  HEATDATA_[line] = TEMP
#---------------------------------------------------------------------- DEBUG.
print(" ")
print("HeatData")
print(len(HEATDATA_))
print(HEATDATA_)
# CREATING THE NUMPY ARRAY AND PLOTTING THE HEATMAP.
PLOTDATA_ = [
              [HEATDATA_[0],HEATDATA_[1],HEATDATA_[2],HEATDATA_[3],HEATDATA_[4],HEATDATA_[5],HEATDATA_[6],HEATDATA_[7]],
              [HEATDATA_[8],HEATDATA_[9],HEATDATA_[10],HEATDATA_[11],HEATDATA_[12],HEATDATA_[13],HEATDATA_[14],HEATDATA_[15]],
              [HEATDATA_[16],HEATDATA_[17],HEATDATA_[18],HEATDATA_[19],HEATDATA_[20],HEATDATA_[21],HEATDATA_[22],HEATDATA_[23]],
              [HEATDATA_[24],HEATDATA_[25],HEATDATA_[26],HEATDATA_[27],HEATDATA_[28],HEATDATA_[29],HEATDATA_[30],HEATDATA_[31]],
              [HEATDATA_[32],HEATDATA_[33],HEATDATA_[34],HEATDATA_[35],HEATDATA_[36],HEATDATA_[37],HEATDATA_[38],HEATDATA_[39]],
              [HEATDATA_[40],HEATDATA_[41],HEATDATA_[42],HEATDATA_[43],HEATDATA_[44],HEATDATA_[45],HEATDATA_[46],HEATDATA_[47]],
              [HEATDATA_[48],HEATDATA_[49],HEATDATA_[50],HEATDATA_[51],HEATDATA_[52],HEATDATA_[53],HEATDATA_[54],HEATDATA_[55]],
              [HEATDATA_[56],HEATDATA_[57],HEATDATA_[58],HEATDATA_[59],HEATDATA_[60],HEATDATA_[61],HEATDATA_[62],HEATDATA_[63]]
            ]
#---------------------------------------------------------------------- DEBUG.
print(" ")
print("PlotData")
print(PLOTDATA_)
print(type(PLOTDATA_))

heatmap_ = np.array(PLOTDATA_)
print(type(heatmap_))
# PLOTTING THE DATA USING 'JET' COLOR SCHEME.
plt.imshow(heatmap_, cmap='jet')
plt.title("AMG8833 Heatmap Data")
plt.show()