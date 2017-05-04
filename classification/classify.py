# This is the main script to start the program

from preprocessing import readRecord, readLabelCsv
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,MinuteLocator
from datetime import datetime
from helper import poltCsv


labelsCsv = readLabelCsv()

recordIds = labelsCsv["recordid"]


for id in recordIds:   
    
    json, sensorData = readRecord(str(id.decode('UTF-8')))
    
    poltCsv(json, sensorData)
    
