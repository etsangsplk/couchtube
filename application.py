#!couchtube-env/bin/python2.6
import flask
import dbutils
import datagrab
import runquery
import json


application = flask.Flask(__name__)


@application.route('/')
@application.route('/index')
def index():
    series = shows(json_obj=False)
    return flask.render_template("index.html", 
        series=series)


@application.route('/shows')
def shows(json_obj=True):
    db = dbutils.DbGet()
    series = db.get_shows()
    db.close()
    if not json_obj:
        return series
    else:
        series_json = []
        for show in series:
            series_json.append(
                {
                    'title': show[0],
                    'tokens': show[0].split(), 
                    'episodes': str(show[3]),
                    'ytcount': str(show[4])
                })
        return json.dumps(series_json)


@application.route('/about')
def about():
    return flask.render_template("about.html")


@application.route('/contact')
def contact():
    return flask.render_template("contact.html")


@application.route('/watch')
def watch():
    show = flask.request.args.get('nm', '')
    year = flask.request.args.get('yy', '')
    db = dbutils.DbGet()
    episodes = db.get_episodes(show, year)
    db.close()
    return flask.render_template("result.html", 
        show=show, 
        year=year, 
        episodes=episodes,
        seasons=set([e[1] for e in episodes]))


@application.route('/findShow')
def findShow():
    show = flask.request.args.get('title', '')
    data = datagrab.DataGrab(show)
    if data.show_title is not None:
        return flask.jsonify(data.tvdb)
    else:
        return 'None'
    

@application.route('/ingestData')
def ingestData():
    title = flask.request.args.get('title', '')
    show, _ = runquery.run_query(title)
    return flask.jsonify(show)

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')