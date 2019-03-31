
import grovepi
import time
import collections

historyBuffer = collections.deque(maxlen = 10)
outputBuffer = collections.deque(maxlen = 4)
warnBuffer = collections. deque(maxlen = 6)
lastValue = 0
highPassed = 0
historyBuffer.append(highPassed)
count = 0  
warn_flag = 0
print("Time", "Value", "High Passed", "Median", "Diff", "Output", "Pir", "Ultro")
while True:
    pir = grovepi.digitalRead(3)
    ultra = grovepi.ultrasonicRead(2)
    value = grovepi.analogRead(1)
    highPassed = 0.5*(highPassed + value - lastValue)
    
    orderedHistory = sorted(historyBuffer)
    median = orderedHistory[int(len(orderedHistory)/2)] 
    lastValue = value
    historyBuffer.append(highPassed)  
    time.sleep(0.01)
    #print(median)
    
    if abs(highPassed-median) > 30:
        outputBuffer.append(1)
        if sum(outputBuffer) >= 3:
            warn_flag = 1 
        else:   
            warn_flag = 0
        
	
    else:
        outputBuffer.append(0)
        warn_flag = 0	
    warnBuffer.append(warn_flag)
    print("%s, %4.4f, %4.4f, %4.4f, %4.4f, %d, %d, %d, %d"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),value,highPassed,median,highPassed-median, warn_flag, pir, ultra, count))    
    

    if sum(warnBuffer) >=4:
        print("warning! " + str(highPassed-median)+" PIR: "+str(pir)+" Ultra: "+str(ultra))
        count += 1
    
