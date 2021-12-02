from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class LoginModel(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    time_in = db.Column(db.String(50), nullable=True)
    time_out = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Log(ID User = {self.id_user}, Day = {self.day}, time in = {self.time_in}, time out = {self.time_out})"


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User(Name = {self.name}, Age = {self.age}, sex = {self.sex})"

db.create_all()
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Name of user is required", required=True)
user_put_args.add_argument("age", type=int, help="Age of user is required", required=True)
user_put_args.add_argument("sex", type=str, help="Sex of user is required", required=True)

login_post_args = reqparse.RequestParser()
login_post_args.add_argument("id_user", type=int, help="IDs of user is required", required=True)
login_post_args.add_argument("time", type=str, help="Time log is required", required=True)
login_post_args.add_argument("day", type=str, help="Day log is required", required=True)

login_get_args = reqparse.RequestParser()
login_get_args.add_argument("id_user", type=int, help="IDs of user is required", required=True)
login_get_args.add_argument("day", type=str, help="IDs of user is required", required=False)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'sex': fields.String
}

resource_log = {
    "id_user": fields.Integer,
    "day": fields.String,
    "time": fields.String
}
resource_log1 = {
    "id_user": fields.Integer,
    "day": fields.String,
    "time_in": fields.String,
    "time_out": fields.String
}


class User(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UsersModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find User with that id")
        return result, 200

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = UsersModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User id taken...")

        user = UsersModel(id=user_id, name=args['name'], age=args['age'], sex=args['sex'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class diemdanh(Resource):
    @marshal_with(resource_log1)
    def post(self, user_id):
        args = login_get_args.parse_args()
        print(args)
        if args['day']:
            result = LoginModel.query.filter_by(id_user=args['id_user'], day=args['day']).first()
            if not result:
                abort(404, message="Could not find User with that id")
            return result, 200
        else:
            result = LoginModel.query.filter_by(id_user=args['id_user']).all()
            if not result:
                abort(404, message="Could not find User with that id")
            return result, 200

    @marshal_with(resource_log1)
    def put(self, user_id):
        args = login_post_args.parse_args()
        result = LoginModel.query.filter_by(id_user=args['id_user'], day=args["day"]).first()
        if result:
            result.time_out = args["time"]
            db.session.commit()
            return result, 200
        else:
            log = LoginModel(id_user=args['id_user'], day=args["day"], time_in=args['time'])
            db.session.add(log)
            db.session.commit()
            return log, 201


api.add_resource(User, "/user/<int:user_id>")
api.add_resource(diemdanh, "/log/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
