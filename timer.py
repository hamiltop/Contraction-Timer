#!/usr/bin/python
import sys    
import termios
import fcntl
import os
from datetime import datetime


# getch is a blocking single character input function that
# does not require the \n termination to input
def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

state = 0
last_time = 0

while True:
  last_time = datetime.now()
  if state == 0:
    print "Timing Contraction"
  else:
    print "Waiting for new contraction to start"
  getch()
  time_diff = datetime.now() - last_time
  if state == 0:
    print "Contraction was %d minutes and  %d seconds long" % time_diff.seconds
  else:
    print "Time between contractions was %d minutes and %d seconds long" % time_diff.seconds
  state = (state + 1) % 2
  
  
