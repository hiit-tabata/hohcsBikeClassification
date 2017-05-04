import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,MinuteLocator
from datetime import datetime


yearsFmt = DateFormatter('%M:%S')
time_format = '%Y-%m-%dT%H:%M:%S.%fZ'

def poltCsv(recordJson, sensorData):
    # reformat the time
    time = [datetime.strptime(i, time_format) for i in sensorData[:,0]]    
    
    # plot the axis
    fig, arrX = plt.subplots(5, sharex=True,figsize=(20, 10), dpi=120)
    for i in range(5):        
        arrX[i].set_title('sensor ' +str(i))
        arrX[i].plot_date(time, sensorData[:,i+1], '-', linewidth=2, xdate=True)
        arrX[i].xaxis.set_major_locator(MinuteLocator())    
        arrX[i].xaxis.set_major_formatter(yearsFmt)
        arrX[i].set_ylabel('sensor value')
        arrX[i].set_xlim(time[0],time[-1])
        if i == 4:
            arrX[i].set_ylim(0,1)
            arrX[i].set_xlabel('time')
        else:
            arrX[i].set_ylim(0,2000)
        arrX[i].autoscale_view()
    fig.suptitle("User "+ recordJson["clientId"]+ " Record "+str(recordJson["id"]))
    fig.text(0.95, 0.01, 'Duration '+str(recordJson["duration"] )+" ms",
        verticalalignment='bottom', horizontalalignment='right',fontsize=12)
    fig.show()