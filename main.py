# flask: web framework for rendering website
from flask import Flask, render_template, request

import time

from utilities import database_helpers


def main():
  app = Flask(__name__)

  # scheduler = APScheduler()
  # scheduler.init_app(app)


  @app.route('/', methods=['GET'])
  def create_website():
    return render_template(
      'index.html', 
      all_articles=database_helpers.get_current_articles()
    )
  
  

  app.run(host='0.0.0.0', port=8080) 


if __name__ == "__main__":
  """
    # will close down an active flask app
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()
  """
  main()