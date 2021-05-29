# flask: web framework for rendering website
from flask import Flask, render_template, request

# makes it easier to work with the database
# all the custom code we wrote (analysis, etc...) is imported and called within this
from utilities import database_helpers as dbh


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


if __name__ == "__main__":
  dbh.refresh_db()
  make_website()
