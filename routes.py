import functools
from flask import Blueprint, current_app, jsonify, request, session, Response
from dotenv import load_dotenv
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256
from models import TestCase, TestCaseSchema, User, UserSchema

load_dotenv()

test_cases = Blueprint("testCases", __name__)


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return Response("You need to login first.", status=201, mimetype='application/json')
        return route(*args, **kwargs)
    return route_wrapper


@test_cases.post("/register")
def register():
    if session.get("email"):
        return Response("You are already logged in.", status=200, mimetype='application/json')

    request_data = request.json
    schema = UserSchema()
    try:
        data = schema.load(request_data)
        user = User (
            name=data['name'],
            email=data['email'],
            password=pbkdf2_sha256.hash(data['password']),
        )
        current_app.session.add(user)
        current_app.session.commit()

        return Response("You have successfully created an account.", status=201, mimetype='application/json')
    
    except ValidationError as err:
        return jsonify(err.messages), 400


@test_cases.post("/login")
def login():
    if session.get("email"):
        return Response("You are already logged in.", status=200, mimetype='application/json')

    request_data = request.json
    schema = UserSchema()
    try:
        data = schema.load(request_data, partial=("name",))

        user = current_app.session.query(User).filter(User.email == data['email']).first()
        if not user:
            return Response("User not found", status=404, mimetype='application/json')

        if user and pbkdf2_sha256.verify(data['password'], user.password):
            session["user_id"] = user.id
            session["email"] = user.email
       
        return Response("You have logged in successfully.", status=200, mimetype='application/json')
    
    except ValidationError as err:
        return jsonify(err.messages), 400


@test_cases.get("/logout")
def logout():
    session.clear()
    return Response("You have logged out successfully.", status=200, mimetype='application/json')


@test_cases.get("/")
def get_all_tests():
    test_cases = current_app.session.query(TestCase).all()
    return jsonify(list(test_cases))


@test_cases.get("/<int:id>")
def get_test_by_id(id):
    test_case = current_app.session.get(TestCase, id)
    return jsonify(test_case)


@test_cases.get("/asset/<int:id>")
def get_tests_by_asset_id(id):
    test_case = current_app.session.query(TestCase).filter(TestCase.asset_id == id).all()
    return jsonify(list(test_case))


@test_cases.post('/create')
@login_required
def create_test():
    user_id = session["user_id"]
    request_data = request.json
    schema = TestCaseSchema()
    try:
        data = schema.load(request_data)
        test_case = TestCase (
            scenario=data['scenario'],
            steps=data['steps'],
            asset=data['asset'],
            asset_id=data['asset_id'],
            test_data=data['test_data'],
            actual_results=data['actual_results'],
            expected_results=data['expected_results'],
            status=data['status'],
            tester_id=user_id,
        )
        current_app.session.add(test_case)
        current_app.session.commit()
        return Response("You have successfully created a test case.", status=201, mimetype='application/json')
    
    except ValidationError as err:
        return jsonify(err.messages), 400
    

@test_cases.patch("/update/<int:id>")
@login_required
def update_test(id): 
    request_data = request.json
    schema = TestCaseSchema()
    try:
        data = schema.load(request_data, partial=True)
        current_app.session.query(TestCase).filter(TestCase.id == id).update(data)
        current_app.session.commit()
        return Response("Test case updated.", status=200, mimetype='application/json')
    
    except ValidationError as err:
        return jsonify(err.messages), 400 


@test_cases.delete("/delete/<int:id>")
@login_required
def delete_test(id):
    current_app.session.query(TestCase).filter(TestCase.id == id).delete()
    current_app.session.commit()
    return Response("Test case deleted.", status=200, mimetype='application/json')



