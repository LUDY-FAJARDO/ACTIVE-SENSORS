import time
import threading
from MCP3008 import MCP3008

class GetPulse:# definicion de la clase sensor
    def __init__(self, channel = 0, bus = 0, device = 0): #definicon parametros entrada adc
        self.channel = channel
        self.BPM = 0
        self.Signal =0
        self.adc = MCP3008(bus, device)
        
    # Iniciar GetBPM loop
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.GetBPM)
        self.thread.stopped = False
        self.thread.start()
        return
        
    # Detener rutina
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return
    
    def GetBPM(self):
        #------- Inicalizacion de variables-----------------
        pulses = [0] * 10         # Almacenar ultimos 10 valores
        sampleCounter = 0         # tiempo por pulso
        lastBeatTime = 0          # tiempo ultimo pulso
        Midpoint = 512            # punto medio de pulso
        High = 512         # pico superior e inferior / inicializacion
        Low = 512
        thresh = 520            # detección de pulso
        amp = 100                 # used to hold amplitude of pulse waveform, seeded
        firstBeat = True          # para generar el array con un dato valido
        otherBeat = False         # 
        Period = 400              # intervalo de tiempo entre latidos
        Pulse = False             # "True" cuando se detecta ritmo constante, de lo contrario "False". 
        lastTime = int(time.time()*1000)
        
        while not self.thread.stopped: # mientras thread.stopped= "False"
        
            self.Signal = self.adc.read(self.channel)# se llama la funcion read de la libreria
            currentTime = int(time.time()*1000) # obtener current time miliseconds
            
            sampleCounter += currentTime - lastTime # aumenta el conteo while
            lastTime = currentTime
            
            N = sampleCounter - lastBeatTime # 

            #---- Encontrar los picos de la onda -----
            if self.Signal < thresh and N > (Period/5.0)*3:     # evitar ruido, esperando 3/5 desde el ultimo latido
                if self.Signal < Midpoint:                      
                    Low = self.Signal                          # define el minimo valor de la onda

            if self.Signal > thresh:  # define el minimo valor de la onda
                High = self.Signal

            # signal surges up in value every time there is a pulse
            if N > 250:                                 # evitar ruido
                if self.Signal > thresh and Pulse == False and N > (Period/5.0)*3:       
                    Pulse = True                        # considerando primer pulso
                    Period = sampleCounter - lastBeatTime  # se ajusta el periodo de los pulsos
                    lastBeatTime = sampleCounter        # se define tiempo del ultimo pulso

                    if otherBeat:                      # si es el segundo pulso encontrado
                        otherBeat = False;             
                        for i in range(len(pulses)):    # se llena el vector con ese periodo de pulsos
                          pulses[i] = Period

                    if firstBeat:                       # si es el primer pulso encontrado se habilita segundo pulso.
                        firstBeat = False;             
                        otherBeat = True;              
                        continue

                    # keep a running total of the last 10 IBI values  
                    pulses[:-1] = pulses[1:]              # desplazamiendo del vector
                    pulses[-1] = Period
                    PeriodTotal = sum(pulses)            # suma de la duracion de todos los pulsos

                    PeriodTotal /= len(pulses)           # se halla el promedio 
                    self.BPM = 60000/PeriodTotal         # se encuentran los pulsos por minuto (60*100ms) 

            if self.Signal < thresh and Pulse == True:       # cuando se encuentre pico negativo
                Pulse = False                           # reset pulse
                amp = High - Low                            # get amplitude of the pulse wave
                thresh = amp/2 + Low                      # se ajusta el valor del 50% de la amplitud
                High = thresh                              # reset these for next time
                Low = thresh

            if N > 2500:                                # si pasan 2.5 sin detectar beat
                thresh = 512                   # se ajustan por defecto
                High = 512
                Low = 512
                lastBeatTime = sampleCounter            # se ajusta valor de ultimo beat        
                firstBeat = True                        # para detectar un nuevo beat
                otherBeat = False                      
                self.BPM = 0                           # se retorna 0;

            time.sleep(0.005)
            
        
