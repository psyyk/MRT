# -*- coding: utf-8 -*-
# import grovepi
import time
import collections # for deque class

# the following code does the median filter itself
    
# create a deque for history
# a deque is a double ended list,
# put things in the end when it is full
# (when it contains maxlen values), and things 
# will be pushed off the other end     
# median filter
'''
historyBuffer=collections.deque(maxlen=10)
historyBuffer2=collections.deque(maxlen=5)
print("Time,Raw data,Median")

while True:
  dataPoint1 = grovepi.ultrasonicRead(2)
  dataPoint2 = grovepi.digitalRead(3)
  # dataPoint=grovepi.digitalRead(2)
  historyBuffer.append(dataPoint1)
  historyBuffer2.append(dataPoint2)
  orderedHistory=sorted(historyBuffer)
  orderedHistory2=sorted(historyBuffer2)
  median=orderedHistory[int(len(orderedHistory)/2)]
  median2=orderedHistory2[int(len(orderedHistory2)/2)]
  print("%4.4f,%4.4f,%4.4f,%4.4f,%4.4f"%(time.time(),dataPoint1,median,dataPoint2,median2))
  time.sleep(0.1)


# low pass filter
lowPassed=0
constant=0.1
print("Time,Raw data, Low pass")
while True:
    value=grovepi.analogRead(0)
    lowPassed=lowPassed*(1.0-constant) + value * constant
    print("%4.4f,%4.4f,%4.4f"%(time.time(),value,lowPassed))
    time.sleep(0.05);

'''

class MedianFilter():
  state = "NORMAL"

  def __init__(self, delay):
    self.delay = delay
    self.historyBuffer = collections.deque(maxlen=delay)

  def printDelay(self):

    print(self.delay)
    return

  def addData(self, dataPoint):

    self.historyBuffer.append(dataPoint)
    orderedHistory = sorted(self.historyBuffer)
    self.median = orderedHistory[int(len(orderedHistory)/2)]
    if self.median > 0:
      self.state = "WARNING"
    return self.median

  def reset(self):
    self.state = "NORMAL"
    self.median = 0
    for i in xrange(0, self.delay-1):
      self.historyBuffer[i] = 0
    return


class LowPassFilter():
  state = "normal"
  def __init__(self, constant, lowPassed, threshold):
    self.constant = constant
    self.lowPassed = lowPassed
    self.threshold = threshold
    
  def addData(self, value):
    self.lowPassed = self.lowPassed * (1.0 - self.constant) + value * self.constant
    if self.lowPassed < self.threshold:
      self.state = "WARNING"
    return self.lowPassed

  def reset(self):
    self.state = "NORMAL"
    self.lowPassed = self.threshold + 100
    return


class HighPassFilter(object):
  state = "NORMAL"
  lastValue = 0
  def __init__(self, constant, highPassed, threshold):
    self.constant = constant
    self.highPassed = highPassed
    self.threshold = threshold

  def addData(self, value):
    self.highPassed = self.constant * (self.highPassed + value - self.lastValue)
    self.lastValue = value

    if self.highPassed > self.threshold:
      self.state = "WARNING"

    return self.highPassed

  def reset(self):
    self.state = "NORMAL"
    self.lastValue = 0

    

class LoudnessFilter(object):
  state = "NORMAL"
  num = 0
  def __init__(self, constant, highPassed, threshold, delay, buffer_size1, buffer_size2):
    self.constant = constant
    self.highPassed = highPassed
    self.threshold = threshold
    self.delay = delay    
    self.medianFilter = MedianFilter(self.delay)
    self.highPassFilter = HighPassFilter(self.constant, self.highPassed, self.threshold)
    self.ob_size = buffer_size1
    self.wb_size = buffer_size2
    self.outputBuffer = collections.deque(maxlen = self.ob_size)
    self.warningBuffer = collections.deque(maxlen = self.wb_size)

  def addData(self, value):
    if self.num < 15:
      self.num += 1
    self.highPassed = self.highPassFilter.addData(value)
    self.medianOfHighPassed = self.medianFilter.addData(self.highPassed)
    self.diff = abs(self.highPassed - self.medianOfHighPassed)
    if self.diff > self.threshold:
      self.outputBuffer.append(1)
      if sum(self.outputBuffer) > (self.ob_size*0.6):
        warn_flag = 1
      else:
        warn_flag = 0
    else:
      self.outputBuffer.append(0)
      warn_flag = 0
    self.warningBuffer.append(warn_flag)
    if sum(self.warningBuffer) >= (self.wb_size*0.6) and self.num > 10:
      self.state = "WARNING"

  def reset(self):
    self.highPassFilter.reset()
    self.medianFilter.reset()
    self.state = "NORMAL"
    for i in xrange(0, self.ob_size-1):
      self.outputBuffer[i] = 0
    for j in xrange(0, self.wb_size-1):
      self.warningBuffer[j] = 0
    self.num = 0








