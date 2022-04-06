""" Envio de la Lectura de sensores ACTIVE BRO"""

from GetPulse import GetPulse
from mpu6050 import mpu6050
from MCP3008 import MCP3008
import time
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


import paho.mqtt.client as mqtt  #Libreria para comunicacion con ThingSpeake en mqtt


#Ajuste para comunicación con thingspeak
client = mqtt.Client()
client.connect("mqtt.thingspeak.com",1883,60)
channelId= "1695716"
apiKey= "NDI778WC4ZALEU6Y"
    


fig, ax = plt.subplots()
line, = ax.plot(0)
ax.set_ylim(300, 800)
ax.set_xlim(0, 100)
xdata, ydata = [0]*100, [0]*100
channel = 0
mpu = mpu6050(0x68)
p = GetPulse()
p.startAsyncBPM()
x = 9
datapuls = p.Signal
data_gen= [0,0]
data_gen[0]=x


def update(data):
    line.set_ydata(data)
    return line

def run(data):
    global xdata, ydata
    x,y = data
    if (x == 0):
        xdata = [0]*100
        ydata = [0]*100
    del xdata[0]
    del ydata[0]
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)
    return line,

while True:
    
    if (x >= 100):
        x = 0
    else:
        x += 1
    data_gen[1]=datapuls 
    bpm = p.BPM
    acel_data = mpu.get_accel_data()
    print("Acc X : "+str(round(acel_data['x'],3)))
    print("Acc Y : "+str(round(acel_data['y'],3)))
    print("Acc Z : "+str(round(acel_data['z'],3)))
    print()

    gyro_data = mpu.get_gyro_data()
    print("Gyro X : "+str(round(gyro_data['x'],3)))
    print("Gyro Y : "+str(round(gyro_data['y'],3)))
    print("Gyro Z : "+str(round(gyro_data['z'],3)))
    print()
    print("-------------------------------")
    
    
    if bpm > 0:
        
        print("BPM: %d" % bpm)
    else:
        print("No Heartbeat detected")
        
    client.publish("channels/%s/publish/%s"%(channelId,apiKey),"field1="+str(bpm)+"&field2="+str(acel_data['x'])+"&field3="+str(acel_data['y'])+"&field4="+str(acel_data['z']))
    #resultad= firebase.post ('/1505/registro',datosUsu) 
    #resultado= firebase.post ('/1505/progres',InfoUsu)   
    #envio = requests.get("https://api.thingspeak.com/update?api_key=NDI778WC4ZALEU6Y&field1="+str(bpm)+"&field2="+str(acel_data['x'])+"&field3="+str(acel_data['y'])+"&field4="+str(acel_data['z']))#fokeorijfñefeñn...
    
    time.sleep(1)

ani = animation.FuncAnimation(fig, run, data_gen, interval=0, blit=True)

plt.show()