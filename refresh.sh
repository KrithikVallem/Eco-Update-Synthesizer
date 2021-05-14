#!/bin/bash
# This bash script will take care of the scheduling stuff.

# It will run constantly and will ping the /refresh endpoint of the flask website in main.py to refresh the database once a day

python3 "refresh.py" &
python3 "main.py" &
