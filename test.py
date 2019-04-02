
import grovepi
import time
import collections

historyBuffer = collections.deque(maxlen = 15)
cur_buffer = collections.deque(maxlen = 5)
outputBuffer = collections.deque(maxlen = 8)

lastValue = 0
highPassed = 0
historyBuffer.append(highPassed)
cur_buffer.append(highPassed)
count = 0  

print("Time, Value, High Passed, Median, Diff, Output, Pir, Ultro, Count")
while True:
    pir = grovepi.digitalRead(3)
    ultra = grovepi.ultrasonicRead(2)
    value = grovepi.analogRead(1)

    highPassed = 0.5*(highPassed + value - lastValue)

    cur_buffer.append(highPassed)
    ordered_cur = sorted(cur_buffer)
    cur_highPass = ordered_cur[int(len(ordered_cur)/2)] 

    orderedHistory = sorted(historyBuffer)
    median_of_history = orderedHistory[int(len(orderedHistory)/2)] 
    lastValue = value
    historyBuffer.append(highPassed)  
    time.sleep(0.01)
    #print(median_of_history)
    
    if abs(cur_highPass-median_of_history) > 25:
        outputBuffer.append(1)
        if sum(outputBuffer) >= 5:
            print("warning! " + str(cur_highPass-median_of_history)+" PIR: "+str(pir)+" Ultra: "+str(ultra))
            count += 1
    else:
        outputBuffer.append(0)

    print("%s, %4.4f, %4.4f, %4.4f, %4.4f, %d, %d, %d"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),value,cur_highPass,median_of_history,cur_highPass-median_of_history, pir, ultra, count))    
    

    
    
