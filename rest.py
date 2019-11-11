from flask import Flask, jsonify
import db
from gevent.pywsgi import WSGIServer
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/trump/<source>", methods=['GET'])
def getSentiment(source):
    results = {}
    timeline = list(db.getSentimentTimeline(source))
    for snapshot in timeline:
        if 'date' in snapshot:
            date = snapshot['date'].strftime('%Y:%m:%d')
            polarity = snapshot['polarity']
            subjectivity = snapshot['subjectivity']
            volume = snapshot['num_articles']
            results[date] = {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'volume': volume
            }
        else:
            print(snapshot)
    return jsonify(source=source, data=results)


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
