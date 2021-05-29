"""
  check make_website.py for the actual website-making

  this file simply runs and then kills make_website.py in 24 hour cycles

  each time make_website is called, refresh_db() is called at the start of it
"""

import subprocess as sp
import time

seconds_per_day = 60*60*24

while True:
  # run the make_website.py script in a subprocess - this also refreshes database
  proc = sp.Popen(["python3", "make_website.py"])
  print("website started and db refreshed")

  # stop running the website after 24 hours
  time.sleep(seconds_per_day)
  sp.Popen.terminate(proc)
  print("website stopped")