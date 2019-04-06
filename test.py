
import grovepi
import time
import collections
from dataprocessfunctions import *

historyBuffer = collections.deque(maxlen = 15)
cur_buffer = collections.deque(maxlen = 5)
outputBuffer = collections.deque(maxlen = 8)

lastValue = 0
highPassed = 0
historyBuffer.append(highPassed)
cur_buffer.append(highPassed)
count = 0  

distanceFilter1 = LowPassFilter(0.1, 500, 80)
distanceFilter2 = LowPassFilter(0.3, 500, 80)
distanceFilter3 = LowPassFilter(0.5, 500, 80)
distanceFilter4 = LowPassFilter(0.7, 500, 80)

state1 = state2 = state3 = state4 = 0

# print("Time, Value, High Passed, Median, Diff, Output, Pir, Ultro, Count")
print("D1"+","+ "D2"+","+ "D3"+","+ "D4")
while True:
    pir = grovepi.digitalRead(3)
    ultra = grovepi.ultrasonicRead(2)
    value = grovepi.analogRead(1)

    # highPassed = 0.5*(highPassed + value - lastValue)

    # cur_buffer.append(highPassed)
    # ordered_cur = sorted(cur_buffer)
    # cur_highPass = ordered_cur[int(len(ordered_cur)/2)] 

    # orderedHistory = sorted(historyBuffer)
    # median_of_history = orderedHistory[int(len(orderedHistory)/2)] 
    # lastValue = value
    # historyBuffer.append(highPassed)  

    distanceFilter1.addData(ultra)
    distanceFilter2.addData(ultra)
    distanceFilter3.addData(ultra)
    distanceFilter4.addData(ultra)

    if distanceFilter1.state == "NORMAL":
        state1 = 0
    else: 
        state1 = 1

    if distanceFilter2.state == "NORMAL":
        state2 = 0
    else: 
        state2 = 1

    if distanceFilter3.state == "NORMAL":
        state3 = 0
    else: 
        state3 = 1

    if distanceFilter4.state == "NORMAL":
        state4 = 0
    else: 
        state4 = 1
    # print(str(distanceFilter1.lowPassed)+", "+str(distanceFilter2.lowPassed)+", "+str(distanceFilter3.lowPassed)+", "+str(distanceFilter4.lowPassed))
    print(str(state1)+", "+str(state2)+", "+str(state3)+", "+str(state4))
    time.sleep(0.01)
    #print(median_of_history)
    '''
    if abs(cur_highPass-median_of_history) > 25:
        outputBuffer.append(1)
        if sum(outputBuffer) >= 5:
            print("warning! " + str(cur_highPass-median_of_history)+" PIR: "+str(pir)+" Ultra: "+str(ultra))
            count += 1
    else:
        outputBuffer.append(0)

    print("%s, %4.4f, %4.4f, %4.4f, %4.4f, %d, %d, %d"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),value,cur_highPass,median_of_history,cur_highPass-median_of_history, pir, ultra, count))    
    
    '''
    
    
