import os
import arrow

class TestModule():
  def __init__(self):
    self.val = 0

  def incVal(self):
    self.val += 1

  def decVal(self):
    self.val -= 1

  def getTime(self):
    utc = arrow.utcnow()

    return utc.format('HH:mm:ss')