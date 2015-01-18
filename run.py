from flask import Flask, Response
from bson import json_util
from pymongo import MongoClient

app = Flask(__name__)

mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/<string:komuna>/monthly-summary/<int:viti>')
def paraqit_komunen(komuna, viti):
    rezultati = collection.aggregate([
      {
        "$match": {
          "viti": 2013,
          "city": "vitia"
        }
      },
      {
        "$group": {
          "_id": {
            "city": "$city",
            "muaji": {
              "$month": "$dataNenshkrimit"
            }
          },
          "vlera": {
            "$sum": "$kontrata.vlera"
          },
          "qmimi": {
            "$sum": "$kontrata.qmimi"
          }
        }
      },
      {
         "$project": {
          "muaji": "$_id.muaji",
          "komuna": "$_id.city",
          "vlera": "$vlera",
          "qmimi": "$qmimi",
          "_id": 0
        }
      },
      {
        "$sort": {
          "muaji": 1
        }
      }
    ])

    resp = Response(
        response=json_util.dumps(rezultati['result']),
        mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(debug=True)
