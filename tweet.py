from flask import Flask,request,jsonify,render_template,redirect
from bson import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'twitter-db'
app.config['MONGO_URI'] = 'mongodb://ankit:twitterapi1@ds233737.mlab.com:33737/twitter-db'

mongo = PyMongo(app)

@app.route('/tweets',methods=['GET','POST','PUT'])
def tweets():
    
    if request.method == 'GET':
        
        tweets = mongo.db.tweets
        output = []

        for tweet in tweets.find():
            output.append({'Tweet' : tweet['tweet'],'id' : tweet['_id']})

        return render_template('tweets.html',tweets=output)
        
    if request.method == 'POST':
        
        tweets = mongo.db.tweets
        tweet = request.values.get('tweet')
        if tweet:
            tweet_id = tweets.insert({'tweet' : tweet})

        return redirect('/tweets')

@app.route("/delete")  
def remove ():  
    #Deleting a Task with various references  
    tweets = mongo.db.tweets
    key = request.values.get('_id')
    tweets.delete_one({"_id": ObjectId(key)})
    return redirect('/tweets')

@app.route("/update1")
def update1():
    tweets = mongo.db.tweets  
    key=request.values.get("_id")
    update=tweets.find({"_id":ObjectId(key)})  
    return render_template('update.html',Update=update)

@app.route("/update",methods=['POST'])
def update():

    tweets = mongo.db.tweets
    key = request.values.get('_id')
    tweet = request.values.get('updatetweet')
    tweets.update_one({"_id":ObjectId(key)},{"$set":{"tweet": tweet}})
    
    return redirect('/tweets')


if __name__ == "__main__":
    app.run(debug=True)