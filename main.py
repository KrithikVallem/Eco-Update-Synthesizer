# flask: web framework for rendering website
from flask import Flask, render_template, request

# makes it easier to work with the database
# all the custom code we wrote (analysis, etc...) is imported and called within this
from utilities import database_helpers as dbh

# use these to schedule database refreshes once a day
import time, threading


def make_website():
  app = Flask(__name__)

  # https://stackoverflow.com/a/31265602
  app.debug = False
  app.use_reloader=False

  @app.route('/', methods=['GET'])
  def create_website():
    return render_template(
      'index.html', 
      all_articles=dbh.get_current_articles()
    )

  app.run(host='0.0.0.0', port=8080)



# run this in a separate background thread
# so the flask app in the main thread doesn't block it
# https://stackoverflow.com/questions/62435134
# refreshes the database with new articles once a day
def schedule_database_refreshes():
  seconds_per_day = 60*60*24

  def background_task():
    while True:
      dbh.refresh_db()
      print("Database refreshed at " + time.ctime() + " UTC time")
      time.sleep(seconds_per_day)
  
  threading.Thread(target=background_task).start()



if __name__ == "__main__":
  schedule_database_refreshes()
  make_website()
