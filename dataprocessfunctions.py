# -*- coding: utf-8 -*-
# import grovepi
import time
import collections # for deque class



class MedianFilter():
  state = "NORMAL"

  def __init__(self, delay):
    self.delay = delay
    self.historyBuffer = collections.deque(maxlen=delay)
    for i in range(0, self.delay-1):
      self.historyBuffer.append(0)

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
    for i in range(0, self.delay-1):
      self.historyBuffer[i] = 0
    return


class LowPassFilter():
  state = "NORMAL"
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
  def __init__(self, constant, highPassed, threshold, hm_delay, ch_delay, ob_size, ob_th):
    self.constant = constant
    self.highPassed = highPassed
    self.medianOfHighPassed = highPassed
    self.threshold = threshold
    self.hm_delay = hm_delay    
    self.hm = MedianFilter(self.hm_delay)
    self.ch_delay = ch_delay    # current highpass median filter
    self.ch = MedianFilter(self.ch_delay)
    self.highPassFilter = HighPassFilter(self.constant, self.highPassed, self.threshold)
    self.ob_size = ob_size
    self.ob_th = ob_th
  
    self.outputBuffer = collections.deque(maxlen = self.ob_size)
    
    for i in range(0, self.ob_size-1):
      self.outputBuffer.append(0)


  def addData(self, value):
    if self.num < 60:
      self.num += 1
    self.highPassed = self.highPassFilter.addData(value)
    self.cur_highPass = self.ch.addData(self.highPassed)
    self.diff = abs(self.cur_highPass - self.medianOfHighPassed)
    self.medianOfHighPassed = self.hm.addData(self.highPassed)
    
    if self.diff > self.threshold:
      self.outputBuffer.append(1)
      if sum(self.outputBuffer) >= self.ob_th and self.num > 55:
        self.state = "WARNING"
    else:
      self.outputBuffer.append(0)
       

  def reset(self):
    self.highPassFilter.reset()
    self.hm.reset()
    self.ch.reset()
    self.state = "NORMAL"
    for i in range(0, self.ob_size-1):
      self.outputBuffer[i] = 0
    self.num = 0








