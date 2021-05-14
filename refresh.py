# This script will take care of the scheduling stuff.

# It will run constantly and will ping the /refresh endpoint of the flask website in main.py to refresh the database once a day

import time, os

seconds_per_day = 60*60*24

def ping_refresh_endpoint():
  os.system(
    'wget "https://Eco-Update-Synthesizer.vallemkr.repl.co/refresh" -O "refresh.txt"'
  )
  

while True:
  ping_refresh_endpoint()
  # time.sleep(seconds_per_day)
  time.sleep(5)

