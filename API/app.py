import os
import sys
import json
import math
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask import Flask, json, request, jsonify

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# run to set up db:
# flask db init
# flask db migrate -m "message" ?
# flask db upgrade


# __init__


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models


# helper table to link skins to users in a many to many relationship
skins = db.Table('skins',
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'user.id'), primary_key=True),
                 db.Column('skin_id', db.Integer, db.ForeignKey(
                     'skin.id'), primary_key=True)
                 )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    playcount = db.Column(db.Integer, default=0)
    hitcount = db.Column(db.Integer, default=0)
    total = db.Column(db.Float, default=0)
    aim = db.Column(db.Float, default=0)
    stamina = db.Column(db.Float, default=0)
    speed = db.Column(db.Float, default=0)
    scores = db.relationship('Score', backref='player', lazy='dynamic')
    skins = db.relationship('Skin', secondary=skins, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def SetPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def CheckPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def AddUser(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def DeleteUser(self, password):
        try:
            # mod powers by 1st user
            if(User.query.get(self.id).CheckPassword(password) or User.query.get(1).CheckPassword(password)):
                for skin in self.skins:
                    skin.RemoveUser(self.id, password)
                db.session.delete(User.query.get(self.id))
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    def UpdateLastSeen(self):
        # helper method used when loggin in, submitting scores
        # or saving/submitting skins
        try:
            self.last_seen = datetime.utcnow()
            return True
        except:
            return False

    def ScoreSubmit(self, hits):
        try:
            total = 0
            aim = 0
            stamina = 0
            speed = 0

            x = 0

            for score in self.scores.order_by(Score.total.desc()).slice(0, 99):
                total += score.total * (0.95 ** x)
                aim += score.aim * (0.95 ** x)
                stamina += score.stamina * (0.95 ** x)
                speed += score.speed * (0.95 ** x)

                x += 1

            self.total = total
            self.aim = aim
            self.stamina = stamina
            self.speed = speed

            if(hits > 0):
                self.playcount += 1
                self.UpdateLastSeen()
                self.hitcount += hits

            return True
        except:
            return False


class Skin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    background = db.Column(db.String(64))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    circleSize = db.Column(db.Integer)
    # circles, circle number at the end
    backgroundColor1 = db.Column(db.String(64))
    borderColor1 = db.Column(db.String(64))
    borderSize1 = db.Column(db.Integer)
    backgroundColor2 = db.Column(db.String(64))
    borderColor2 = db.Column(db.String(64))
    borderSize2 = db.Column(db.Integer)
    backgroundColor3 = db.Column(db.String(64))
    borderColor3 = db.Column(db.String(64))
    borderSize3 = db.Column(db.Integer)
    backgroundColor4 = db.Column(db.String(64))
    borderColor4 = db.Column(db.String(64))
    borderSize4 = db.Column(db.Integer)
    backgroundColor5 = db.Column(db.String(64))
    borderColor5 = db.Column(db.String(64))
    borderSize5 = db.Column(db.Integer)
    backgroundColor6 = db.Column(db.String(64))
    borderColor6 = db.Column(db.String(64))
    borderSize6 = db.Column(db.Integer)
    backgroundColor7 = db.Column(db.String(64))
    borderColor7 = db.Column(db.String(64))
    borderSize7 = db.Column(db.Integer)
    backgroundColor8 = db.Column(db.String(64))
    borderColor8 = db.Column(db.String(64))
    borderSize8 = db.Column(db.Integer)
    # many to many relationship with user in user model

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def CreateSkin(self, password):
        try:
            if(User.query.get(self.creator_id).CheckPassword(password)):
                db.session.add(self)
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    def DeleteSkin(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    def AddUser(self, userID, password):
        try:
            currentUser = User.query.get(userID)
            if(currentUser.CheckPassword(password)):
                self.users.append(currentUser)
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    def RemoveUser(self, userID, password):
        try:
            currentUser = User.query.get(userID)
            # mod powers by 1st user
            if(currentUser.CheckPassword(password) or User.query.get(1).CheckPassword(password)):
                self.users.remove(currentUser)
                db.session.commit()
                if not self.users:
                    self.DeleteSkin()
                return True
            else:
                return False
        except:
            return False


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dateTime = db.Column(db.DateTime, default=datetime.utcnow)
    spacing = db.Column(db.Integer)
    circleSize = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    numberOfCircles = db.Column(db.Integer)
    timeTaken = db.Column(db.Float)
    aim = db.Column(db.Float, default=0)
    stamina = db.Column(db.Float, default=0)
    speed = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def Calculate(self):
        # this will be used to calculate the
        # points that the score gets the user
        try:
            width = self.width
            height = self.height
            spacing = self.spacing
            circleSize = self.circleSize
            numberOfCircles = self.numberOfCircles
            timeTaken = self.timeTaken

            aim = ((spacing - circleSize) * 500 *
                   (numberOfCircles - 1) / (timeTaken * circleSize)) ** 2
            stamina = (spacing ** 2) * math.log(numberOfCircles) * numberOfCircles *\
                100 / (timeTaken * (circleSize ** 2))
            speed = (((numberOfCircles - 1) * 1000) / timeTaken) ** 2
            total = aim + stamina + speed

            if(total > 99999 or self.numberOfCircles/self.timeTaken > 0.03):
                self.aim = 0
                self.stamina = 0
                self.speed = 0
                self.total = 0
                db.session.commit()
                return False, 0, 0, 0, 0

            self.aim = aim
            self.stamina = stamina
            self.speed = speed
            self.total = total
            db.session.commit()

            return True, aim, stamina, speed, total
        except:
            return False

    def Submit(self, userPassword):
        try:
            player = User.query.get(self.player_id)
            if(player.CheckPassword(userPassword)):
                db.session.add(self)
                scores = self.Calculate()
                db.session.commit()
                player.ScoreSubmit(self.numberOfCircles)
                db.session.commit()
                return scores
            else:
                return False
        except Exception as e:
            return False


# the api/resource

# all classes need a OPTIONS request type return,
# since axios sends an OPTIONS request before each
# 'actual' request. doesn't need a response.

# anything below will not write to the database directly
# only read. Only the Models' methods above should write
api = Api(app)

# required to allow requests from axios
CORS(app)


class Positions(Resource):
    def post(self):
        requestData = request.json
        width = requestData['settings']['areaWidth']
        height = requestData['settings']['areaHeight']
        spacing = requestData['settings']['spacing']
        circleSize = requestData['settings']['circleSize']
        numberOfCircles = requestData['settings']['numberOfCircles'] - 1

        minY = 0
        minX = 0
        maxY = height - circleSize
        maxX = width - circleSize
        yCoordinate = minY
        xCoordinate = minX

        coordinateSet = [[xCoordinate, yCoordinate]]

        for i in range(numberOfCircles):
            if(bool(random.getrandbits(1))):
                negativeSwitcher = 1
            else:
                negativeSwitcher = -1

            change = random.randint(0, spacing)  # range of added y values
            yCoordinate += negativeSwitcher * change
            if (yCoordinate < minY or yCoordinate > maxY):
                yCoordinate -= 2 * negativeSwitcher * change

            if(bool(random.getrandbits(1))):
                negativeSwitcher = 1
            else:
                negativeSwitcher = -1

            change = math.floor(math.sqrt(spacing ** 2 - change ** 2))
            xCoordinate += negativeSwitcher * change
            if (xCoordinate < minX or xCoordinate > maxX):
                xCoordinate -= 2 * negativeSwitcher * change

            coordinateSet.append([xCoordinate, yCoordinate])

        return {
            'positions': coordinateSet,
            'settings': requestData
        }, 200

    def options(self):
        return


class Rankings(Resource):
    def get(self):
        requestData = request.args
        userQuery = User.query.order_by(User.total.desc()).slice(
            50 * (int(requestData['scorePage']) - 1), 50 * int(requestData['scorePage']))

        if(userQuery == None):
            return {'message': 'not found :/'}, 404

        users = []
        for user in userQuery:
            userData = {}
            userData['username'] = user.username
            userData['total'] = user.total
            userData['aim'] = user.aim
            userData['stamina'] = user.stamina
            userData['speed'] = user.speed
            userData['playcount'] = user.playcount
            userData['userID'] = user.id
            users.append(userData)

        return {'users': users}

    def options(self):
        return


class Account(Resource):
    def get(self):  # return all the info about the player,
        # might be extra but should be enough for user profile page (public)
        requestData = request.args

        queriedUser = User.query.get(requestData['userID'])

        if(queriedUser == None):
            return {'message': 'user not found'}, 404

        responseData = {'username': queriedUser.username}

        responseData['joinDate'] = str(queriedUser.join_date)
        responseData['lastSeen'] = str(queriedUser.last_seen)
        responseData['playcount'] = queriedUser.playcount
        responseData['hitcount'] = queriedUser.hitcount

        scores = []
        for score in queriedUser.scores.order_by(Score.total.desc()).slice(50 * (int(requestData['scorePage']) - 1), 50 * int(requestData['scorePage']) - 1):
            scoreData = {}
            scoreData['datetime'] = str(score.dateTime)
            scoreData['timeTaken'] = score.timeTaken
            scoreData['numberOfCircles'] = score.numberOfCircles
            scoreData['aim'] = score.aim
            scoreData['stamina'] = score.stamina
            scoreData['speed'] = score.speed
            scoreData['total'] = score.total
            scores.append(scoreData)

        skins = {}
        for skin in queriedUser.skins:
            skinData = {}
            skinData['name'] = skin.name
            skinData['created'] = str(skin.created)
            skins[skin.id] = skinData

        responseData['scores'] = scores
        responseData['skins'] = skins

        return responseData

    def post(self):
        requestData = request.json

        newUser = User(username=requestData['username'])
        newUser.SetPassword(requestData['password'])

        if(newUser.AddUser()):
            return {'message': 'User created!'}, 201
        else:
            return {'message': 'Unable to create user :('}, 418

    def put(self):  # deletes for now, will modify later too
        try:
            requestData = request.json

            queriedUser = User.query.filter_by(
                username=requestData['username']).first()

            if(requestData['option'] == "LogIn"):
                if(queriedUser.CheckPassword(requestData['password'])):
                    return {'userID': queriedUser.id}, 200
                else:
                    return {'message': 'Username or password not correct'}, 401
            elif(requestData['option'] == "delete"):
                if(queriedUser.DeleteUser(requestData['password'])):
                    return {'message': 'it is no more'}
                else:
                    return {'message': 'unable to do that'}, 401
            else:
                return {'message': 'Please provide valid option'}, 404
        except:
            return {'message': 'Please provide valid input'}, 401

    def options(self):
        return


class Scores(Resource):
    def post(self):
        requestData = request.json
        width = requestData['settings']['areaWidth']
        height = requestData['settings']['areaHeight']
        spacing = requestData['settings']['spacing']
        circleSize = requestData['settings']['circleSize']
        numberOfCircles = requestData['settings']['numberOfCircles']
        timeTaken = requestData['score']['timeTaken']
        player_id = requestData['userID']
        password = requestData['password']

        newScore = Score(width=width,
                         height=height,
                         spacing=spacing,
                         circleSize=circleSize,
                         numberOfCircles=numberOfCircles,
                         timeTaken=timeTaken,
                         player_id=player_id)

        success, aim, stamina, speed, total = newScore.Submit(password)
        if(success):
            return {'submissionSuccess': 'True',
                    'total': total,
                    'aim': aim,
                    'stamina': stamina,
                    'speed': speed}, 200
        else:
            return {'submissionSuccess': 'False'}, 418

    def put(self):
        requestData = request.json

        try:
            if (User.query.get(1).CheckPassword(requestData['password'])):
                for user in User.query.all():
                    for score in user.scores:
                        score.Calculate()
                    
                    user.ScoreSubmit(0)

            return 200
        except:
            return 401

    def options(self):
        return


class Skins(Resource):
    def get(self):
        requestData = request.args

        try:
            queriedSkin = Skin.query.filter_by(
                name=requestData['name']).first()
        except:
            return {'message': 'no skin'}, 404

        if(queriedSkin == None):
            return {'message': 'no skin'}, 404

        return {
            'name': queriedSkin.name,
            'created': str(queriedSkin.created),
            'background': queriedSkin.background,
            'width': queriedSkin.width,
            'height': queriedSkin.height,
            'circleSize': queriedSkin.circleSize,
            'circles': [
                {
                    'backgroundColor': queriedSkin.backgroundColor1,
                    'borderColor': queriedSkin.borderColor1,
                    'borderSize': queriedSkin.borderSize1
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor2,
                    'borderColor': queriedSkin.borderColor2,
                    'borderSize': queriedSkin.borderSize2
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor3,
                    'borderColor': queriedSkin.borderColor3,
                    'borderSize': queriedSkin.borderSize3
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor4,
                    'borderColor': queriedSkin.borderColor4,
                    'borderSize': queriedSkin.borderSize4
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor5,
                    'borderColor': queriedSkin.borderColor5,
                    'borderSize': queriedSkin.borderSize5
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor6,
                    'borderColor': queriedSkin.borderColor6,
                    'borderSize': queriedSkin.borderSize6
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor7,
                    'borderColor': queriedSkin.borderColor7,
                    'borderSize': queriedSkin.borderSize7
                },
                {
                    'backgroundColor': queriedSkin.backgroundColor8,
                    'borderColor': queriedSkin.borderColor8,
                    'borderSize': queriedSkin.borderSize8
                }
            ]
        }

    def put(self):
        requestData = request.json

        try:
            queriedSkin = Skin.query.filter_by(
                name=requestData['name']).first()
        except:
            return {'message': 'no skin'}, 404

        if(queriedSkin == None):
            return {'message': 'no skin'}, 404

        if(requestData['option'] == 'add'):
            if(queriedSkin.AddUser(requestData['userID'], requestData['password'])):
                return {'message': 'added!'}
            else:
                return {'message': 'Please provide valid credentials'}, 401

        elif(requestData['option'] == 'remove'):
            if(queriedSkin.RemoveUser(requestData['userID'], requestData['password'])):
                return {'message': 'removed!'}
            else:
                return {'message': 'Please provide valid credentials'}, 401

        elif(requestData['option'] == 'delete'):
            if(queriedSkin.DeleteSkin(requestData['userID'], requestData['password'])):
                return {'message': 'it is no more'}
            else:
                return {'message': 'Please provide valid credentials'}, 401
        else:
            return {'message': 'Please provide a valid option'}, 400

    def post(self):
        requestData = request.json

        newSkin = Skin(name=requestData['name'],
                       creator_id=requestData['creator'],
                       background=requestData['background'],
                       width=requestData['width'],
                       height=requestData['height'],
                       circleSize=requestData['circleSize'],
                       backgroundColor1=requestData['circles'][0]['backgroundColor'],
                       borderColor1=requestData['circles'][0]['borderColor'],
                       borderSize1=requestData['circles'][0]['borderSize'],
                       backgroundColor2=requestData['circles'][1]['backgroundColor'],
                       borderColor2=requestData['circles'][1]['borderColor'],
                       borderSize2=requestData['circles'][1]['borderSize'],
                       backgroundColor3=requestData['circles'][2]['backgroundColor'],
                       borderColor3=requestData['circles'][2]['borderColor'],
                       borderSize3=requestData['circles'][2]['borderSize'],
                       backgroundColor4=requestData['circles'][3]['backgroundColor'],
                       borderColor4=requestData['circles'][3]['borderColor'],
                       borderSize4=requestData['circles'][3]['borderSize'],
                       backgroundColor5=requestData['circles'][4]['backgroundColor'],
                       borderColor5=requestData['circles'][4]['borderColor'],
                       borderSize5=requestData['circles'][4]['borderSize'],
                       backgroundColor6=requestData['circles'][5]['backgroundColor'],
                       borderColor6=requestData['circles'][5]['borderColor'],
                       borderSize6=requestData['circles'][5]['borderSize'],
                       backgroundColor7=requestData['circles'][6]['backgroundColor'],
                       borderColor7=requestData['circles'][6]['borderColor'],
                       borderSize7=requestData['circles'][6]['borderSize'],
                       backgroundColor8=requestData['circles'][7]['backgroundColor'],
                       borderColor8=requestData['circles'][7]['borderColor'],
                       borderSize8=requestData['circles'][7]['borderSize']
                       )

        if(newSkin.CreateSkin(requestData['password'])):
            return {'message': 'Skin has been uploaded!'}, 201
        else:
            return {'message': 'unable to upload skin :('}, 401

    def options(self):
        return


api.add_resource(Positions, '/positions')
api.add_resource(Rankings, '/rankings')
api.add_resource(Account, '/profile')
api.add_resource(Scores, '/scores')
api.add_resource(Skins, '/skins')

if __name__ == "__main__":
    app.run(debug=True)
