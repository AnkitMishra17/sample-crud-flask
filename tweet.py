from flask import Flask,request,jsonify,render_template,redirect
from bson import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'twitter-db'
app.config['MONGO_URI'] = 'mongodb://ankit:twitterapi1@ds233737.mlab.com:33737/twitter-db'

mongo = PyMongo(app)

@app.route('/tweets',methods=['GET','POST','PUT','DELETE'])
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
        tweet_id = tweets.insert({'tweet' : tweet})
        
        output = []

        for tweet in tweets.find():
            output.append({'Tweet' : tweet['tweet']})

        return redirect('/tweets')

    if request.method == 'PUT':    
        
        tweets = mongo.db.tweets
        tweet = request.json['tweet']
        tweets.update_one({"tweet":"First Tweet"},{"$set":{"tweet": tweet}})

        result = tweets.find_one({"tweet": tweet})
        output = {'Updated Tweet' : result['tweet']}

        return jsonify({'Tweet' : output}) 
        

@app.route("/delete")  
def remove ():  
    #Deleting a Task with various references  
    tweets = mongo.db.tweets
    key = request.values.get('_id')
    tweets.delete_one({"_id": ObjectId(key)})
    return redirect('/tweets')

if __name__ == "__main__":
    app.run(debug=True)