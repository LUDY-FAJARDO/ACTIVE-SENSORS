from GetPulse import GetPulse
import time
import requests

p = GetPulse()
p.startAsyncBPM()

try:
    while True:
        bpm = p.BPM
        if bpm > 0:
            print("BPM: %d" % bpm)
        else:
            print("No Heartbeat detected")
        
        envio = requests.get("https://api.thingspeak.com/update?api_key=NLCJHRS7IXQKW30Y&field1="+str(bpm))
        time.sleep(1)
except:
    p.stopAsyncBPM()

